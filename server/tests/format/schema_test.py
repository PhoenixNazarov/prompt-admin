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
    {"schema_type": "value", "value_type": "object", "object_schema": {"schema_type": "object", "fields": {}}}
    """
    schema = Schema.from_json(string_format)
    assert isinstance(schema, ValueSchema)
    assert isinstance(schema.object_schema, ObjectSchema)
    assert schema.object_schema.fields == {}


def test_from_string_array():
    string_format = """
    {"schema_type": "value", "value_type": "object", "array": true, "object_schema": {"schema_type": "object", "fields": {}}}
    """
    schema = Schema.from_json(string_format)
    assert isinstance(schema, ValueSchema)
    assert isinstance(schema.object_schema, ObjectSchema)
    assert schema.object_schema.fields == {}
    assert schema.array


def test_from_string_field():
    dict_format = {
        'schema_type': 'value',
        'value_type': 'object',
        'object_schema': {
            "schema_type": "object",
            "fields": {
                "field1": {
                    'schema_type': 'value',
                    'value_type': 'string'
                }
            }
        }
    }
    schema = Schema.from_dict(dict_format)
    assert isinstance(schema, ValueSchema)
    assert len(schema.object_schema.fields) == 1
    assert schema.object_schema.fields['field1']
    assert schema.object_schema.fields['field1'].value_type == 'string'


def test_generate_from_obj_string():
    obj = 'qweqwe'
    schema = Schema.generate_from_obj(obj)
    assert isinstance(schema, ValueSchema)
    assert schema.value_type == 'string'
    assert not schema.array
    schema.validate('qweewqeqkwneqlkwen')


def test_generate_from_obj_integer():
    obj = 123
    schema = Schema.generate_from_obj(obj)
    assert isinstance(schema, ValueSchema)
    assert schema.value_type == 'integer'
    assert not schema.array
    schema.validate('12398123')


def test_generate_from_obj_float():
    obj = 123.123
    schema = Schema.generate_from_obj(obj)
    assert isinstance(schema, ValueSchema)
    assert schema.value_type == 'float'
    assert not schema.array
    schema.validate('123.3213')
    schema.validate('123')


def test_generate_from_obj_array():
    obj = [123.123]
    schema = Schema.generate_from_obj(obj)
    assert isinstance(schema, ValueSchema)
    assert schema.value_type == 'float'
    assert schema.array
    assert schema.validate('[98123.12312, 123012.123]')


def test_generate_from_obj_dict():
    obj = {
        'recommendation': {
            'text': 'Hello',
            'text2': 'Hello2'
        }
    }
    schema = Schema.generate_from_obj(obj)
    assert schema.validate(
        """
        {"recommendation":{"text": "Hello213", "text2": "Hello2123"}}
        """
    )


def test_make_example():
    obj = {
        'result':
            {'recommendation':
                [
                    {
                        "category_id": 123,
                        "importance": 100,
                        "relevance": "[based on my answers, explain relevance of this category to me to make we want to focus on "
                                     "it. refer to my answers. up to 50 words]",
                    }
                ]
            }
    }
    schema = Schema.generate_from_obj(obj)

    assert schema.make_example_obj() == {'result': {
        'recommendation': [{'category_id': 1, 'importance': 1, 'relevance': 'test'},
                           {'category_id': 1, 'importance': 1, 'relevance': 'test'}]}}

    assert schema.make_example_json() == """
    {"result": {"recommendation": [{"category_id": 1, "importance": 1, "relevance": "test"}, {"category_id": 1, "importance": 1, "relevance": "test"}]}}
    """.strip()

    assert schema.make_example_xml() == """
    <result><recommendation><category_id>1</category_id><importance>1</importance><relevance>test</relevance></recommendation><recommendation><category_id>1</category_id><importance>1</importance><relevance>test</relevance></recommendation></result>
    """.strip()


def test_casting_type():
    obj = {
        'id': '123'
    }

    schema = Schema.generate_from_obj(obj)
    assert schema.to_dict() == {'value_type': 'object',
                                'object_schema': {'fields': {'id': {'value_type': 'integer', 'schema_type': 'value'}},
                                                  'schema_type': 'object'}, 'schema_type': 'value'}


def test_casting_type_2():
    obj = {
        'id': '123.0'
    }

    schema = Schema.generate_from_obj(obj)
    assert schema.to_dict() == {'value_type': 'object',
                                'object_schema': {'fields': {'id': {'value_type': 'float', 'schema_type': 'value'}},
                                                  'schema_type': 'object'}, 'schema_type': 'value'}


def test_casting_type_3():
    obj = {
        'id': 123
    }

    schema = Schema.generate_from_obj(obj)
    assert schema.to_dict() == {'value_type': 'object',
                                'object_schema': {'fields': {'id': {'value_type': 'integer', 'schema_type': 'value'}},
                                                  'schema_type': 'object'}, 'schema_type': 'value'}


def test_good_format():
    obj = {
        'result':
            {
                'recommendation':
                    [
                        {
                            "category_id": 123,
                            "importance": 100,
                            "relevance": "[based on my answers, explain relevance of this category to me to make we want to focus on "
                                         "it. refer to my answers. up to 50 words]",
                        }
                    ]
            }
    }
    schema = Schema.generate_from_obj(obj)
    schema_dict = schema.to_dict()

    example_obj = schema.make_example_obj()
    example_json = schema.make_example_json()
    example_xml = schema.make_example_xml()

    assert Schema.generate_from_obj(example_obj).to_dict() == schema_dict
    assert Schema.generate_from_json(example_json).to_dict() == schema_dict
    assert Schema.generate_from_xml(example_xml).to_dict() == schema_dict


def test_good_format_builtin():
    obj = {
        'result':
            {
                'recommendation':
                    [
                        {
                            "category_id": 123,
                            "importance": 100,
                            "relevance": "[based on my answers, explain relevance of this category to me to make we want to focus on "
                                         "it. refer to my answers. up to 50 words]",
                        }
                    ]
            }
    }
    schema = Schema.generate_from_obj(obj)

    report = schema.get_consistent_format_report()

    assert report.to_dict

    assert report.make_example_obj
    assert report.make_example_obj_converse
    assert report.make_example_obj_converse_equal

    assert report.make_example_json
    assert report.make_example_json_converse
    assert report.make_example_json_converse_equal

    assert report.make_example_xml
    assert report.make_example_xml_converse
    assert report.make_example_xml_converse_equal
