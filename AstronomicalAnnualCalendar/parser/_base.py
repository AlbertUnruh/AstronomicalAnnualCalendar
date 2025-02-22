# standard library
from abc import ABC, abstractmethod
from inspect import getdoc

# third party
from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.types import FilePath

# local
from ..models import DataModel, MetaDataModel, ObservableObjectModel
from ..utils import classproperty


__all__ = ("ABCParser",)


class ABCParser(ABC, BaseModel):
    """Baseclass for every parser."""

    file: FilePath = Field(alias="file_path")

    @property
    @abstractmethod
    def metadata(self) -> MetaDataModel:
        """Return with data associated metadata."""

    @abstractmethod
    def parse(self) -> dict[ObservableObjectModel, DataModel]:
        """Parse data and return it accordingly."""

    @classproperty
    @abstractmethod
    def specification(cls) -> str:  # noqa: N805
        """Return a specification of what the current parser expects (in a human-readable format)."""

    @classproperty
    def parser_name(cls) -> str:  # noqa: N805
        """Return the name of the parser."""
        return cls.__name__

    @staticmethod
    @classproperty
    def _human_readable_abcs_to_implement() -> str:
        """Return abstract methods (in a human-readable format)."""
        longest_method_name = len(max(ABCParser.__abstractmethods__, key=len)) + 1
        methods = []
        for method_name in sorted(ABCParser.__abstractmethods__):
            method = ABCParser.__getattribute__(ABCParser, method_name)
            methods.append(f"  - {method_name+":": <{longest_method_name}} {getdoc(method)}")
        return f"Following methods need to be implemented:\n{"\n".join(methods)}"
