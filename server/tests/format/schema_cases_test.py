import pytest

from pydantic import BaseModel

from promptadmin_server.format.errors import CantValidateValue
from promptadmin_server.format.schema import Schema


class SchemaTestCase(BaseModel):
    dict_schema: dict
    generated_from_obj: dict | list
    valid_obj: list
    invalid_obj: list


cases = [
    SchemaTestCase(
        dict_schema={'value_type': 'object',
                     'object_schema': {'fields': {'id': {'value_type': 'integer', 'schema_type': 'value'}},
                                       'schema_type': 'object'}, 'schema_type': 'value'},
        generated_from_obj={"id": 123},
        valid_obj=[
            ({'id': 1}, {'id': 1}),
            ({'id': 14124}, {'id': 14124}),
            ({'id': '14124'}, {'id': 14124}),
            ({'id': 14124.1232}, {'id': 14124}),
        ],
        invalid_obj=[
            'asdasd',
            {'id': '123.123'},
            {'id': 123, 'qwe': 123},
            [123, 123]
        ]
    ),
    SchemaTestCase(
        dict_schema={
            'value_type': 'object', 'object_schema': {
                'fields': {'id': {'value_type': 'object',
                                  'object_schema': {'fields': {
                                      'qwe': {'value_type': 'integer',
                                              'schema_type': 'value'},
                                      'kjwqeh': {'value_type': 'integer',
                                                 'schema_type': 'value'}},
                                      'schema_type': 'object'},
                                  'schema_type': 'value'}},
                'schema_type': 'object'}, 'schema_type': 'value'},
        generated_from_obj={"id": {'qwe': 123, 'kjwqeh': 44312}},
        valid_obj=[
            ({"id": {'qwe': 321, 'kjwqeh': 124214}}, {"id": {'qwe': 321, 'kjwqeh': 124214}}),
            ({"id": {'qwe': 55, 'kjwqeh': '1242141'}}, {"id": {'qwe': 55, 'kjwqeh': 1242141}}),
        ],
        invalid_obj=[
            {'id': 123},
            {"id": {'qwe': 123, 'kjwqeh1': 44312}},
        ],
    ),
    SchemaTestCase(
        dict_schema={'value_type': 'integer', 'array': True, 'schema_type': 'value'},
        generated_from_obj=[123123, 123123, 123],
        valid_obj=[
            ([1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]),
            ([1, 1, 1, 1, 1, 1, 1, 2, 1], [1, 1, 1, 1, 1, 1, 1, 2, 1]),
            ([1, 1, 1, 1, 1, 5, 1, 2, 1], [1, 1, 1, 1, 1, 5, 1, 2, 1]),
            (['1', 1, 1, 1, 1, '5', 1, 2, 1], [1, 1, 1, 1, 1, 5, 1, 2, 1]),
        ],
        invalid_obj=[
            123, 'qwe',
            ['123', 'qwe'],
            [{'123': '123'}]
        ],
    ),
    SchemaTestCase(
        dict_schema={'value_type': 'object',
                     'object_schema': {'fields': {'test1': {'value_type': 'string', 'schema_type': 'value'}},
                                       'schema_type': 'object'}, 'array': True, 'schema_type': 'value'},
        generated_from_obj=[{'test1': '123qwe123'}, {'test1': '123'}],
        valid_obj=[
            ([{'test1': '1'}, {'test1': '2'}], [{'test1': '1'}, {'test1': '2'}]),
            ([{'test1': '1'}, {'test1': 'qwe'}], [{'test1': '1'}, {'test1': 'qwe'}])
        ],
        invalid_obj=[
            [{'test1': '1'}, {'test1': '2', 'test3': '123'}],
            [{'test1': '1'}, {'test1': '2', 'qwe': 123}],
            [{'test1': '1'}, {'test1': '2qwe', 'q': 'q'}],
            [{'test1': '1'}, {'test2': '2qwe'}]
        ],
    ),
]


@pytest.mark.parametrize(
    'schema_input,schema_output',
    [(case.generated_from_obj, case.dict_schema) for case in cases]
)
def test_generate_from_obj_cases(schema_input, schema_output):
    assert Schema.generate_from_obj(schema_input).to_dict() == schema_output


@pytest.mark.parametrize(
    'schema,obj,validated',
    [(case.dict_schema, valid_obj[0], valid_obj[1]) for case in cases for valid_obj in case.valid_obj]
)
def test_validate_obj_cases_valid(schema, obj, validated):
    assert Schema.from_dict(schema).validate_obj(obj) == validated


@pytest.mark.parametrize(
    'schema,obj',
    [(case.dict_schema, invalid_obj) for case in cases for invalid_obj in case.invalid_obj]
)
def test_validate_obj_cases_invalid(schema, obj):
    with pytest.raises(CantValidateValue):
        assert Schema.from_dict(schema).validate_obj(obj)
