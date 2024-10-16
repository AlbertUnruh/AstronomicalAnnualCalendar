# third party
from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.types import FilePath

# local
from .models import CoordinateModel, DataModel, HeaderModel, MetaDataModel, ObservableObjectModel
from .regex import METADATA_REGEX
from .utils import raw_delta_t_to_timedelta


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
        with self.file.open("r", encoding="utf-8") as f:
            first_file = f.readline()

        metadata = METADATA_REGEX.match(first_file)

        self._cached_metadata = MetaDataModel(
            place=metadata.group("place"),
            coordinate=CoordinateModel(lat=metadata.group("lat"), lon=metadata.group("lon")),
            equinox=metadata.group("equinox"),
            delta_t=raw_delta_t_to_timedelta(metadata.group("delta_t"), metadata.group("delta_t_unit")),
        )

    def parse(self) -> dict[ObservableObjectModel, DataModel]:  # noqa: D102  # ToDo: add documentation
        raise NotImplementedError

    def _parse_observable_objects(self):
        raise NotImplementedError

    def _extract_header(self) -> dict[ObservableObjectModel, HeaderModel]:
        raise NotImplementedError
