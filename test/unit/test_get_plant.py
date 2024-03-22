from utils_test import mismatch_error
 

def test_get_plant_1(test_client, init_database, validate_response):
    """
    GIVEN a plant ID
    WHEN a plant is requested by ID
    THEN return the plant information
    """
    response = test_client.get('/api/plants/1/')
    validate_response(response, 200, "application/json")
    data = response.get_json() 
    expected_plant = {"config_id": 1, "id": 1, "name": "AguaClara", "phone_number": "111-111-1111"}
    assert 'id' in data, "ID not in response"
    for key in expected_plant:
        assert data[key] == expected_plant[key], mismatch_error("Response Output", expected_plant[key], data[key])

# ------------------------------------------------------------------------------------------

def test_get_plant_4(test_client, init_database, validate_response):
    """
    GIVEN a plant ID that does not exist
    WHEN a plant is requested by ID
    THEN return a 400 error
    """
    response = test_client.get('/api/plants/4/')
    assert response.status_code == 400


