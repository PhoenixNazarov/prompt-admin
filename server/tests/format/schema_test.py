from promptadmin.format.schema import Schema, ObjectSchema, ValueSchema


def test_from_string_value_string():
    string_format = """
    {"schema_type": "value", "value_type": "string"}
    """
    schema = Schema.from_json(string_format)
    assert isinstance(schema, ValueSchema)
    assert schema.value_type == "string"


def test_from_string_integer():
    string_format = """
    {"schema_type": "value", "value_type": "integer"}
    """
    schema = Schema.from_json(string_format)
    assert isinstance(schema, ValueSchema)
    assert schema.value_type == "integer"


def test_from_string_object():
    string_format = """
    {"schema_type": "value", "value_type": "object", "object_schema": {"schema_type": "object", "fields": []}}
    """
    schema = Schema.from_json(string_format)
    assert isinstance(schema, ValueSchema)
    assert isinstance(schema.object_schema, ObjectSchema)
    assert schema.object_schema.fields == []


def test_from_string_array():
    string_format = """
    {"schema_type": "value", "value_type": "object", "array": true, "object_schema": {"schema_type": "object", "fields": []}}
    """
    schema = Schema.from_json(string_format)
    assert isinstance(schema, ValueSchema)
    assert isinstance(schema.object_schema, ObjectSchema)
    assert schema.object_schema.fields == []
    assert schema.array


def test_from_string_field():
    dict_format = {
        'schema_type': 'value', 'value_type': 'object',
        'object_schema': {
            "schema_type": "object",
            "fields": [{
                "schema_type": "field",
                "name": "field1",
                "value_schema": {
                    'schema_type': 'value',
                    'value_type': 'string'
                }
            }]
        }
    }
    schema = Schema.from_dict(dict_format)
    assert isinstance(schema, ValueSchema)
    assert len(schema.object_schema.fields) == 1
    assert schema.object_schema.fields[0].name == 'field1'
    assert schema.object_schema.fields[0].value_schema.value_type == 'string'


def test_generate_from_obj_string():
    obj = 'qweqwe'
    schema = Schema.generate_from_obj(obj)
    assert isinstance(schema, ValueSchema)
    assert schema.value_type == 'string'
    assert not schema.array


def test_generate_from_obj_integer():
    obj = 123
    schema = Schema.generate_from_obj(obj)
    assert isinstance(schema, ValueSchema)
    assert schema.value_type == 'integer'
    assert not schema.array


def test_generate_from_obj_float():
    obj = 123.123
    schema = Schema.generate_from_obj(obj)
    assert isinstance(schema, ValueSchema)
    assert schema.value_type == 'float'
    assert not schema.array


def test_generate_from_obj_array():
    obj = [123.123]
    schema = Schema.generate_from_obj(obj)
    assert isinstance(schema, ValueSchema)
    assert schema.value_type == 'float'
    assert schema.array
