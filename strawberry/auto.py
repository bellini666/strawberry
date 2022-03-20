from __future__ import annotations

from typing import Any, Optional, Union, cast

from typing_extensions import Annotated, Final, get_args, get_origin

from strawberry.type import StrawberryType

from .annotation import StrawberryAnnotation


class StrawberryAutoMeta(type):
    """Metaclass for StrawberryAuto to ensure it is a singleton."""

    def __init__(self, *args, **kwargs):
        self._instance: Optional[StrawberryAuto] = None
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)

        return cls._instance

    def __instancecheck__(
        self,
        instance: Union[StrawberryAuto, StrawberryAnnotation, StrawberryType, type],
    ):
        if isinstance(instance, StrawberryAnnotation):
            resolved = instance.annotation
            if isinstance(resolved, str):
                namespace = instance.namespace
                resolved = namespace and namespace.get(resolved)

            if resolved is not None:
                instance = cast(type, resolved)

        if instance is auto:
            return True

        # Support uses of Annotated[auto, something()]
        if get_origin(instance) is Annotated:
            args = get_args(instance)
            if args[0] is Any:
                return any(isinstance(arg, StrawberryAuto) for arg in args[1:])

        return False


class StrawberryAuto(metaclass=StrawberryAutoMeta):
    def __str__(self):
        return "auto"

    def __repr__(self):
        return "<auto>"


auto: Final = Annotated[Any, StrawberryAuto()]
