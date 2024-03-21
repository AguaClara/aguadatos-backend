from flask import jsonify
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