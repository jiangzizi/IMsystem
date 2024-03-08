import json
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from utils.utils_request import BAD_METHOD, request_failed, request_success, return_field
from utils.utils_require import CheckRequire, require
from .models import *
from utils.utils_jwt import generate_jwt_token,check_jwt_token
from django.db.models import Q
# Create your views here.

@CheckRequire
def register(req: HttpRequest):
    if req.method != "POST":
        return BAD_METHOD
    """ Request body example:
    {
        "userName": "Ashitemaru",
        "password": "123456",
        "email": "example@gmail.com",
        "telephone": "1234567890",
        "image": ["TODO"]
    }"""
    
    body = json.loads(req.body.decode("utf-8"))
    username = require(body, "userName", "string",
                       err_msg="Missing or error type of [userName]")
    password = require(body, "password", "string",
                       err_msg="Missing or error type of [password]")
    email = require(body, "email", "string",
                    err_msg="Missing or error type of [email]")
    telephone = require(body, "telephone", "telephone",
                        err_msg="Missing or error type of [telephone]")

    duplicate_user = User.objects.filter(Q(name=username) | Q(
        email=email) | Q(telephone=telephone)).first()
    if duplicate_user:
        if duplicate_user.name == username:
            return request_failed(1, "Username already in use",409)
        elif duplicate_user.email == email:
            return request_failed(2, "Email already in use",409)
        elif duplicate_user.telephone == telephone:
            return request_failed(2, "Telephone already in use",409)

    newUser = User( name=username, password="",
                   email=email, telephone=telephone)
    newUser.set_password(password)
    newUser.save()
    token = generate_jwt_token(username, email,telephone)
    return request_success({"token": token})
@CheckRequire
def login(req:HttpRequest):
    if req.method!="POST":
        return BAD_METHOD
    body = json.loads(req.body.decode("utf-8"))
    
    username = require(body, "userName", "string", err_msg="Missing or error type of [userName]")
    password = require(body, "password", "string", err_msg="Missing or error type of [password]")
    try :
        possible_user=User.objects.get(name=username)
        if(possible_user.check_password(password)):
            email=possible_user.email
            telephone=possible_user.telephone
            return request_success({"token":generate_jwt_token(username,email,telephone)})
        else:
            return request_failed(2,"Wrong password",401)
    except:
        return request_failed(1, "User not found",401)
@CheckRequire
def delete_account(req:HttpRequest):
    if req.method!="POST":
        return BAD_METHOD
    body = json.loads(req.body.decode("utf-8"))
    jwt_token = req.headers.get("Authorization")
    if check_jwt_token(jwt_token) ==None:
        return request_failed(2, "Invalid or expired JWT", 401)
    username=check_jwt_token(jwt_token)["username"]
    try:
        possible_user=User.objects.get(name=username)
        possible_user.delete()
        return request_success()
    except:
        return request_failed(2, "Invalid or expired JWT", 401)

@CheckRequire
def setting(req:HttpRequest):
    if req.method!="POST":
        return BAD_METHOD
    jwt_token = req.headers.get("Authorization")
    if check_jwt_token(jwt_token) ==None:
        return request_failed(2, "Invalid or expired JWT", 401)
    #return request_success({"data"})
    body = json.loads(req.body.decode("utf-8"))
    username = require(body, "userName", "string",
                       err_msg="Missing or error type of [userName]")
    password = require(body, "password", "string",
                       err_msg="Missing or error type of [password]")
    email = require(body, "email", "string",
                    err_msg="Missing or error type of [email]")
    telephone = require(body, "telephone", "telephone",
                        err_msg="Missing or error type of [telephone]")
    old_name=check_jwt_token(jwt_token)["username"]
    old_email=check_jwt_token(jwt_token)["email"]
    old_telephone=check_jwt_token(jwt_token)["telephone"]


    duplicate_user = User.objects.filter(Q(name=username) | Q(
        email=email) | Q(telephone=telephone)).first()
    
    if duplicate_user:
        if duplicate_user.name == username and username != old_name:
            return request_failed(6, f"Username already in use {username}: {old_name}",409)
        elif duplicate_user.email == email and email!= old_email:
            return request_failed(6, "Email already in use",409)
        elif duplicate_user.telephone == telephone and telephone!= old_telephone:
            return request_failed(6, "Telephone already in use",409)
    
    user=User.objects.get(name=old_name)
    user.name=username
    user.set_password(password)
    user.email=email
    user.telephone=telephone
    user.save()
    token = generate_jwt_token(username, email,telephone)
    return request_success({"token": token})
@CheckRequire
def find_user(req:HttpRequest):
    if req.method!="GET":
        return BAD_METHOD
    params=req.GET
    userName=params.get("userName")
    if len(userName)==0:
        return request_failed(1,"Need username",400)
    try:
        possible_user=User.objects.get(name=userName)
        data={"userName":possible_user.name,"email":possible_user.email,"telephone":possible_user.telephone}
        json_data={"user":data}
        return request_success(json_data)
    except:
        return request_failed(2,"No such user", 404)
    
    
    
