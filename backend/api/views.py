import json
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from utils.utils_request import BAD_METHOD, request_failed, request_success, return_field
from utils.utils_require import CheckRequire, require
from models import *
from utils.utils_jwt import generate_jwt_token
# Create your views here.


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
    try:
        possible_user = User.object.get(userName=username)
        return request_failed(1, "Username already in use")
    except:
        try:
            possible_user = User.objects.get(email=email)
            return request_failed(2, "Email already in use")
        except:
            try:
                possible_user = User.objects.get(telephone=telephone)
                return request_failed(2, "Telephone already in use")
            except:
                newUser = User(userName=username, password="",
                               email=email, telephone=telephone)
                newUser.set_password(password)
                newUser.save()
                token = generate_jwt_token(username, email)
                return request_success({"token": token})
