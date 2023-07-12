import dataclasses
import typing as T
import enum
import json

def filter_dictionary(args_dict: T.Dict[str, T.Any], as_dataclass: T.Any) -> T.Dict[str, T.Any]:
    """
    Given a dictionary, and a dataclass type, filters
    the fields of the dictionary to only the keys which are present
    in the dataclass's generated __init__ function
    """
    fields = {f.name for f in dataclasses.fields(as_dataclass) if f.init}
    return {
        k: args_dict[k] for k in args_dict if k in fields
    }

def dataclass_to_dictionary(obj: T.Any, flatten_enums: bool = False) -> T.Any:
    """
    Converts a dataclass to a dictionary
    """
    if isinstance(obj, enum.Enum):
        if flatten_enums:
            return obj.value
        else:
            return {"name": obj.name, "value": obj.value}
    
    if dataclasses.is_dataclass(obj):
        fields = dataclasses.fields(obj)
        return {
            f.name: dataclass_to_dictionary(getattr(obj, f.name))
            for f in fields
        }

    if isinstance(obj, list):
        return [dataclass_to_dictionary(item) for item in obj]

    if isinstance(obj, dict):
        return {k: dataclass_to_dictionary(obj[k]) for k in obj}
    
    return obj

def parse_as_type(js_obj: T.Any, expected_type: T.Type[T.Any]) -> T.Any:
    """
    Parses the json object js_obj as an instance of the given type.
    Raises an exception if the object does not match the type.
    Otherwise, an object of the given type.

    # js_obj can be:
    # strings
    # integers
    # floats
    # None
    # dictionaries of string -> js_obj
    # lists of js_obj
    """
    
    
    # print("Parsing", js_obj, "as", expected_type)
    origin = T.get_origin(expected_type)
    if origin is None:
        assert isinstance(expected_type, type), f"Bad type: {expected_type} for {js_obj}"
            
        if issubclass(expected_type, enum.Enum):
            return expected_type(js_obj)
        if dataclasses.is_dataclass(expected_type):
            assert isinstance(js_obj, dict), f"Bad dict: {js_obj}"
            init_args = {}
            for each_field in dataclasses.fields(expected_type):
                if each_field.name in js_obj and each_field.init:
                    init_args[each_field.name] = parse_as_type(js_obj[each_field.name], each_field.type)
            return expected_type(**init_args)
        if isinstance(js_obj, expected_type):
            return js_obj
        # Try just converting
        return expected_type(js_obj)         

    else:
        if origin is T.Literal:
            pass
        elif origin is T.ClassVar:
            pass
        elif origin is T.Generic:
            pass
        elif origin is T.Union:
            possibilities = T.get_args(expected_type)
            for each_possibility in possibilities:
                try:
                    return parse_as_type(js_obj, each_possibility) 
                except Exception:
                    pass
            raise ValueError(f"{js_obj} is not any of: {possibilities}")
        elif origin is list:
            (item_type,) = T.get_args(expected_type)
            assert isinstance(js_obj, list), f"Bad list: {js_obj}"
            ret = []
            for item in js_obj:
                ret.append(parse_as_type(item, item_type))
            return ret

        elif origin is dict:
            k_type, v_type = T.get_args(expected_type)
            assert isinstance(js_obj, dict), f"Bad obj: {js_obj}"
            ret = {}
            for k in js_obj:
                v = js_obj[k]
                ret[parse_as_type(k, k_type)] = parse_as_type(v, v_type)
            return ret
            
    
    raise NotImplementedError(f"Unexpected type/origin: {expected_type}/{origin}")

def json_to_dataclass(js: str, expected_dc: T.Any, **kwargs):
    """
    Shorthand for (parse_as_type(json.loads(...)))
    """
    return parse_as_type(json.loads(js, **kwargs), expected_dc)
