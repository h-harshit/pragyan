from fastapi import FastAPI
from common.connections import app_db_engine, init_db
from routers.connections import connections_router
from routers.auth import auth_router
from routers.data import data_router
from contextlib import asynccontextmanager
# from connectors import DbConnection, ConnectionEngine


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await app_db_engine.dispose()


app = FastAPI(debug=True, lifespan=lifespan)

app.include_router(connections_router, prefix="/api/v1/connections")
app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(data_router, prefix="/api/v1/data")


@app.get("/")
async def root():
    return {"message": "Hello Pragyan"}
