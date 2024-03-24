"""
This module contains fixtures that are used by the test modules in the test directory.

Utilize "python3 -m pytest -vclear -s --setup-show" to initialize the test environment and run the tests.
"""
import os
import pytest
from application import create_app, db
from application.models import User, Plant, Configuration


# generalized status code and content type assert
@pytest.fixture(scope='module')
def validate_response():
    def _validate(response, status_code, content_type):
        """
        Validates the status code and content type of a response.

        :param response: The response object to validate.
        :param status_code: The expected status code.
        :param content_type: The expected content type.
        """
        assert response.status_code == status_code, f'Expected status code {status_code}, but got {response.status_code} instead.'
        assert response.content_type == content_type, f'Expected content type {content_type}, but got {response.content_type} instead.'
    return _validate


@pytest.fixture(scope='session')
def test_client():
    # Set the Testing configuration prior to creating the Flask application
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='module')
def init_database(test_client):
    db.create_all()

    first_config = Configuration(id=1, chemical_type='PAC', chemical_concentration=0.1, num_filters=1, num_clarifiers=1)
    second_config = Configuration(id=2, chemical_type='PAC', chemical_concentration=0.2, num_filters=2, num_clarifiers=2)
    third_config = Configuration(id=3, chemical_type='PAC', chemical_concentration=0.3, num_filters=3, num_clarifiers=3)
    db.session.add(first_config)
    db.session.add(second_config)
    db.session.add(third_config)   
    db.session.commit()

    first_plant = Plant(id=1, name='AguaClara', phone_number='111-111-1111', config_id=1)
    second_plant = Plant(id=2, name='AguaClara2', phone_number='222-222-2222', config_id=2)
    third_plant = Plant(id=3, name='AguaClara3', phone_number='333-333-3333', config_id=3)
    db.session.add(first_plant)
    db.session.add(second_plant)
    db.session.add(third_plant)
    db.session.commit()

    first_user = User(name='John Doe', email='email@email.com', phone_number='123-456-789', plant_id=1)
    second_user = User(name='Jane Smith', email='jane@email.com', phone_number='987-654-321', plant_id=2)
    third_user = User(name='Bob Johnson', email='bob@example.com', phone_number='555-555-555', plant_id=3)
    db.session.add(first_user)
    db.session.add(second_user)
    db.session.add(third_user)
    db.session.commit()

    yield db  # this is where the testing happens!

    db.session.remove()
    db.drop_all()





