from flask import Flask, redirect, url_for, session, render_template, request
from flask_restful import Resource, Api
from models import box, users
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
app.secret_key = os.environ.get('SECRET_KEY')
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRETKEY")

api.add_resource(users.UserLogin, "/autenticar")
api.add_resource(users.CreateUser, "/criar")
api.add_resource(users.TwoFactorLogin, "/codigo")

if __name__ == "__main__":
    app.run(debug=True)
