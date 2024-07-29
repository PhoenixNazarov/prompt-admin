import json

from pydantic import BaseModel

from promptadmin_server.format.dto import ConsistentFormatReport
from promptadmin_server.format.errors import CantParseSchema, CantMakeExample, CantGenerateSchema, CantValidateValue
from promptadmin_server.format.schema import Schema


class CalculateOutput(BaseModel):
    cant_load_schema_error: str | None = None
    cant_generate_schema_error: str | None = None

    format_json: str | None = None

    example_json: str | None = None
    cant_make_example_json_error: str | None = None
    example_xml: str | None = None
    cant_make_example_xml_error: str | None = None

    consistent_report: ConsistentFormatReport | None = None


class ValidateOutput(BaseModel):
    cant_load_schema_error: str | None = None
    cant_validate_value_error: str | None = None
    validate_value: str | None = None


def parse_json_garbage(s):
    s = s[next(idx for idx, c in enumerate(s) if c in "{["):]
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        return json.loads(s[:e.pos])


class FormatService:
    def __init__(self):
        pass

    def load_calculate(self, json_schema: str) -> CalculateOutput:
        try:
            schema = Schema.from_json(json_schema)
        except CantParseSchema as e:
            return CalculateOutput(cant_load_schema_error=str(e))
        return self.process_calculator(schema)

    def generate_calculate(self, input_object: str, mode: str) -> CalculateOutput:
        try:
            if mode == 'object':
                schema = Schema.generate_from_obj(input_object)
            elif mode == 'xml':
                schema = Schema.generate_from_xml(input_object)
            else:
                schema = Schema.generate_from_json(input_object)
        except CantGenerateSchema as e:
            return CalculateOutput(cant_generate_schema_error=str(e))

        return self.process_calculator(schema)

    def process_calculator(self, schema: Schema) -> CalculateOutput:
        result = CalculateOutput()
        result.format_json = schema.to_json()

        try:
            result.example_json = schema.make_example_json(indent=2)
        except CantMakeExample as e:
            result.cant_make_example_json_error = str(e)

        try:
            result.example_xml = schema.make_example_xml(pretty=True, indent=2)
        except CantMakeExample as e:
            result.cant_make_example_xml_error = str(e)

        result.consistent_report = schema.get_consistent_format_report()
        return result

    def validate(self, json_schema: str, obj: str):
        try:
            schema = Schema.from_json(json_schema)
        except CantParseSchema as e:
            return ValidateOutput(cant_load_schema_error=str(e))

        try:
            return ValidateOutput(validate_value=str(schema.validate(obj)))
        except CantValidateValue as e:
            return ValidateOutput(cant_validate_value_error=str(e))
