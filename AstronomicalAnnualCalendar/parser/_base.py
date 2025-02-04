# standard library
from abc import ABC, abstractmethod

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
