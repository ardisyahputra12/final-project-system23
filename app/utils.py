import os
from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    text
)


def get_engine():
    engine = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        os.environ["POSTGRES_USER"],
        os.environ["POSTGRES_PASSWORD"],
        os.environ["POSTGRES_HOST"],
        os.environ["POSTGRES_PORT"],
        os.environ["POSTGRES_DB"],
    )
    return create_engine(engine, future=True)

def create_table():
    engine = get_engine()
    meta = MetaData()
    # Table is not yet fix
    Table(
        "users",
        meta,
        Column("type", String, nullable=False),
        Column("username", String, nullable=False, unique=True),
        Column("password", String, nullable=False),
        Column("balance", String, nullable=False, server_default="0"),
        Column("token", String, nullable=True, unique=True),
    )
    meta.create_all(engine)

def run_query(query, commit: bool = False):
    engine = get_engine()
    if isinstance(query, str):
        query = text(query)

    with engine.connect() as conn:
        if commit:
            conn.execute(query)
            conn.commit()
        else:
            return [dict(row) for row in conn.execute(query)]

def error_message(msg: str, sts: int):
    return {"error": msg}, sts

def success_message(msg: str, sts: int, tkn: str = None):
    val = {"message": msg}
    if tkn!=None: val["token"] = tkn
    return val, sts