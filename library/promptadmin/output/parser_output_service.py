import json
import re
from json import JSONDecodeError

import xmltodict
from pydantic import BaseModel, ValidationError


class ParserOutputService:
    def parse(self, model_type, result: str):
        if issubclass(model_type, BaseModel):
            try:
                return model_type.parse_obj(self.try_extract_json(result))
            except StopIteration:
                pass
            except JSONDecodeError:
                pass
            except ValidationError:
                pass
            try:
                return model_type.parse_obj(self.try_parse_xml(result))
            except ValidationError:
                pass
        return None

    @staticmethod
    def try_extract_json(s: str):
        if '{' not in s and '[' not in s:
            s = '{' + s
        s = s[next(idx for idx, c in enumerate(s) if c in '{['):]
        try:
            return json.loads(s)
        except json.JSONDecodeError as e:
            return json.loads(s[:e.pos])

    @staticmethod
    def try_parse_xml(s: str):
        s = s.replace('\n', '@||')
        tag = re.search(r'<([a-zA-Z_]*)>', s)
        if tag:
            first_tag = tag.group(1)
            res = re.search(rf'<{first_tag}>.*</{first_tag}>', s)
            if res:
                find = res.group(0)
                find = find.replace('@||', '\n')
                return xmltodict.parse(find, attr_prefix='attr_')
        res = re.search(r'<[^>]*/>', s)
        if res is None:
            return None
        find = res.group(0)
        find = find.replace('@||', '\n')
        return xmltodict.parse(find, attr_prefix='attr_')
