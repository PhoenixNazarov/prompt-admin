from pydantic import BaseModel

from promptadmin.output.parser_output_service import ParserOutputService


class ExtractingDocStructureSlideInner(BaseModel):
    attr_id: int
    attr_title: str
    attr_topics: str


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
                {"attr_id": 1, "attr_title": "Investment Strategy", "attr_topics": "1,2,4"},
                {"attr_id": 2, "attr_title": "Portfolio Composition", "attr_topics": "2,3,5"}
            ]
        }
    }
"""

valid_obj = ExtractingDocStructureOutput(
    structure=ExtractingDocStructureSlide(
        slide=[
            ExtractingDocStructureSlideInner(attr_id=1, attr_title='Investment Strategy', attr_topics='1,2,4'),
            ExtractingDocStructureSlideInner(attr_id=2, attr_title='Portfolio Composition', attr_topics='2,3,5')
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


def test_parse_xml():
    result = """Based on the provided presentation slide, I can classify the fund as follows:

```xml
<result>
  <fund_type id="1" type="Hedge Fund"/>
  <fund_name>Altana Asymmetric Opportunities Fund</fund_name>
  <pitch_name>Altana Asymmetric Opportunities Fund Special Situations Pitch</pitch_name>
</result>
This classification is based on the fund's name "Altana Asymmetric Opportunities Fund" and its focus on "Special Situations with High Return to Risk ratios". The mention of asymmetric opportunities and the emphasis on risk-return ratios are typical characteristics of hedge fund strategies, particularly those focusing on special situations and market inefficiencies.
```
"""

    class FundTypeOutputResultType(BaseModel):
        attr_id: int
        attr_type: str

    class FundTypeOutputResult(BaseModel):
        fund_type: FundTypeOutputResultType
        fund_name: str
        pitch_name: str

    class FundTypeOutput(BaseModel):
        result: FundTypeOutputResult

    assert ParserOutputService().parse(FundTypeOutput, result) == FundTypeOutput(
        result=FundTypeOutputResult(fund_type=FundTypeOutputResultType(attr_id=1, attr_type='Hedge Fund'),
                                    fund_name='Altana Asymmetric Opportunities Fund',
                                    pitch_name='Altana Asymmetric Opportunities Fund Special Situations Pitch')
    )
