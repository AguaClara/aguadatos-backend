from application.models import Plant, Configuration


# ensure that the Config model is working as expected
def test_config_model():
    """
    GIVEN a Configuration model
    WHEN a new Configuration is created
    THEN check the chemical_type, chemical_concentration, num_filters, and num_clarifiers fields are defined correctly
    """
    new_config = Configuration(
        chemical_type='PAC',
        chemical_concentration=0.5,
        num_filters=4,
        num_clarifiers=2)
    assert new_config.chemical_type == 'PAC'
    assert new_config.chemical_concentration == 0.5
    assert new_config.num_filters == 4
    assert new_config.num_clarifiers == 2

# ------------------------------------------------------------------------------------------

# ensure that the Plant model is working as expected
def test_plant_model():
    """
    GIVEN a Plant model
    WHEN a new Plant is created
    THEN check the name, phone-number, and config_id fields are defined correctly
    """
    new_plant = Plant(
        name='AguaClara',
        phone_number='123-456-7890',
        config_id=1)
    assert new_plant.name == 'AguaClara'
    assert new_plant.phone_number == '123-456-7890'
    assert new_plant.config_id == 1