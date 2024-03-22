from application.models import Plant, Configuration
from utils_test import mismatch_error

direct_attributes = ['name', 'phone_number']
config_attributes = ['chemical_type', 'chemical_concentration', 'num_filters', 'num_clarifiers']

# unit test for creating a new plant
def test_create_plant(test_client, init_database, validate_response): 
    """
    GIVEN a new plant information
    WHEN a new plant is created
    THEN valid response is returned, response's information is correct and written to the database
    """
    new_plant = {
        "name": "AguaClara4",
        "phone_number": "444-444-4444",
        "chemical_type": "PAC",
        "chemical_concentration": 0.4,
        "num_filters": 4,
        "num_clarifiers": 4
    }
    
    response = test_client.post('/api/plants/', json=new_plant)
    validate_response(response, 201, "application/json")

    data = response.get_json()
    assert 'id' in data, "ID not in response"

    # Check the plant attributes in the response
    for key in direct_attributes:
        assert data[key] == new_plant[key], mismatch_error("Response Output", new_plant[key], data[key])

    # Check the configuration attributes in the response
    assert 'config' in data, "Config not in response"
    for key in config_attributes:
        assert data['config'][key] == new_plant[key], mismatch_error("Response Output", new_plant[key], data['config'][key])

    # Check if new plant is written to the database correctly
    created_plant = Plant.query.get(data['id'])
    assert created_plant is not None, "Plant not created in the database"
    for attribute in direct_attributes:
        assert getattr(created_plant, attribute) == new_plant[attribute], mismatch_error("Written Output", new_plant[attribute], getattr(created_plant, attribute))

    created_config = Configuration.query.get(created_plant.config_id)
    assert created_config is not None, "Configuration not created in the database"
    for attribute in config_attributes:
        assert getattr(created_config, attribute) == new_plant[attribute], mismatch_error("Written Output", new_plant[attribute], getattr(created_config, attribute))


