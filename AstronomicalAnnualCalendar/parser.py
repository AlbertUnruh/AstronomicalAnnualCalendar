# standard library
from collections.abc import Iterator

# third party
from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.types import FilePath

# local
from .enums import ObservableObjectEnum
from .models import CoordinateModel, DataModel, MetaDataModel, ObservableObjectModel
from .regex import METADATA_REGEX, OBJECT_DATA_BODY_REGEX
from .utils import observable_object_from_alias, raw_delta_t_to_timedelta


__all__ = ("Parser",)


class Parser(BaseModel):  # noqa: D101  # ToDo: add documentation
    file: FilePath = Field(alias="file_path")

    _cached_metadata: MetaDataModel = None

    @property
    def metadata(self) -> MetaDataModel:
        """The information from the first line of the file."""
        if self._cached_metadata is None:  # pragma: no cover
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

    def _iter_observable_objects(self) -> Iterator[tuple[ObservableObjectEnum, str, str]]:
        for match in OBJECT_DATA_BODY_REGEX.finditer(self.file.read_text("utf-8")):
            yield observable_object_from_alias(match.group("name")), match.group("header"), match.group("body")
