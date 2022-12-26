import json
import typing as T

from typehintjson import parse_as_type, dataclass_to_dictionary
from dataclasses import dataclass

@dataclass
class Child:
    x: T.Union[int, str]
    y: int = 4

@dataclass
class Parent:
    a: int
    c: Child


obj = Parent(a=2, c=Child(x="meow"))
print(repr(parse_as_type(json.loads(json.dumps(dataclass_to_dictionary(obj))), Parent)))