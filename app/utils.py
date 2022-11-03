import os
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    ForeignKey,
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
    Table(
        "categories",
        meta,
        Column("category_id", String, nullable=False, unique=True),
        Column("category_name", String, nullable=False, server_default="None"),
        Column("create_at", String, nullable=False, server_default="None"),
        Column("create_by", String, nullable=False, server_default="None"),
        Column("update_at", String, nullable=True, server_default="None"),
        Column("update_by", String, nullable=True, server_default="None"),
    )
    Table(
        "products",
        meta,
        Column("product_id", String, nullable=False, unique=True),
        Column("category_id", String, ForeignKey('categories.category_id', ondelete='CASCADE', onupdate='CASCADE',), nullable=False),
        Column("product_name", String, nullable=False, server_default="None"),
        Column("product_price", Integer, nullable=False, server_default="0"),
        Column("product_detail", String, nullable=False, server_default="None"),
        Column("product_size", String, nullable=False, server_default="['S', 'M', 'L']"),
        Column("product_condition", String, nullable=False, server_default="deleted"),          # product_condition == new/used/deleted
        Column("product_image", String, nullable=False, server_default="None"),
        Column("product_images_url", String, nullable=False, server_default="None"),
        Column("create_at", String, nullable=False, server_default="None"),
        Column("create_by", String, nullable=False, server_default="None"),
        Column("update_at", String, nullable=True, server_default="None"),
        Column("update_by", String, nullable=True, server_default="None"),
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

def error_message(sts: int, msg: str):
    """
    This function is for handle error message.\n
    sts => status code,\n
    msg => message for return
    """
    return {"error": msg}, sts

def success_message(sts: int, data: str = None, msg: str = None, key: str = None, tkn: str = None, row: bool = False):
    """
    This function is for handle success message.\n
    sts => status code,\n
    data => result from run_query function,\n
    msg => message for return,\n
    key => define new key (default is data),\n
    tkn => token or id,\n
    row => show total row from parameter data if True (default is False)
    """
    val = {"data": [data]}
    if tkn!=None: val["token"] = tkn
    if row!=False: val["total_rows"]= len(data)
    if msg!=None: return msg, sts
    if key!=None: val = {f"{key}": data}
    return val, sts