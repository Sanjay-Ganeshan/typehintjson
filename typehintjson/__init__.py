import sys

assert sys.version_info >= (3, 8), "typehintjson needs python version 3.8.0 or above"

from ._impl import (
    filter_dictionary,
    dataclass_to_dictionary,
    parse_as_type,
    json_to_dataclass
)