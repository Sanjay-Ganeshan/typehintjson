# JSON Decoder / Encoder for type hints

Simple, 2 file python module that parses JSON into dataclasses / enums
and vice versa. Ignores extra fields, and works with default values for 
missing fields.

Requires Python 3.8.0 or higher

For security sake, you have to know the type you're expecting to deserialize
into.


Unions will be resolved in order (i.e. Union[int, MyType, None] will first
try parsing as int, then as MyType, then as None),
so if a value is MULTIPLE valid types, it might not pick the right one.

## Installation
```
pip install typehintjson
```


## Usage
```python
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

# Parent(a=2, c=Child(x='meow', y=4))
```