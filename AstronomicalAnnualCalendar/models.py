# standard library
import re
from datetime import datetime, timedelta
from typing import Self

# third party
from annotated_types import LowerCase
from pydantic import BaseModel, field_validator
from pydantic.config import ConfigDict
from pydantic.fields import Field
from pydantic.functional_validators import model_validator
from pydantic.types import PositiveFloat
from pydantic_extra_types.color import Color

# local
from .errors import EvaluatedHeaderValidationError
from .translations import get_text
from .utils import optional_hm_str_to_timedelta

__all__ = (
    "CoordinateModel",
    "DataModel",
    "EvaluatedHeaderModel",
    "HeaderModel",
    "MetaDataModel",
    "ObservableObjectModel",
    "RowModel",
)


_SUN_LINE_STRENGTH_MULTIPLIER: float = 4


class ObservableObjectModel(BaseModel):
    """Model to hold basic information about observable objects."""

    model_config = ConfigDict(frozen=True)

    internal_id: LowerCase = Field(alias="id")
    aliases_: set[str] = Field(default_factory=set, alias="aliases")
    line_color: Color
    is_sun_: bool | None = Field(default=None, alias="is_sun")
    is_moon_: bool | None = Field(default=None, alias="is_moon")
    is_planet_: bool | None = Field(default=None, alias="is_planet")
    line_strength_: float = Field(default=2, alias="line_strength", gt=0)
    """NOTE: if the object is a sun the line_strength will get modified!"""

    @property
    def name(self) -> str:
        """Returns the localized name of the object."""
        return get_text(self.internal_id)

    @property
    def aliases(self) -> set[str]:
        """
        Returns given aliases including the name.

        This comes in handy when dealing with the raw (localized) data.
        """
        ret = {self.internal_id, self.name}
        ret.update(self.aliases_)
        return ret

    @property
    def is_sun(self) -> bool:
        """
        Returns whether it's the sun.

        It's determined by setting ``is_sun`` to either True or False.
        If not set, check whether the ``internal_id`` equals "sun".
        """
        if self.is_sun_ is None:
            return self.internal_id == "sun"
        return self.is_sun_

    @property
    def is_moon(self) -> bool:
        """
        Returns whether it's the moon.

        It's determined by setting ``is_moon`` to either True or False.
        If not set, check whether the ``internal_id`` equals "moon".
        """
        if self.is_moon_ is None:
            return self.internal_id == "moon"
        return self.is_moon_

    @property
    def is_planet(self) -> bool:
        """
        Returns whether it's a planet.

        It's determined by setting ``is_planet`` to either True or False.
        If not set will check whether it's already the sun or moon.
        """
        if self.is_planet_ is None:
            return not (self.is_sun or self.is_moon)
        return self.is_planet_

    @property
    def line_strength(self) -> PositiveFloat:
        """Returns the appropriate line-strength for the object."""
        return self.line_strength_ * (_SUN_LINE_STRENGTH_MULTIPLIER if self.is_sun else 1)  # pragma: no cover

    def __hash__(self) -> int:  # noqa: D105
        return hash(self.name)


class BoundToObservableObjectBaseModel(BaseModel):
    bound_object: ObservableObjectModel = Field(frozen=True)


class CoordinateModel(BaseModel):
    """Model to hold basic information about coordinates."""

    model_config = ConfigDict(frozen=True)

    lat: str
    lon: str

    def __str__(self) -> str:  # noqa: D105
        return f"{self.lat} {self.lon}"


class MetaDataModel(BaseModel):
    """Model to hold information about the metadata from the data."""

    model_config = ConfigDict(frozen=True)

    place: str
    coordinate: CoordinateModel
    equinox: float | None
    delta_t: timedelta


class HeaderModel(BaseModel):
    """Model to store basic information about a header."""

    model_config = ConfigDict(frozen=True)

    name: str
    regex: re.Pattern[str]
    length: int = Field(ge=1)
    offset: int = Field(default=0)
    # Note: length and offset are relative to endpos of the match

    def search(self, header: str) -> re.Match[str] | None:
        """Shortcut for ``self.regex.search``."""
        return self.regex.search(header)


class EvaluatedHeaderModel(BoundToObservableObjectBaseModel, BaseModel):
    """Model to store information about a header's position."""

    model_config = ConfigDict(frozen=True)

    bound_header: HeaderModel
    endpos: int = Field(ge=0)

    @property
    def length(self) -> int:
        """Shortcut for ``self.bound_header.length``."""
        return self.bound_header.length

    @property
    def offset(self) -> int:
        """Shortcut for ``self.bound_header.offset``."""
        return self.bound_header.offset

    def get_value(self, raw_line: str) -> str:
        """Get value referred to by header."""
        end = self.endpos + self.offset
        start = end - self.length
        return raw_line[start:end].strip()

    @model_validator(mode="after")
    def _validate_endpos(self) -> Self:
        if (startpos := self.endpos + self.offset - self.length) < 0:
            raise EvaluatedHeaderValidationError(
                endpos=self.endpos,
                offset=self.offset,
                length=self.length,
                startpos=startpos,
            )
        return self


class RowModel(BoundToObservableObjectBaseModel, BaseModel):
    """Represents a single row/set of data."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    date_and_time: datetime = Field(
        title="Date & Time",
        description="The date and time for the specific row/set of data.",
    )
    culmination: timedelta | None = Field(
        default=None,
        title="Culmination",
        description="The culmination relative to ``.date_and_time`` based on the observing position.",
    )

    @field_validator("culmination", mode="before")
    def optional_hm_time_regex_to_timedelta_object(cls, v: timedelta | None | str) -> timedelta | None:  # noqa: N805
        """Allow fields with expected timedelta-objects to be populated with str-objects."""
        if isinstance(v, str):
            v = optional_hm_str_to_timedelta(v)
        return v


class DataModel(BoundToObservableObjectBaseModel, BaseModel):
    """Represents all data connected to an observable object."""

    model_config = ConfigDict(frozen=True)

    metadata: MetaDataModel
    rows: list[RowModel]
