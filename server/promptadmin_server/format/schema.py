from __future__ import annotations

import json
import logging
from json import JSONDecodeError
from pyexpat import ExpatError
from typing import Literal
import xmltodict

from promptadmin_server.format import errors, dto

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
    def generate_from_json(cls, obj: str):
        try:
            obj = json.loads(obj)
        except JSONDecodeError:
            raise errors.CantGenerateSchema('Is not json')

        return cls.generate_from_obj(obj)

    @classmethod
    def generate_from_xml(cls, obj: str):
        try:
            obj = xmltodict.parse(obj)
        except ExpatError:
            raise errors.CantGenerateSchema('Is not xml')

        return cls.generate_from_obj(obj)

    @classmethod
    def generate_from_obj(cls, obj: SupportGenerateType) -> Schema:
        return ValueSchema.generate_from_obj(obj)

    def validate(self, obj: str) -> SupportValidateType:
        try:
            return self.validate_json(obj)
        except errors.CantValidateValue:
            pass

        try:
            return self.validate_xml(obj)
        except errors.CantValidateValue:
            pass

        try:
            return self.validate_obj(obj)
        except errors.CantValidateValue:
            pass

        raise errors.CantValidateValue()

    def validate_json(self, obj: str) -> SupportValidateType:
        try:
            obj = json.loads(obj)
        except JSONDecodeError:
            raise errors.CantValidateValue('Is not json')

        return self.validate_obj(obj)

    def validate_xml(self, obj: str) -> SupportValidateType:
        try:
            obj = xmltodict.parse(obj)
        except ExpatError:
            raise errors.CantValidateValue('Is not xml')

        return self.validate_obj(obj)

    def validate_obj(self, obj: SupportValidateType) -> SupportValidateType:
        raise NotImplementedError()

    def make_example_json(self, indent=None) -> str:
        try:
            return json.dumps(self.make_example_obj(), indent=indent)
        except JSONDecodeError:
            raise errors.CantMakeExample('Cant convert to json')

    def make_example_xml(self, pretty=False, indent=0) -> str:
        try:
            return xmltodict.unparse(self.make_example_obj(), full_document=False, pretty=pretty, indent=' ' * indent)
        except AttributeError:
            raise errors.CantMakeExample('Cant convert to xml')
        except ExpatError:
            raise errors.CantMakeExample('Cant convert to xml')
        except ValueError as e:
            raise errors.CantMakeExample('Cant convert to xml. ' + str(e))

    def make_example_obj(self) -> SupportValidateType:
        raise NotImplementedError()

    def get_consistent_format_report(self) -> dto.ConsistentFormatReport:
        report = dto.ConsistentFormatReport()
        scheme_dict = None
        try:
            scheme_dict = self.to_dict()
            report.to_dict = True
        except Exception as e:
            logger.warning('Unexpected exception while consistent_format_report', exc_info=e)
            pass

        # Object
        try:
            example_obj = self.make_example_obj()
            report.make_example_obj = True
            new_scheme_obj = Schema.generate_from_obj(example_obj)
            report.make_example_obj_converse = True
            report.make_example_obj_converse_equal = (scheme_dict is not None and
                                                      scheme_dict == new_scheme_obj.to_dict())
        except errors.CantMakeExample:
            pass
        except errors.CantGenerateSchema:
            pass

        # Json
        try:
            example_json = self.make_example_json()
            report.make_example_json = True
            new_scheme_json = Schema.generate_from_json(example_json)
            report.make_example_json_converse = True
            report.make_example_json_converse_equal = (scheme_dict is not None and
                                                       scheme_dict == new_scheme_json.to_dict())
        except errors.CantMakeExample:
            pass
        except errors.CantGenerateSchema:
            pass

        # Xml
        try:
            example_xml = self.make_example_xml()
            report.make_example_xml = True
            new_scheme_xml = Schema.generate_from_xml(example_xml)
            report.make_example_xml_converse = True
            report.make_example_xml_converse_equal = (scheme_dict is not None and
                                                      scheme_dict == new_scheme_xml.to_dict())
        except errors.CantMakeExample:
            pass
        except errors.CantGenerateSchema:
            pass

        return report


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

    @staticmethod
    def casting_types(obj):
        if isinstance(obj, str):
            try:
                if obj.isdigit():
                    return int(obj)
                else:
                    return float(obj)
            except ValueError:
                pass
            except TypeError:
                pass
        return obj

    @classmethod
    def generate_from_obj(cls, obj: SupportGenerateType) -> ValueSchema:
        obj = cls.casting_types(obj)
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
        return [
            self.__validate_obj_value(i) for i in obj
        ]

    def make_example_obj(self) -> SupportValidateType:
        res = None
        if self.value_type == 'float':
            res = 1.1
        elif self.value_type == 'integer':
            res = 1
        elif self.value_type == 'string':
            res = 'test'
        elif self.value_type == 'object':
            res = self.object_schema.make_example_obj()

        if self.array:
            return [res, res]
        return res


class ObjectSchema(Schema):
    schema_type_name = 'object'

    def __init__(self, fields: dict[str, ValueSchema]):
        self.fields = fields

    @classmethod
    def from_dict(cls, dict_schema: dict) -> ObjectSchema:
        cls.validate_dict_schema([('fields', dict, True)], dict_schema)
        fields = dict_schema.get('fields', {})
        return ObjectSchema(fields={k: ValueSchema.from_dict(v) for k, v in fields.items()})

    def _to_dict_impl(self) -> dict:
        return {
            'fields': {k: v.to_dict() for k, v in self.fields.items()}
        }

    @classmethod
    def generate_from_obj(cls, obj: SupportGenerateType) -> ObjectSchema:
        if not isinstance(obj, dict):
            raise errors.CantGenerateSchema(f'Object: {obj} is not dict')

        return ObjectSchema(fields={k: ValueSchema.generate_from_obj(v) for k, v in obj.items()})

    def validate_obj(self, obj: SupportValidateType) -> SupportValidateType:
        if not isinstance(obj, dict):
            raise errors.CantValidateValue(f'Object: {obj} is not dict')

        accept_keys = set(self.fields.keys())
        current_keys = set(obj.keys())
        no_accept_keys = current_keys - accept_keys
        required_keys = accept_keys - current_keys
        if len(no_accept_keys) > 0:
            raise errors.CantValidateValue(f'Object: {obj} has not acceptable keys: {no_accept_keys}')
        if len(required_keys) > 0:
            raise errors.CantValidateValue(f'Object: {obj} has need required keys: {required_keys}')

        return {
            k: v.validate_obj(obj[k]) for k, v in self.fields.items()
        }

    def make_example_obj(self) -> dict:
        return {
            k: v.make_example_obj() for k, v in self.fields.items()
        }
