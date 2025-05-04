from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import config
from models.base import Base
from common.logging import LOGGER

APP_DB_URL = (
    f"postgresql+psycopg://{config.PG_USER}:"
    f"{config.PG_PASSWORD}@"
    f"{config.PG_HOST}:"
    f"{config.PG_PORT}/"
    f"{config.PG_APP_DB}"
)
app_db_engine = create_async_engine(APP_DB_URL)
AppDBSessionLocal = async_sessionmaker(bind=app_db_engine)


async def init_db():
    async with app_db_engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
        except Exception as e:
            LOGGER.fatal(e)
            raise e
