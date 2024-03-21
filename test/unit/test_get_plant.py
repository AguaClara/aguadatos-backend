from utils_test import mismatch_error
 
def test_get_all_plants(test_client, init_database, validate_response):
    response = test_client.get('/api/plants/1')

    assert response.status_code == 200 
    assert response.content_type == "application/json"

    data = response.get_json() 

    expected_plant = {"config_id": 1, "id": 1, "name": "AguaClara", "phone_number": "111-111-1111"}

    assert 'id' in data, "ID not in response"

    # Check the plant attributes in the response
    for key in expected_plant:
        assert data[key] == expected_plant[key], mismatch_error("Response Output", expected_plant[key], data[key])