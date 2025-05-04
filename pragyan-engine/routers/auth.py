from config import config
from datetime import timedelta

# from entities.auth_entities import NewUser, AuthToken
from fastapi import Request, APIRouter, HTTPException, status, Depends
from core.auth import AuthService
from common.errors.auth import UserAlreadyExists
from entities.auth import RegisterUser
from fastapi.security import OAuth2PasswordRequestForm
from common.logging import LOGGER
from dependencies.db import get_db_session
from sqlalchemy.exc import IntegrityError

auth_router = APIRouter()


@auth_router.post(
    "/user/register",
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    user_data: RegisterUser,
    app_db_session=Depends(get_db_session),
):
    try:
        auth_service = AuthService(app_db_session)
        new_user = await auth_service.register_user(user_data)
        LOGGER.info("user successfully created.")
    except UserAlreadyExists as err:
        LOGGER.error(err)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User Already Exists!"
        )
    except IntegrityError as err:
        LOGGER.error(err)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Unique Violation"
        )
    except Exception as err:
        LOGGER.error(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong on server",
        )

    response = {"created_user": new_user}
    return response


@auth_router.post("/user/login", status_code=status.HTTP_200_OK)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    app_db_session=Depends(get_db_session),
):
    # formdata should contain 'username' and 'password' as per OAuth2 specification
    try:
        auth_service = AuthService(app_db_session)
        user = await auth_service.authenticate_user(
            form_data.username, form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRES_MINUTES)
        access_token = auth_service.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        response = {"access_token": access_token, "token_type": "Bearer"}
        return response
    except Exception as err:
        LOGGER.error(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong on server",
        )
