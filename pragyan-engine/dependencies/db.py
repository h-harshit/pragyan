from common.connections import AppDBSessionLocal


async def get_db_session():
    db_session = AppDBSessionLocal()
    try:
        yield db_session
    finally:
        await db_session.close()
