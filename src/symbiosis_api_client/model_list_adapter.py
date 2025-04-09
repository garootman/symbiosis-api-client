from typing import Any, List, Type, TypeVar, cast

from pydantic import BaseModel, RootModel, TypeAdapter

T = TypeVar("T", bound=BaseModel)


def list_adapter(data: Any, model: Type[T]) -> List[T]:
    if not isinstance(data, list):
        raise ValueError(f"Expected list, got {type(data)}")
    if not isinstance(model, type) or not issubclass(model, BaseModel):
        raise ValueError(f"Expected subclass of BaseModel, got {model}")

    # Создание нового класса через type(), чтобы избежать проблем с mypy
    TempModel = type("TempModel", (RootModel[List[model]],), {})  # type: ignore

    parsed = TypeAdapter(TempModel).validate_python(data)
    return cast(List[T], parsed.root)
