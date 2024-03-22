from utils_test import mismatch_error


def test_get_all_plants(test_client, init_database, validate_response):
    """
    GIVEN all plants in the database
    WHEN all plants are requested
    THEN return all plants
    """
    response = test_client.get('/api/plants/')

    assert response.status_code == 200 
    assert response.content_type == "application/json"

    data = response.get_json()
    assert 'plants' in data
    assert len(data['plants']) == 3

    expected_plants = [
        {"config_id": 1, "id": 1, "name": "AguaClara", "phone_number": "111-111-1111"},
        {"config_id": 2, "id": 2, "name": "AguaClara2", "phone_number": "222-222-2222"},
        {"config_id": 3, "id": 3, "name": "AguaClara3", "phone_number": "333-333-3333"}
    ]

    for expected, actual in zip(expected_plants, data['plants']):
        assert expected == actual, mismatch_error("Response Output", expected, actual)

# ------------------------------------------------------------------------------------------