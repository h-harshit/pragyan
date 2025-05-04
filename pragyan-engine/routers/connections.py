from fastapi import APIRouter, HTTPException, status, Depends, Response
from entities.connections import CreateConnection
from entities.auth import User
from dependencies.auth import get_current_user
from core.db.connections import ConnectionManager
from dependencies.db import get_db_session
from sqlalchemy.exc import OperationalError, IntegrityError
from redis.exceptions import ConnectionError
from common.logging import LOGGER
from core.data.service import DataService

connections_router = APIRouter()


@connections_router.post("/connections/")
async def create_connection(
    response: Response,
    payload: CreateConnection,
    user: User = Depends(get_current_user),
    app_db_session=Depends(get_db_session),
):
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")

    dbtype = payload.dbtype
    username = payload.username
    password = payload.password
    host = payload.host
    port = payload.port
    database = payload.database

    try:
        conn_manager = ConnectionManager(
            user.email, app_db_session, dbtype, username, password, host, port, database
        )
        await conn_manager.create_conn_engine()
    except OperationalError as err:
        LOGGER.error(err)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to connect to the database",
        )
    except IntegrityError as err:
        LOGGER.error(err)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid connection request",
        )
    except ConnectionError as err:
        LOGGER.error(err)
        response.headers["X-Redis-Cache-Status"] = "failed"
    return {"message": "Connection created successfully"}


@connections_router.put("/connections/{connection_id}/")
async def update_connection(
    connection_id: str,
    payload: CreateConnection,
    user: User = Depends(get_current_user),
    app_db_session=Depends(get_db_session),
):
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")

    try:
        conn_manager = ConnectionManager(
            user.email,
            app_db_session,
            payload.dbtype,
            payload.username,
            payload.password,
            payload.host,
            payload.port,
            payload.database,
            engine_id=connection_id,
        )
        await conn_manager.update_conn_engine()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Conn string not valid"
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return {"message": "Connection updated successfully"}


@connections_router.delete("/connections/{connection_id}/")
async def delete_connection(
    connection_id: str,
    user: User = Depends(get_current_user),
    app_db_session=Depends(get_db_session),
):
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")

    try:
        await ConnectionManager.delete_conn_engine(
            user.email, app_db_session, connection_id
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return {"message": "Connection deleted successfully"}
