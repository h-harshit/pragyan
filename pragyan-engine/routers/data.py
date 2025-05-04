from fastapi import APIRouter, status, HTTPException, Depends, UploadFile
from common.logging import LOGGER
from entities.data import ExtractData
from entities.auth import User
from dependencies.auth import get_current_user
from dependencies.db import get_db_session
from core.data.service import UploadService, DataService

data_router = APIRouter()


@data_router.post("/upload/{file_type}/{extract_name}")
async def upload_file(file_type: str, extract_name: str, file: UploadFile):
    try:
        file_content = file.file
        upload_service = UploadService(extract_name, file_type)
        upload_service.upload_file(file_content)
    except Exception as err:
        LOGGER.error(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong on server",
        )


@data_router.post("/extract")
async def extract_data(
    payload: ExtractData,
    user: User = Depends(get_current_user),
    app_db_session=Depends(get_db_session),
):
    try:
        data_service = DataService(app_db_session)
        engine_id = payload.engine_id
        query_str = payload.query_str
        extract_name = payload.extract_name
        data_service.extract_data(extract_name, user.email, engine_id, query_str)
    except Exception as err:
        LOGGER.error(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong on server",
        )


@data_router.get("/extract")
async def query_client(
    connection_id: str,
    query: str,
    user: User = Depends(get_current_user),
    app_db_session=Depends(get_db_session),
):
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")

    try:
        data_service = DataService(app_db_session)
        result = await data_service.extract_data(
            "data_extract", user.email, connection_id, query
        )
    except AssertionError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid query request"
        )

    return result


@data_router.get("/extract/{extract_name}/{page}")
async def get_data(
    extract_name: str, page: int, user: User = Depends(get_current_user)
):
    try:
        data_service = DataService()
        result = data_service.get_data(user.email, extract_name, page)
    except Exception as err:
        LOGGER.error(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong on server",
        )

    return result
