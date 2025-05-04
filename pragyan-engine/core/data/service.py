from entities.auth import User
from core.db.connections import ConnectionManager
from core.db.utils import QueryUtils
from common.logging import LOGGER
from sqlalchemy import text
import polars as pl
import duckdb
from config import config


class DataService:
    def __init__(self, app_db_session=None):
        self.app_db_session = app_db_session

    async def extract_data_from_query(self, user: User, engine_id: str, query: str):
        try:
            QueryUtils.check_query_sanity(query)
        except AssertionError as err:
            LOGGER.error(err)
            raise err

        if self.app_db_session:
            client_conn_engine = await ConnectionManager.get_client_conn_engine(
                engine_id, user, self.app_db_session
            )

            formatted_query = QueryUtils.format_query(query)
            async with client_conn_engine.connect() as conn:
                result = await conn.execute(text(formatted_query))

            rows = result.fetchall()
            columns = result.keys()

            return {"rows": rows, "columns": columns}

    def write_extract_to_parquet(self, data_extract, extract_name: str):
        rows = data_extract["rows"]
        columns = data_extract["columns"]
        data = [dict(zip(columns, row)) for row in rows]
        lazy_df = pl.LazyFrame(data)
        lazy_df.sink_parquet(f"./extract/{extract_name}.parquet", compression="snappy")

    async def extract_data(
        self, extract_name: str, user: str, engine_id: str, query: str
    ):
        data_extract = await self.extract_data_from_query(user, engine_id, query)
        self.write_extract_to_parquet(data_extract, extract_name)

    def get_data(
        self,
        user: str,
        extract_name: str,
        page: int = 1,
        page_size: int = config.DEFAULT_PAGE_SIZE,
    ):
        extract_duck_tbl = duckdb.read_parquet(f"./extract/{extract_name}.parquet")
        result = extract_duck_tbl.limit(page_size, offset=page * page_size)
        columns = [desc[0] for desc in extract_duck_tbl.description]

        data = [dict(zip(columns, row)) for row in result.fetchall()]
        return data


class UploadService:
    def __init__(self, extract_name, file_type):
        self.extract_name = extract_name
        self.file_type = file_type

    def upload_csv_file(self, file_content):
        csv_file_read = duckdb.read_csv(file_content)
        csv_file_read.write_parquet(
            f"{self.extract_name}.parquet", compression="snappy"
        )

    def upload_file(self, file_content):
        if self.file_type == "csv":
            self.upload_csv_file(file_content)
