import json
from flask import request
from flask import current_app as app
from .models import db, Plant, Configuration, User

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
    return success_response(new_plant.serialize(), 201)

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
    plant_name = body.get("plant_name")
    if name is None:
        return failure_response("Please enter something for name", 400)
    if email is None:
        return failure_response("Please enter something for email", 400)
    if phone_number is None:
        return failure_response("Please enter something for phone number", 400)
    if plant_name is None:
        return failure_response("Please choose the associated plant", 400)
    
    plant = Plant.query.filter_by(name=plant_name).first()
    if plant is None:
        return failure_response("Plant not found")
    new_user = User(name=name, email=email, phone_number=phone_number, plant_id=plant.id)
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)

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