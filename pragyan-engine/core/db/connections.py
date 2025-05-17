import json
from sqlalchemy import text, select
import redis
from redis import Connection
from security.encryption import Encryptor
from common.logging import LOGGER
from uuid import uuid4
from datetime import datetime
from config import config
from models.connections import ClientConnectionConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine import URL
from core.db.utils import QueryUtils, encrypt_credentials
from sqlalchemy.exc import SQLAlchemyError
from common.caching import CacheManager


class RedisConnection:
    def __init__(
        self,
        host: str = config.REDIS_HOST,
        port: int = config.REDIS_PORT,
        db: int = config.REDIS_ACTIVE_CONN_DB_INDEX,
        decode_responses: bool = True,
    ) -> None:
        self.rconn = None
        self.host = host
        self.port = port
        self.db = db
        self.decode_responses = decode_responses

    def __enter__(self) -> Connection:
        self.rconn = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=self.decode_responses,
        )
        return self.rconn

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.rconn:
            self.rconn.close()


class ConnectionManager:
    def __init__(
        self,
        user: str,
        app_db_session,
        dbtype: str,
        username: str,  # client db_user
        password: str,  # client db_password
        host: str,
        port: int,
        database: str,
        engine_id: str = None,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: int = 30,
        pool_recycle: int = 1800,
    ):
        self.user = user
        self.dbtype = dbtype
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_timeout = pool_timeout
        self.pool_recycle = pool_recycle

        self.conn_engine = None
        self.engine_id = engine_id

        self.app_db_session = app_db_session

    @classmethod
    async def _test_conn(cls, conn_engine) -> None:
        if not conn_engine:
            raise ValueError("No connection engine provided.")
        try:
            async with conn_engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
        except SQLAlchemyError as err:
            LOGGER.error(f"Error connecting to database, {err}")
            raise ConnectionError("Error connecting to database")

    def _cache_conn_config(
        self,
        engine_id: str,
        encrypted_conn_string: str,
        db_dialect: str,
        modified_at: datetime,
        created_at: datetime = datetime.now(),
    ) -> None:
        with RedisConnection() as rconn:
            engine_id = str(engine_id)
            client_config_dict = {
                "user_id": self.user,
                "engine_id": engine_id,
                "conn_string": encrypted_conn_string,
                "db_name": self.database,
                "dialect": db_dialect,
                "modified_at": str(modified_at),
                "created_at": str(created_at),
            }

            cache = CacheManager(rconn)
            client_configs = cache.get(self.user)

            if client_configs is None:
                client_configs = dict()
                client_configs[engine_id] = client_config_dict
            else:
                client_configs = json.loads(client_configs)
                if engine_id in client_configs:
                    client_configs[engine_id] = {
                        **client_configs[engine_id],
                        "conn_string": encrypted_conn_string,
                        "db_name": self.database,
                        "dialect": db_dialect,
                        "modified_at": str(modified_at),
                    }
                else:
                    client_configs[engine_id] = client_config_dict

            cache.set(self.user, json.dumps(client_configs))

    def _invalidate_cached_conn(cls, user, engine_id: str):
        with RedisConnection() as rconn:
            cache = CacheManager(rconn)
            engine_id = str(engine_id)
            client_configs = cache.get(user)

            if client_configs:
                if engine_id in client_configs:
                    del client_configs[engine_id]

            cache.set(user, client_configs)

    async def _persist_conn_config(
        self,
        engine_id: str,
        encrypted_conn_string: str,
        db_dialect: str,
        created_at: datetime,
        modified_at: datetime,
    ):
        new_connection_config = ClientConnectionConfig(
            user_id=self.user,
            engine_id=engine_id,
            conn_string=encrypted_conn_string,
            db_name=self.database,
            dialect=db_dialect,
            created_at=created_at,
            modified_at=modified_at,
        )

        self.app_db_session.add(new_connection_config)
        await self.app_db_session.commit()

    def _create_conn_engine(self, conn_string: str):
        return create_async_engine(
            conn_string,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            pool_timeout=self.pool_timeout,
            pool_recycle=self.pool_recycle,
        )

    async def create_conn_engine(self):
        db_dialect = QueryUtils.get_db_dialect(self.dbtype)
        conn_string = URL.create(
            f"{self.dbtype}+{db_dialect}",
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )
        self.conn_engine = self._create_conn_engine(conn_string)

        # testing connection
        await self.__class__._test_conn(self.conn_engine)

        # assigning engine id
        self.engine_id = uuid4()
        encrypted_conn_string = encrypt_credentials(conn_string)
        current_time = datetime.now()

        # persisting client connection config
        await self._persist_conn_config(
            self.engine_id,
            encrypted_conn_string,
            db_dialect,
            current_time,
            current_time,
        )

        # caching client connection config
        self._cache_conn_config(
            self.engine_id,
            encrypted_conn_string,
            db_dialect,
            modified_at=current_time,
            created_at=current_time,
        )

    async def _update_conn_config(
        self, engine_id: str, encrypted_conn_string: str, db_dialect: str
    ):
        stmt = select(ClientConnectionConfig).where(
            ClientConnectionConfig.engine_id == engine_id
        )
        result = await self.app_db_session.execute(stmt)
        client_conn_config = result.scalar_one_or_none()
        if client_conn_config:
            client_conn_config.conn_string = encrypted_conn_string
            client_conn_config.db_dialect = db_dialect
            client_conn_config.db_name = self.database

            await self.app_db_session.commit()

            # updating cache
            self._cache_conn_config(
                self.engine_id,
                encrypted_conn_string,
                db_dialect,
                modified_at=datetime.now(),
            )

    async def update_conn_engine(self):
        db_dialect = QueryUtils.get_db_dialect(self.dbtype)
        conn_string = URL.create(
            f"{self.dbtype}+{db_dialect}",
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )

        self.conn_engine = self._create_conn_engine(conn_string)

        # testing connection
        await self.__class__._test_conn(self.conn_engine)

        encrypted_conn_string = encrypt_credentials(conn_string)

        # update connection in db
        await self._update_conn_config(
            self.engine_id, encrypted_conn_string, db_dialect
        )

    @classmethod
    async def _delete_conn_config(cls, user, app_db_session, engine_id: str):
        stmt = select(ClientConnectionConfig).where(
            ClientConnectionConfig.engine_id == engine_id
        )
        result = await app_db_session.execute(stmt)
        client_conn_config = result.scalar_one_or_none()
        if client_conn_config:
            await app_db_session.delete(client_conn_config)
            await app_db_session.commit()

            cls._invalidate_cached_conn(user, engine_id)

    @classmethod
    async def delete_conn_engine(cls, user, app_db_session, engine_id):
        await cls._delete_conn_config(user, app_db_session, engine_id)

    @classmethod
    async def _get_conn_engine_from_string(cls, conn_string: str):
        encryptor = Encryptor(key=config.FERNET_KEY)
        decrypted_client_conn_string = encryptor.decrypt(conn_string)

        client_conn_engine = create_async_engine(
            decrypted_client_conn_string,
        )

        await cls._test_conn(client_conn_engine)

        return client_conn_engine

    @classmethod
    async def _fetch_cached_client_config(cls, user: str, engine_id: str):
        with RedisConnection() as rconn:
            cache = CacheManager(rconn)
            client_conn_configs = cache.get(user)
            if client_conn_configs and (engine_id in client_conn_configs):
                client_conn_config = client_conn_configs[engine_id]
                if client_conn_config:
                    client_conn_string = client_conn_config.conn_string
                    client_conn_engine = await cls._get_conn_engine_from_string(
                        client_conn_string
                    )
                    return client_conn_engine

    @classmethod
    async def _fetch_client_config_from_db(
        cls, user: str, engine_id: str, app_db_session
    ):
        stmt = select(ClientConnectionConfig).where(
            ClientConnectionConfig.engine_id == engine_id
            and ClientConnectionConfig.user_id == user
        )
        result = await app_db_session.execute(stmt)
        client_conn_config = result.scalar_one_or_none()
        if client_conn_config:
            client_conn_string = client_conn_config.conn_string
            client_conn_engine = await cls._get_conn_engine_from_string(
                client_conn_string
            )
            return client_conn_engine

    @classmethod
    async def get_client_conn_engine(cls, engine_id: str, user: str, app_db_session):
        client_conn_engine = await cls._fetch_cached_client_config(user, engine_id)
        if client_conn_engine:
            await cls._test_conn(client_conn_engine)
            return client_conn_engine
        else:
            client_conn_engine = await cls._fetch_client_config_from_db(
                user, engine_id, app_db_session
            )
            await cls._test_conn(client_conn_engine)
            return client_conn_engine
