# third party
from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.types import FilePath

# first party
from AstronomicalAnnualCalendar.models import MetaDataModel


__all__ = ("Parser",)


class Parser(BaseModel):  # noqa: D101  # ToDo: add documentation
    file: FilePath = Field(alias="file_path")

    _cached_metadata: MetaDataModel = None

    @property
    def metadata(self) -> MetaDataModel:
        """The information from the first line of the file."""
        if self._cached_metadata is None:
            self.populate_metadata()
        return self._cached_metadata

    def model_post_init(self, *args, **kwargs) -> None:  # noqa: D102, ANN002, ANN003
        self.populate_metadata()

    def populate_metadata(self) -> None:  # noqa: D102  # ToDo: add documentation
        ...
