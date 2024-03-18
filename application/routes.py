import json
from flask import request, jsonify
from flask import current_app as app
from .models import db, ChemicalTypes, TankLabels, Plants, Configurations, Users
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from sqlalchemy.inspection import inspect

# generalized serialization function
def serialize_model(model_instance):
    return {
        c.key: getattr(model_instance, c.key)
        for c in inspect(model_instance).mapper.column_attrs
    }

# generalized response formats 
def success_response(data, status=200):
    """
    Generalized success response function
    """
    return jsonify(data), status

def failure_response(message, status=400):
    """
    Generalized failure response function
    """
    return jsonify({"error": message}), status

# generalized body request unpacking 
def extract_fields(body, *fields):
    missing_fields = [field for field in fields if field not in body or body[field] is None]
    if missing_fields:
        return None, missing_fields
    return [body[field] for field in fields], None

# -- PLANT ROUTES ------------------------------------------------------
@app.route("/api/plants/", methods=["POST"])
def create_plant():
    """
    Endpoint for creating a plant
    """
    body = request.json
    required_fields = [
    "name",
    "phone_number",
    "chemical_type",
    "chemical_concentration",
    "num_filters",
    "num_clarifiers"
    ]

    extracted_fields, missing_fields = extract_fields(body, *required_fields)
    if missing_fields:
        return failure_response(f"Plant missing {', '.join(missing_fields)}", 400)
    name, phone_number, chemical_type, chemical_concentration, num_filters, num_clarifiers = extracted_fields

    if chemical_type not in ChemicalTypes:
        return failure_response(f"Chemical '{chemical_type}' invalid", 400)

    # handles uniqueness constraints
    existing_plant = existing_plant = Plants.query.filter(or_(Plants.name == name, Plants.phone_number == phone_number)).first() 
    if existing_plant is not None:
        if existing_plant.name == body["name"]:
            return failure_response(f"Plant '{name}' already exists", 400)
        if existing_plant.phone_number == body["phone_number"]:
            return failure_response(f"Phone number '{phone_number}' already exists", 400)
    try: 
        new_config = Configurations(
            chemical_type=chemical_type,
            chemical_concentration=chemical_concentration,
            num_filters=num_filters,
            num_clarifiers=num_clarifiers)
        db.session.add(new_config)
        db.session.flush() # in event, new_plant fails, do not keep the new_config entry

        new_plant = Plants(
            name=name,
            phone_number=phone_number, 
            config_id=new_config.id)
        db.session.add(new_plant)
        db.session.commit()
        
        serialized_plant = serialize_model(new_plant)
        serialized_plant['config'] = serialize_model(new_config)
        return success_response(serialized_plant, 201)
        # return success_response(serialized_plant, 201, headers={"Location": f"/api/plants/{new_plant.id}"})
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return failure_response("Internal Server Error", 500)

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
