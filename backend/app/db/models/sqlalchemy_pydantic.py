from typing import Any

from pydantic import BaseModel
from sqlalchemy.orm.attributes import InstrumentedAttribute


def list_to_pydantic_list(obj: Any, model: type[BaseModel]) -> list[Any] | BaseModel:
    """
    Convert unlimited nested lists of dicts to nested lists of pydantic `model`s.
    """
    return (
        [list_to_pydantic_list(item, model) for item in obj]
        if isinstance(obj, list)
        else model.model_validate(obj)
    )


def pydantic_list_to_list(obj: Any) -> list[Any] | dict[str, Any]:
    """
    Convert unlimited nested lists of pydantic model`s to nested lists of dicts.
    """
    return (
        [pydantic_list_to_list(item) for item in obj]
        if isinstance(obj, list)
        else obj.dict(exclude_unset=True)
    )


def sql_model_property_setter(
    value: BaseModel,
    model: type[BaseModel],  # pylint: disable=unused-argument
    default: Any = None,
) -> list[Any] | dict[str, Any]:
    """
    Returns pydantic `model` as object safe to store in DB JSONB.
    """
    if isinstance(value, InstrumentedAttribute) or not value:
        return default  # type: ignore
    return pydantic_list_to_list(value)


def sql_model_property_getter(
    db_object: list[str] | dict[str, Any],
    model: type[BaseModel],
    default: Any = None,
) -> list[BaseModel] | BaseModel:
    """
    Loads DB object (usually JSONB) in the pydantic `model`.
    """
    if isinstance(db_object, InstrumentedAttribute):
        db_object = default
    return list_to_pydantic_list(db_object, model)
