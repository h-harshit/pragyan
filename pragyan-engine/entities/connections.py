from pydantic import BaseModel


class CreateConnection(BaseModel):
    dbtype: str
    username: str
    password: str
    host: str
    port: int
    database: str
