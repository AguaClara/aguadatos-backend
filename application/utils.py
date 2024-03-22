from flask import jsonify
from sqlalchemy.inspection import inspect

# generalized serialization function
def serialize_model(model_instance):
    """
    Serialize a SQLAlchemy model instance into a dictionary.

    :param model_instance: The SQLAlchemy model instance to serialize.
    :return: A dictionary containing the model instance's attributes.
    """
    return {
        c.key: getattr(model_instance, c.key)
        for c in inspect(model_instance).mapper.column_attrs
    }

# generalized response formats 
def success_response(data, status=200):
    """
    Generalized success response function. 

    :param data: serialized data to be returned in the response
    :param status: status code of the response with default 200
    :return: JSON response with data and status code
    """
    return jsonify(data), status

def failure_response(message, status=400):
    """
    Generalized failure response function

    :param data: serialized data to be returned in the response
    :param status: status code of the response with default 200
    :return: JSON response with data and status code
    """
    return jsonify({"error": message}), status

# generalized body request unpacking 
def extract_fields(body, *fields):
    """
    Extract value of key-value pairs from a request body.
    
    :param body: request body
    :param fields: list of keys to extract from the body
    :return: list of values extracted from the body, otherwise list of missing fields
    """
    missing_fields = [field for field in fields if field not in body or body[field] is None]
    if missing_fields:
        return None, missing_fields
    return [body[field] for field in fields], None