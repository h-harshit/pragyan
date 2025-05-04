from config import config
from jose import JWTError, jwt
from fastapi import HTTPException, status
from entities.auth import AuthTokenData
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from core.auth import AuthService
from common.logging import LOGGER
from dependencies.db import get_db_session

user_oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config.USER_TOKEN_URL)


async def get_current_user(
    token: str = Depends(user_oauth2_scheme),
    app_db_session=Depends(get_db_session),
):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        # JWT specification has "sub" as Subject (in this case username) of the token
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user credentials",
            )
        token_data = AuthTokenData(username=username)
    except JWTError as err:
        LOGGER.error(err)
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="Could not validate user credentials"
        )

    # async with request.app.async_pool.connection() as conn:
    auth_service = AuthService(app_db_session)
    user = await auth_service.get_user(username=token_data.username)
    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user credentials",
        )
    return user
