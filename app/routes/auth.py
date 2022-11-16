# import uuid
# from flask import request
# from sqlalchemy import (
#     update,
#     delete,
#     insert,
#     select,
# )
# from werkzeug.security import (
#     generate_password_hash,
#     check_password_hash,
# )
# from app.utils.query import run_query
# from app.utils.format_datetime import format_datetime
# from app.utils.auth_token import encode_auth_token
# from app.utils.response import (
#     error_message,
#     success_message,
# )
# from app.models.user import Users
# from . import sign_up_bp, sign_in_bp


# @sign_up_bp.route("", methods=["POST"])
# def sign_up():
#     body = request.json
#     id = uuid.uuid4()
#     name = body["name"]
#     email = body["email"]
#     number = body["number"]
#     password = body["password"]
#     type = body["type"]
    
#     #for testing only
#     if {"email":""+email+""} in run_query(f"select email from users where type ='{type}'"):
#         return "email already exist",401
    
#     else:
#         # run_query("delete from users",True)
#         run_query(f"insert into users (id,name,email,phone_number,password,create_by,type) values ('{id}','{name}','{email}','{number}','{password}','admin','{type}')",True)
#         return "Success, User Created",200
        

    
# @sign_in_bp.route("", methods=["POST"])
# def sign_in():
# <<<<<<< HEAD
#     body = request.json
#     email = body["email"]
#     password = body["password"]
    
#     check = run_query(f"select email,password from users where email = '{email}' and password = '{password}'")
#     query = run_query(f"select name,email,phone_number,type from users where email = '{email}' and password = '{password}'")
#     id = run_query(f"select id from users where email = '{email}' and password = '{password}'")
    
#     if check == []:
#         return "email or password is incorrect",400
#     else:
#         return {
#         "user_information": [
#             query
#         ],
#         "token":[
#             id
#         ],
#         "message":[
#             "Login Success"   
#         ]
#     },200
# =======
#     # For example only
#     name = request.get_json()["name"]
#     user_id = run_query(select(Users.id).where(Users.name==name))[0]["id"]
#     token = encode_auth_token(user_id)
#     return success_message(200, data="Login success", key="message", tkn=token)
# >>>>>>> c96673e7b4a9de2abb77bd0ffb09e51588878abd

import uuid
from flask import request
from sqlalchemy import (
    update,
    delete,
    insert,
    select,
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)
from app.utils.query import run_query
from app.utils.format_datetime import format_datetime
from app.utils.auth_token import encode_auth_token
from app.utils.response import (
    error_message,
    success_message,
)
from app.models.user import Users
from . import sign_up_bp, sign_in_bp


@sign_up_bp.route("", methods=["POST"])
def sign_up():
    pass

@sign_in_bp.route("", methods=["POST"])
def sign_in():
    # For example only
    name = request.get_json()["name"]
    user_id = run_query(select(Users.id).where(Users.name==name))[0]["id"]
    token = encode_auth_token(user_id)
    return success_message(200, data="Login success", key="message", tkn=token)