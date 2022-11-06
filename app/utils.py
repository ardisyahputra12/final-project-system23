from datetime import datetime
from sqlalchemy import text
from models import get_engine


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

def format_datetime():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string