from pydantic import BaseModel

from promptadmin.output.parser_output_service import ParserOutputService


class ExtractingDocStructureSlideInner(BaseModel):
    id: int
    title: str
    topics: str


class ExtractingDocStructureSlide(BaseModel):
    slide: list[ExtractingDocStructureSlideInner]


class ExtractingDocStructureOutput(BaseModel):
    structure: ExtractingDocStructureSlide


xml_case = """
    <structure>
      <slide id="1" title="Investment Strategy" topics="1,2,4"/>
      <slide id="2" title="Portfolio Composition" topics="2,3,5"/>
    </structure> 
"""

json_case = """
    {
        "structure": {
            "slide": [
                {"id": 1, "title": "Investment Strategy", "topics": "1,2,4"},
                {"id": 2, "title": "Portfolio Composition", "topics": "2,3,5"}
            ]
        }
    }
"""

valid_obj = ExtractingDocStructureOutput(
    structure=ExtractingDocStructureSlide(
        slide=[
            ExtractingDocStructureSlideInner(id=1, title='Investment Strategy', topics='1,2,4'),
            ExtractingDocStructureSlideInner(id=2, title='Portfolio Composition', topics='2,3,5')
        ]
    )
)


def test_parse_xml():
    assert ParserOutputService().parse(ExtractingDocStructureOutput, xml_case) == valid_obj


def test_parse_xml_additional():
    assert ParserOutputService().parse(ExtractingDocStructureOutput,
                                       'qweqwe' + xml_case + '<lkqwmel qwelkm qwlkme lwqk melwq ke') == valid_obj


def test_parse_json():
    assert ParserOutputService().parse(ExtractingDocStructureOutput, json_case) == valid_obj


def test_parse_json_additional():
    assert ParserOutputService().parse(ExtractingDocStructureOutput,
                                       'qweqwe' + json_case + '<lkqwmel qwelkm qwlkme lwqk melwq ke') == valid_obj


def test_parse_null_xml():
    assert ParserOutputService().parse(ExtractingDocStructureOutput, '<123>123</qwe>') is None
    assert ParserOutputService().parse(ExtractingDocStructureOutput, '>') is None
    assert ParserOutputService().parse(ExtractingDocStructureOutput, '') is None


def test_parse_null_json():
    assert ParserOutputService().parse(ExtractingDocStructureOutput, '{123}') is None
    assert ParserOutputService().parse(ExtractingDocStructureOutput, '') is None
