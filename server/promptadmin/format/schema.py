from __future__ import annotations

import json
import logging
from json import JSONDecodeError
from typing import Literal

from . import errors

logger = logging.getLogger()

SCHEMA_TYPE_KEY = 'schema_type'

SupportGenerateType = list | dict | str | int | float
SupportValidateType = list | dict | str | int | float


class Schema:
    schema_type_name = 'prompt-admin-schema'
    schema_type_key = SCHEMA_TYPE_KEY

    @classmethod
    def from_json(cls, json_schema: str) -> Schema:
        try:
            dict_schema = json.loads(json_schema)
        except JSONDecodeError:
            raise errors.CantParseSchema()

        return cls.from_dict(dict_schema)

    @classmethod
    def from_dict(cls, dict_schema: dict) -> Schema:
        return ValueSchema.from_dict(dict_schema)

    @classmethod
    def validate_dict_schema(cls, keys: list[(str, type, bool)], dict_schema: dict):
        accept_keys = {i[0] for i in keys}
        accept_keys.add(cls.schema_type_key)

        if set(dict_schema.keys()) - accept_keys != set():
            raise errors.CantParseSchema('Not provide all schema keys')

        if (now_schema_name := dict_schema.get(cls.schema_type_key)) != cls.schema_type_name:
            raise errors.CantParseSchema(f'Expected schema name: {cls.schema_type_name}. But now: {now_schema_name}')

        for key in keys:
            name = key[0]
            type_ = key[1]
            required = key[2]
            val = dict_schema.get(name)
            if val is None:
                if required:
                    raise errors.CantParseSchema(f'Not set required key: {name}')
            else:
                if not isinstance(val, type_):
                    raise errors.CantParseSchema(f'Provide value: {name} expected type: {type_}, but now: {type(val)}')

    def to_json(self) -> str:
        dict_schema = self.to_dict()
        return json.dumps(dict_schema)

    def to_dict(self) -> dict:
        dict_impl = self._to_dict_impl()
        dict_impl[self.schema_type_key] = self.schema_type_name
        return dict_impl

    def _to_dict_impl(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def generate_from_obj(cls, obj: SupportGenerateType) -> Schema:
        return ValueSchema.generate_from_obj(obj)

    def validate(self, obj: str) -> SupportValidateType:
        pass

    def validate_json(self, obj: str) -> SupportValidateType:
        pass

    def validate_xml(self, obj: str) -> SupportValidateType:
        pass

    def validate_obj(self, obj: SupportValidateType) -> SupportValidateType:
        raise NotImplementedError()


class ValueSchema(Schema):
    schema_type_name = 'value'

    def __init__(
            self,
            value_type: Literal['string', 'integer', 'float', 'object'],
            object_schema: ObjectSchema | None = None,
            array: bool | None = None,
    ):
        self.value_type = value_type
        self.object_schema = object_schema
        self.array = array

    @classmethod
    def from_dict(cls, dict_schema: dict) -> ValueSchema:
        dict_keys = [
            ['value_type', str, True],
            ['object_schema', dict, False],
            ['array', bool, False],
        ]
        cls.validate_dict_schema(dict_keys, dict_schema)

        value_type = dict_schema['value_type']
        array = dict_schema.get('array')
        if value_type == 'object':
            if dict_schema.get('object_schema') is None:
                raise errors.CantParseSchema('value must have key object_schema')
            return ValueSchema(
                value_type=value_type,
                object_schema=ObjectSchema.from_dict(dict_schema['object_schema']),
                array=array
            )
        return ValueSchema(
            value_type=value_type,
            array=array
        )

    def _to_dict_impl(self) -> dict:
        dict_schema = {
            'value_type': self.value_type
        }
        if self.object_schema:
            dict_schema['object_schema'] = self.object_schema.to_dict()
        if self.array:
            dict_schema['array'] = self.array
        return dict_schema

    @classmethod
    def generate_from_obj(cls, obj: SupportGenerateType) -> ValueSchema:
        if isinstance(obj, list):
            return cls.__generate_from_obj_list(obj)
        elif isinstance(obj, dict):
            return ValueSchema(
                value_type='object',
                object_schema=ObjectSchema.generate_from_obj(obj)
            )
        elif isinstance(obj, float):
            return ValueSchema(
                value_type='float'
            )
        elif isinstance(obj, int):
            return ValueSchema(
                value_type='integer'
            )
        elif isinstance(obj, str):
            return ValueSchema(
                value_type='string'
            )

        raise errors.CantGenerateSchema(f'Not support type for: {type(obj)}')

    @classmethod
    def __generate_from_obj_list(cls, obj: list) -> ValueSchema:
        if len(obj) <= 0:
            raise errors.CantGenerateSchema('Try to generate from empty list')

        if isinstance(obj[0], dict):
            accept_keys = set(obj[0].keys())
            for i in obj:
                if not isinstance(i, dict) or set(i.keys()) != accept_keys:
                    raise errors.CantGenerateSchema('Object keys in list not equals')
            return ValueSchema(
                value_type='object',
                array=True,
                object_schema=ObjectSchema.generate_from_obj(obj[0])
            )

        if isinstance(obj[0], list):
            raise errors.CantGenerateSchema('2d array not support')

        for type_, value_type in [(int, 'integer'), (float, 'float'), (str, 'string')]:
            for i in obj:
                if not isinstance(i, type_):
                    break
            else:
                return ValueSchema(
                    value_type=value_type,
                    array=True
                )
        else:
            raise errors.CantGenerateSchema('Array types not equal')

    def validate_obj(self, obj: SupportValidateType) -> SupportValidateType:
        if self.array:
            return self.__validate_obj_list(obj)
        return self.__validate_obj_value(obj)

    def __validate_obj_value(self, obj: SupportValidateType) -> SupportValidateType:
        if self.value_type == 'float':
            try:
                return float(obj)
            except ValueError:
                raise errors.CantValidateValue(f'Object: {obj} is not float')
        elif self.value_type == 'integer':
            try:
                return int(obj)
            except ValueError:
                raise errors.CantValidateValue(f'Object: {obj} is not integer')
            except TypeError:
                raise errors.CantValidateValue(f'Object: {obj} is not integer')
        elif self.value_type == 'string':
            try:
                return str(obj)
            except ValueError:
                raise errors.CantValidateValue(f'Object: {obj} is not string')
        elif self.value_type == 'object':
            return self.object_schema.validate_obj(obj)
        raise errors.CantValidateValue()

    def __validate_obj_list(self, obj: SupportValidateType) -> SupportValidateType:
        if not isinstance(obj, list):
            raise errors.CantValidateValue(f'Object: {obj} is not list')
        print(obj)
        return [
            self.__validate_obj_value(i) for i in obj
        ]


class ObjectSchema(Schema):
    schema_type_name = 'object'

    def __init__(self, fields: list[FieldSchema]):
        self.fields = fields

    @classmethod
    def from_dict(cls, dict_schema: dict) -> ObjectSchema:
        cls.validate_dict_schema([('fields', list, False)], dict_schema)
        fields = dict_schema.get('fields', [])
        return ObjectSchema(fields=[FieldSchema.from_dict(i) for i in fields])

    def _to_dict_impl(self) -> dict:
        return {
            'fields': [i.to_dict() for i in self.fields]
        }

    @classmethod
    def generate_from_obj(cls, obj: SupportGenerateType) -> ObjectSchema:
        if not isinstance(obj, dict):
            raise errors.CantGenerateSchema(f'Object: {obj} is not dict')

        return ObjectSchema(fields=[FieldSchema.generate_from_obj({k: v}) for k, v in obj.items()])

    def validate_obj(self, obj: SupportValidateType) -> SupportValidateType:
        if not isinstance(obj, dict):
            raise errors.CantValidateValue(f'Object: {obj} is not dict')

        accept_keys = set([i.name for i in self.fields])
        no_accept_keys = set(obj.keys()) - accept_keys
        required_keys = accept_keys - set(obj.keys())
        if len(no_accept_keys) > 0:
            raise errors.CantValidateValue(f'Object: {obj} has not acceptable keys: {no_accept_keys}')
        if len(required_keys) > 0:
            raise errors.CantValidateValue(f'Object: {obj} has need required keys: {required_keys}')

        res = {}
        for field in self.fields:
            res.update(field.validate_obj({field.name: obj[field.name]}))
        return res


class FieldSchema(Schema):
    schema_type_name = 'field'

    def __init__(
            self,
            name: str,
            value_schema: ValueSchema
    ):
        self.name = name
        self.value_schema = value_schema

    @classmethod
    def from_dict(cls, dict_schema: dict) -> FieldSchema:
        dict_keys = [
            ['name', str, True],
            ['value_schema', dict, True],
        ]
        cls.validate_dict_schema(dict_keys, dict_schema)
        return FieldSchema(
            name=dict_schema['name'],
            value_schema=ValueSchema.from_dict(dict_schema['value_schema'])
        )

    def _to_dict_impl(self) -> dict:
        return {
            "name": self.name,
            "value_schema": self.value_schema.to_dict(),
        }

    @classmethod
    def generate_from_obj(cls, obj: SupportGenerateType) -> FieldSchema:
        if not isinstance(obj, dict):
            raise errors.CantGenerateSchema()
        keys = list(obj.keys())
        if len(obj.keys()) != 1:
            raise errors.CantGenerateSchema()
        key = keys[0]

        return FieldSchema(
            name=key,
            value_schema=ValueSchema.generate_from_obj(obj[key])
        )

    def validate_obj(self, obj: SupportValidateType) -> SupportValidateType:
        if not isinstance(obj, dict):
            raise errors.CantValidateValue()
        keys = list(obj.keys())
        if len(obj.keys()) != 1:
            raise errors.CantValidateValue()
        key = keys[0]

        if key != self.name:
            raise errors.CantValidateValue()

        return {key: self.value_schema.validate_obj(obj[key])}
