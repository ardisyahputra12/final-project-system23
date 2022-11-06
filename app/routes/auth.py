import uuid
from flask import request
from sqlalchemy import (
    update,
    delete,
    insert,
    select,
)
from utils import (
    run_query,
    error_message,
    success_message,
    format_datetime,
)
from models.user import Users
from . import sign_up_bp, sign_in_bp


@sign_up_bp.route("", methods=["POST"])
def sign_up():
    body = request.json
    id = uuid.uuid4()
    name = body["name"]
    email = body["email"]
    number = body["number"]
    password = body["password"]
    type = body["type"]
    
    #for testing only
    if {"email":""+email+""} in run_query(f"select email from users where type ='{type}'"):
        return "email already exist",401
    
    else:
        # run_query("delete from users",True)
        run_query(f"insert into users (id,name,email,phone_number,password,create_by,type) values ('{id}','{name}','{email}','{number}','{password}','admin','{type}')",True)
        return "Success, User Created",200
        

    
@sign_in_bp.route("", methods=["POST"])
def sign_in():
    body = request.json
    email = body["email"]
    password = body["password"]
    
    check = run_query(f"select email,password from users where email = '{email}' and password = '{password}'")
    query = run_query(f"select name,email,phone_number,type from users where email = '{email}' and password = '{password}'")
    id = run_query(f"select id from users where email = '{email}' and password = '{password}'")
    
    if check == []:
        return "email or password is incorrect",400
    else:
        return {
        "user_information": [
            query
        ],
        "token":[
            id
        ],
        "message":[
            "Login Success"   
        ]
    },200