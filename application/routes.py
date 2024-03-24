from flask import request
from flask import current_app as app
from .models import db, ChemicalTypes, TankLabels, Plant, Configuration, User
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from .utils import extract_fields, serialize_model, success_response, failure_response

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
        return failure_response(f"Plant missing {', '.join(missing_fields)}", 404)
    name, phone_number, chemical_type, chemical_concentration, num_filters, num_clarifiers = extracted_fields

    if chemical_type not in ChemicalTypes:
        return failure_response(f"Chemical '{chemical_type}' invalid.", 400)

    # handles uniqueness constraints
    # duplicate plants can appear as Plants that have the same name or the same number
    existing_name = existing_number = Plant.query.filter(or_(Plant.name == name, Plant.phone_number == phone_number)).first() 
    if existing_name is not None:
        if existing_name.name == body["name"]:
            return failure_response(f"Plant '{name}' already exists", 409)
        if existing_number.phone_number == body["phone_number"]:
            return failure_response(f"Phone number '{phone_number}' already exists.", 409)
    try: 
        new_config = Configuration(
            chemical_type=chemical_type,
            chemical_concentration=chemical_concentration,
            num_filters=num_filters,
            num_clarifiers=num_clarifiers)
        db.session.add(new_config)
        db.session.flush() # in event, new_plant fails, do not keep the new_config entry

        new_plant = Plant(
            name=name,
            phone_number=phone_number, 
            config_id=new_config.id)
        db.session.add(new_plant)
        db.session.commit()
        
        serialized_plant = serialize_model(new_plant)
        serialized_plant['config_id'] = serialize_model(new_config)
        return success_response(serialized_plant, 201)
        # return success_response(serialized_plant, 201, headers={"Location": f"/api/plants/{new_plant.id}"})
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return failure_response("Internal Server Error", 500)
    
@app.route("/api/plants/<int:plant_id>/", methods=["GET"])
def get_plant(plant_id):
    """
    Endpoint for getting a specific plant
    """
    plant = Plant.query.filter_by(id=plant_id).first()
    if plant is None:
        return failure_response("Plant not found.", 404)
    serialized_plant = serialize_model(plant)
    return success_response(serialized_plant)

@app.route("/api/plants/", methods=["GET"])
def get_all_plants():
    """
    Endpoint for getting all plants
    """
    return success_response({"plants": [serialize_model(p) for p in Plant.query.all()]})

# -- USER ROUTES ------------------------------------------------------
@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a user

    Eventually we will have Google Authentication
    """
    body = request.json
    required_fields = [
    "name",
    "email",
    "phone_number",
    "plant_name"
    ]

     # extracted_fields returns extracted_fields and any missing_fields if there are any
    extracted_fields, missing_fields = extract_fields(body, *required_fields)
    if missing_fields:
        return failure_response(f"User missing {', '.join(missing_fields)}", 404)
    # unpacks extracted_fields into individual variables 
    name, email, phone_number, plant_name = extracted_fields

    # handles uniqueness constraints
    # duplicate users can appear as Users that have the same email or number
    existing_email = existing_number = User.query.filter(or_(User.email == email, User.phone_number == phone_number)).first() 
    if existing_email is not None:
        if existing_email.email == body["email"]:
            return failure_response(f"User '{email}' already in use.", 409)
        if existing_number.phone_number == body["phone_number"]:
            return failure_response(f"User Phone number '{phone_number}' already in use.", 409)
        
    # to get associated Plant ID
    plant = Plant.query.filter_by(name=plant_name).first()
    if plant is None:
        return failure_response(f"Plant named {plant_name} not found.", 404)
    try: 
        new_user = User(
            name=name, 
            email=email, 
            phone_number=phone_number, 
            plant_id=plant.id)
        db.session.add(new_user)
        db.session.commit()

        serialized_user = serialize_model(new_user)
        serialized_user['plant_id'] = serialize_model(plant)
        return success_response(serialized_user, 201)
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return failure_response("Internal Server Error", 500)

@app.route("/api/users/<int:user_id>/")
def get_specific_user(user_id):
    """
    Endpoint for getting user by id 
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!", 404)
    serialized_user = serialize_model(user)
    return success_response(serialized_user)

@app.route("/api/users/")
def get_all_users():
    """
    Endpoint for getting all users
    """
    return success_response({"users": [serialize_model(u) for u in User.query.all()]})

# get all users for a plant 

@app.route("/api/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    Endpoint for deleting a user by id
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!", 404)
    db.session.delete(user)
    db.session.commit()
    serialized_user = serialize_model(user)
    return success_response(serialized_user)

@app.route("/api/plants/<int:plant_id>/", methods=["DELETE"])
def delete_plant(plant_id):
    """
    Endpoint for deleting a plant by id

    Must also delete associated Configuration and Users/Plant Operators
    """
    plant = Plant.query.filter_by(id=plant_id).first()
    if plant is None:
        return failure_response("Plant not found!", 404)

    # delete users associated with plant 
    associated_users = User.query.filter_by(plant_name=plant.name)
    for u in associated_users:
        db.session.delete(u)
        db.session.commit()

    db.session.delete(plant)
    db.session.commit()

    # delete config associated with plant 
    associated_config = Configuration.query.filter_by(id=plant.config_id)
    db.session.delete(associated_config)
    db.session.commit()
    serialized_plant = serialize_model(plant)
    return success_response(serialized_plant)