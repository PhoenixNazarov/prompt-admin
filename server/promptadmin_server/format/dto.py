from pydantic import BaseModel


class ConsistentFormatReport(BaseModel):
    to_dict: bool = False

    make_example_obj: bool = False
    make_example_obj_converse: bool = False
    make_example_obj_converse_equal: bool = False

    make_example_json: bool = False
    make_example_json_converse: bool = False
    make_example_json_converse_equal: bool = False

    make_example_xml: bool = False
    make_example_xml_converse: bool = False
    make_example_xml_converse_equal: bool = False
