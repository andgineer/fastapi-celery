from typing import Dict
from typing import List
from typing import Type
from typing import Union

from pydantic import BaseModel
from sqlalchemy.orm.attributes import InstrumentedAttribute


def list_to_pydantic_list(obj, model: Type[BaseModel]):
    """
    Convert unlimited nested lists of dicts to nested lists of pydantic `model`s.
    """
    if isinstance(obj, list):
        result = [list_to_pydantic_list(item, model) for item in obj]
    else:
        result = model.parse_obj(obj)
    return result


def pydantic_list_to_list(obj):
    """
    Convert unlimited nested lists of pydantic model`s to nested lists of dicts.
    """
    if isinstance(obj, list):
        result = [pydantic_list_to_list(item) for item in obj]
    else:
        result = obj.dict(exclude_unset=True)
    return result


def sql_model_property_setter(
    value: BaseModel, model: Type[BaseModel], default=None
) -> Union[List, Dict]:
    """
    Returns pydantic `model` as object safe to store in DB JSONB.
    """
    if isinstance(value, InstrumentedAttribute) or not value:
        return default
    else:
        return pydantic_list_to_list(value)


def sql_model_property_getter(
    db_object: Union[List, Dict], model: Type[BaseModel], default=None
):
    """
    Loads DB object (usually JSONB) in the pydantic `model`.
    """
    if isinstance(db_object, InstrumentedAttribute):
        db_object = default
    return list_to_pydantic_list(db_object, model)
