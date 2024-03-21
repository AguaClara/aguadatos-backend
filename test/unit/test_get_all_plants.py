# from utils_test import mismatch_error

# def test_get_all_plants(test_client, init_database, validate_response):
#     response = test_client.get('/api/plants/')

#     assert response.status_code == 200 
#     assert response.content_type == "application/json"

#     data = response.get_json()
#     assert 'plants' in data
#     assert len(data['plants']) == 3

#     expected_plants = [
#         {"config_id": 1, "id": 1, "name": "AguaClara", "phone_number": "111-111-1111"},
#         {"config_id": 2, "id": 2, "name": "AguaClara2", "phone_number": "222-222-2222"},
#         {"config_id": 3, "id": 3, "name": "AguaClara3", "phone_number": "333-333-3333"}
#     ]

#     for expected, actual in zip(expected_plants, data['plants']):
#         assert expected['id'] == actual['id']
#         assert expected['config_id'] == actual['config_id']
#         assert expected['name'] == actual['name']
#         assert expected['phone_number'] == actual['phone_number']