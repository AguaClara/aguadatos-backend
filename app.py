import json 

from db import db
from db import User, Plant, Configuration, DosageEntry, CalibrationSection, ChangeDoseSection, RawWaterEntry

import datetime
import random

from flask import Flask
from flask import request 

import os

# Third-party libraries
from flask import Flask, redirect, request, url_for

# google libraries
# from google.oauth2 import id_token
# from google.auth.transport import requests
# import requests

# define db filename 
db_filename = "aguadatos.db"
app = Flask(__name__)

# setup config 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

# initialize app
db.init_app(app)
with app.app_context():
    db.create_all()

# generalized response formats 
def success_response(data, code=200):
    """
    Generalized success response function
    """
    return json.dumps(data), code

def failure_response(message, code=404):
    """
    Generalized failure response function
    """
    return json.dumps({"error": message}), code

# -- GOOGLE ROUTES ------------------------------------------------------
# @app.route("/api/login/", methods=["POST"])
# def login():
#     """
#     Endpoint for logging a user in with Google and registering new users
#     """
#     data = json.loads(request.data)
#     token = data.get("token")
#     try:
        
#         id_info = id_token.verify_oauth2_token(token, requests.Request(), os.environ.get("CLIENT_ID"))
#         email, first_name, last_name = id_info["email"], id_info["given_name"], id_info["family_name"]
#         name = first_name + " " + last_name
        
#         user = User.query.filter_by(email=email).first()

#         if user is None:
#             # create user and session
#             user = User(email=email, name=name)
#             db.session.add(user)
#             db.session.commit()

#         return success_response(user.serialize())
#         # return session serialize
#     except ValueError:
#         raise Exception("Invalid Token")

# @app.route("/api/users/<int:user_id>/phone/", methods=["POST"])
# def add_number(user_id):
#     """
#     Endpoint for adding phone number to user
#     """
#     body = json.loads(request.data)
#     number = body.get("number")
#     if number is None:
#         return failure_response("Please input a phone number", 400)
#     user = User.query.filter_by(id=user_id).first()
#     if user is None:
#         return failure_response("User not found", 404)
#     user.number = number
#     db.session.commit()
#     return success_response(user.serialize())

# -- PLANT ROUTES ------------------------------------------------------
@app.route("/api/plants/", methods=["POST"])
def create_plant():
    """
    Endpoint for creating a plant

    """
    body = json.loads(request.data)
    name = body.get("name")
    phone_number = body.get("phone_number")
    chemical_type = body.get("chemical_type")
    chemical_concentration = body.get("chemical_concentration")
    num_filters = body.get("num_filters")
    num_clarifiers = body.get("num_clarifiers")
    if name is None:
        return failure_response("Please enter something for name", 400)
    if phone_number is None:
        return failure_response("Please enter something for phone number", 400)
    if chemical_type is None:
        return failure_response("Please enter something for chemical type", 400)
    if chemical_concentration is None:
        return failure_response("Please enter something for chemical concentration", 400)
    if num_filters is None:
        return failure_response("Please enter something for the number of filters", 400)
    if num_clarifiers is None:
        return failure_response("Please enter something for the number of clarifiers", 400)
    
    new_config = Configuration(chemical_type=chemical_type, chemical_concentration=chemical_concentration, num_filters=num_filters, num_clarifiers=num_clarifiers)
    db.session.add(new_config)
    db.session.commit()
    new_plant = Plant(name=name, phone_number=phone_number, config_id=new_config.id)
    db.session.add(new_plant)
    db.session.commit()
    return success_response(new_plant, 201)

# -- USER ROUTES ------------------------------------------------------
@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a user

    Eventually we will have Google Authentication
    """
    body = json.loads(request.data)
    name = body.get("name")
    email = body.get("email")
    phone_number = body.get("phone_number")
    if name is None:
        return failure_response("Please enter something for name", 400)
    if email is None:
        return failure_response("Please enter something for email", 400)
    if phone_number is None:
        return failure_response("Please enter something for phone number", 400)
    new_user = User(name=name, email=email, phone_number=phone_number)
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user, 201)

@app.route("/api/users/<int:user_id>/")
def get_specific_user(user_id):
    """
    Endpoint for getting user by id 
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    return success_response(user)

@app.route("/api/users/")
def get_all_users():
    """
    Endpoint for getting all users
    """
    # return success_response({"events": [e.serialize() for e in Event.query.order_by(Event.date.desc())]})
    return success_response({"users": [user for user in User.query.all()]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)