# standard library
from collections.abc import Iterator
from datetime import datetime, timedelta, timezone

# third party
from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.types import FilePath

# local
from .enums import HeaderEnum, ObservableObjectEnum
from .models import (
    CoordinateModel,
    DataModel,
    EvaluatedHeaderModel,
    MetaDataModel,
    ObservableObjectModel,
    RowModel,
)
from .regex import METADATA_REGEX, OBJECT_DATA_BODY_REGEX
from .utils import get_present_headers, observable_object_from_alias, raw_delta_t_to_timedelta


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
        data: dict[ObservableObjectModel, DataModel] = {}
        for name, header, body in self._iter_observable_objects():
            bound_object = observable_object_from_alias(name)
            rows = self._parse_rows(bound_object, header, body)
            data[bound_object] = DataModel(bound_object=bound_object, metadata=self.metadata, rows=rows)
        return data

    @staticmethod
    def _parse_rows(bound_object: ObservableObjectModel, header: str, body: str) -> list[RowModel]:
        rows: list[RowModel] = []
        present_headers: list[EvaluatedHeaderModel] = get_present_headers(bound_object, header)

        # I know that this is filthy...
        tz = timezone(timedelta(hours={"MEZ ": 1, "MESZ": 2, "UTC ": 0}[HeaderEnum.TIME.search(header)[0]]))

        for row in body.splitlines():

            row_data = {}
            for h in present_headers:
                row_data[h.bound_header.name] = h.get_value(row)

            row_data.pop("weekday")  # not needed, can be discarded

            date = row_data.pop("date")
            time = row_data.pop("time")
            row_data["date_and_time"] = datetime(
                year=int(date[6:]),
                month=int(date[3:5]),
                day=int(date[:2]),
                hour=int(time[:2]),
                minute=int(time[3:5]),
                second=int(time[6:]),
                tzinfo=tz,
            )

            rows.append(RowModel(bound_object=bound_object, **row_data))

        return rows

    def _iter_observable_objects(self) -> Iterator[tuple[ObservableObjectEnum, str, str]]:
        for match in OBJECT_DATA_BODY_REGEX.finditer(self.file.read_text("utf-8")):
            yield observable_object_from_alias(match.group("name")), match.group("header"), match.group("body")
