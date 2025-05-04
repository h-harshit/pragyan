from collections import OrderedDict
from core.auth import AuthService
from models.auth import Users


def UserSerializer(user_record: Users) -> dict:
    serialized_user = OrderedDict(
        email=user_record.email,
        first_name=user_record.first_name,
        last_name=user_record.last_name,
    )

    return serialized_user


def NewUserSerializer(user: dict) -> dict:
    return OrderedDict(
        email=user.get("email"),
        first_name=user.get("first_name"),
        last_name=user.get("last_name"),
        passhash=AuthService.get_password_hash(user.get("password")),
    )
