from symbiosis_api_client.model_list_adapter import BaseModel, list_adapter


def test_model_list_adapter():

    class TestModel(BaseModel):
        id: int
        name: str
        value: float

    data = [
        {"id": 1, "name": "Test1", "value": 10.5},
        {"id": 2, "name": "Test2", "value": 20.0},
    ]
    validated_data = list_adapter(data, TestModel)
    assert isinstance(validated_data, list)
    assert len(validated_data) == 2
    assert validated_data[0].id == 1
    assert validated_data[0].name == "Test1"
    assert validated_data[0].value == 10.5
