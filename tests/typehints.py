# standard library
from typing import Protocol


__all__ = ("GetTextCallable",)


class GetTextCallable(Protocol):  # noqa: D101
    def __call__(self, message: str, *, lang: str | None = None) -> str: ...  # noqa: D102
