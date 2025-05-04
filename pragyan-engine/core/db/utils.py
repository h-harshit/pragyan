import sqlparse
from sqlparse.sql import Statement
from sqlparse import tokens
from common.logging import LOGGER
from sqlalchemy.engine import URL
from config import config
from security.encryption import Encryptor


class QueryUtils:
    def __init__(self) -> None:
        pass

    @classmethod
    def format_query(cls, query: str) -> str:
        if not query:
            raise ValueError("Query cannot be None or empty")
        query_list_after_split = query.strip("\n").split("\n")
        clean_query = " ".join(query_list_after_split)
        formatted_query = sqlparse.format(
            clean_query, reindent=True, keyword_case="upper"
        )
        return formatted_query

    @classmethod
    def get_query_type(cls, query_stmt: Statement):
        if query_stmt:
            return query_stmt.get_type()

    @classmethod
    def contains_cte(cls, query_stmt: Statement):
        for token in query_stmt.tokens:
            if token.ttype == tokens.Keyword.CTE:
                return True
        return False

    @classmethod
    def check_query_sanity(cls, query_str: str):
        parsed_query_statements = sqlparse.parse(query_str)
        assert len(parsed_query_statements) == 1, (
            f"Batched or empty queries not allowed. query_stmt_len: {len(parsed_query_statements)}"
        )
        parsed_query_statement = parsed_query_statements[0]
        assert cls.get_query_type(parsed_query_statement) == "SELECT", (
            "Invalid query type, only select query allowed"
        )
        assert not cls.contains_cte(parsed_query_statement), (
            "Invalid query, CTE not allowed"
        )

    @classmethod
    def get_db_dialect(cls, dbtype: str):
        db_dialect_mapping = {"postgresql": "psycopg"}

        try:
            return db_dialect_mapping[dbtype]
        except KeyError:
            LOGGER.error(f"No dialect found for db: {dbtype}")
            return None


def encrypt_credentials(credential: URL) -> str:
    credential = credential.render_as_string(hide_password=False)
    try:
        encryption_key = config.FERNET_KEY
        encryptor = Encryptor(key=encryption_key)
        return encryptor.encrypt(credential)
    except ValueError as err:
        LOGGER.error(err)
        raise err
    except AttributeError as err:
        LOGGER.error(err)
        raise err
