# standard library
from abc import ABC, abstractmethod

# third party
from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.types import FilePath

# local
from ..models import DataModel, MetaDataModel, ObservableObjectModel


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
