"""auth_services.py

This module provides services for authentication
"""

from jose import jwt
from typing import Union
from config import config
from entities.auth import User
from models.auth import Users
from sqlalchemy import select

# from services.crud_services import CRUDService
# from common.errors.db import ResourceNotFound
from common.errors.auth import UserAlreadyExists
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from common.logging import LOGGER

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, app_db_session: Session) -> None:
        self.app_db_session = app_db_session

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return pwd_context.hash(password)

    async def get_user(self, username: str) -> Union[User, None]:
        # read_query_filepath = "./SQL/auth/read_superuser.sql"
        # crud_service = CRUDService(self.conn)
        # avoiding circular imports
        # from serializers.auth import UserSerializer

        stmt = select(Users).where(Users.email == username)

        result = await self.app_db_session.execute(stmt)
        user = result.scalars().first()
        return user

    async def register_user(self, user_data) -> Users:
        # Avoiding circular imports
        from serializers.auth import NewUserSerializer, UserSerializer

        user = await self.get_user(user_data.email)
        if user:
            raise UserAlreadyExists

        user_dict = user_data.model_dump()
        serialized_new_user = NewUserSerializer(user_dict)

        new_user = Users(
            email=serialized_new_user.get("email"),
            first_name=serialized_new_user.get("first_name"),
            last_name=serialized_new_user.get("last_name"),
            passhash=serialized_new_user.get("passhash"),
        )

        self.app_db_session.add(new_user)
        await self.app_db_session.commit()

        # Not using new_user after the commit to avoid Missing Greenlet error
        return serialized_new_user.get("email")

    def create_access_token(
        self, data: dict, expires_delta: Union[timedelta, None] = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(
                minutes=config.ACCESS_TOKEN_EXPIRES_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM
        )
        return encoded_jwt

    def verify_password(self, plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def authenticate_user(self, username, password: str) -> Union[User, bool]:
        user = await self.get_user(username)
        if not user:
            return False

        if isinstance(user, list):
            user = user[0]
        if not self.verify_password(password, user.passhash):
            return False
        return user
