# standard library
import re
from datetime import datetime, timedelta

# third party
from annotated_types import LowerCase
from pydantic import BaseModel
from pydantic.config import ConfigDict
from pydantic.fields import Field
from pydantic.types import PositiveFloat
from pydantic_extra_types.color import Color

# local
from .regex import (
    DEGREE_180_REGEX,
    DEGREE_360_REGEX,
    DMS_ANGLE_90_REGEX,
    DMS_ANGLE_360_REGEX,
    HMS_ANGLE_REGEX,
    OPTIONAL_HM_TIME_REGEX,
)


__all__ = (
    "ObservableObjectModel",
    "MetaDataModel",
    "CoordinateModel",
    "HeaderModel",
    "RowModel",
    "DataModel",
)


_SUN_LINE_STRENGTH_MULTIPLIER: float = 2


class ObservableObjectModel(BaseModel):
    """Model to hold basic information about observable objects."""

    model_config = ConfigDict(frozen=True)

    internal_id: LowerCase = Field(alias="id")
    aliases_: set[str] = Field(default_factory=set, alias="aliases")
    line_color: Color
    is_sun_: bool = Field(default=None, alias="is_sun")
    is_moon_: bool = Field(default=None, alias="is_moon")
    is_planet_: bool = Field(default=None, alias="is_planet")
    line_strength_: float = Field(default=2, alias="line_strength", gt=0)
    """NOTE: if the object is a sun the line_strength will get modified!"""

    @property
    def name(self) -> str:
        """Returns the name of the object (is equivalent to ``.internal_id``)."""
        return self.internal_id

    @property
    def localized_name(self) -> str:
        """Returns the localized name of the object."""
        return self.name  # ToDo: use gettext() aka _()

    @property
    def aliases(self) -> set[str]:
        """Returns given aliases including the name.

        This comes in handy when dealing with the raw (localized) data.
        """
        ret = {self.name}
        ret.update(self.aliases_)
        return ret

    @property
    def is_sun(self) -> bool:
        """
        Returns whether it's the sun.

        It's determined by setting ``is_sun`` to either True or False.
        If not set will check whether the ``internal_id`` equals "sun".
        """
        if self.is_sun_ is None:
            return self.internal_id == "sun"
        return self.is_sun_

    @property
    def is_moon(self) -> bool:
        """
        Returns whether it's the moon.

        It's determined by setting ``is_moon`` to either True or False.
        If not set will check whether the ``internal_id`` equals "moon".
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
        return self.line_strength_ * (_SUN_LINE_STRENGTH_MULTIPLIER if self.is_sun else 1)


class BoundToObservableObjectBaseModel(BaseModel):
    bound_object: ObservableObjectModel = Field(frozen=True)


class CoordinateModel(BaseModel):
    """Model to hold basic information about coordinates."""

    model_config = ConfigDict(frozen=True)

    lat: str
    lon: str

    @property
    def coordinate(self) -> str:
        """Returns combined latitude and longitude."""
        return " ".join([self.lat, self.lon])


class MetaDataModel(BaseModel):
    """Model to hold information about the metadata from the data."""

    model_config = ConfigDict(frozen=True)

    place: str
    coordinate: CoordinateModel
    equinox: float | None
    delta_t: timedelta


class HeaderModel(BaseModel):
    """Model to store basic information about."""

    model_config = ConfigDict(frozen=True)

    regex: re.Pattern[str]
    length: int = Field(ge=1)
    offset: int = Field(default=0)
    # Note: length and offset are relative to endpos of the match

    def search(self, header: str) -> re.Match[str] | None:
        """Shortcut for ``self.regex.search``."""
        return self.regex.search(header)


class RowModel(BoundToObservableObjectBaseModel, BaseModel):
    """Represents a single row from the csv-like data/table."""

    model_config = ConfigDict(frozen=True)

    date_and_time: datetime  # "Datum" & "MEZ"/"MESZ"/"UTC"
    right_ascension: str = Field(default=None, pattern=HMS_ANGLE_REGEX)  # "Rektasz."
    declination: str = Field(default=None, pattern=DMS_ANGLE_90_REGEX)  # "Deklin."
    ecliptic_longitude: str = Field(default=None, pattern=DMS_ANGLE_360_REGEX)  # "Ekl. Lg."
    ecliptic_latitude: str = Field(default=None, pattern=DMS_ANGLE_90_REGEX)  # "Ekl. Br"
    rise: str = Field(default=None, pattern=OPTIONAL_HM_TIME_REGEX)  # "Aufg."
    culmination: str = Field(default=None, pattern=OPTIONAL_HM_TIME_REGEX)  # "Kulm."
    set: str = Field(default=None, pattern=OPTIONAL_HM_TIME_REGEX)  # "Unterg"
    azimut_rise: str = Field(default=None, pattern=DEGREE_180_REGEX)  # "Az Auf"
    azimut_set: str = Field(default=None, pattern=DEGREE_360_REGEX)  # "[Az ]Unt."
    distance: float = Field(default=None)  # "Entf."
    distance_unit_: str = Field(default=None, alias="distance_unit")  # reverse engineered (from observations)
    brightness: float = Field(default=None)  # "Hell."
    diameter: float = Field(default=None, gt=0)  # "Ø [\"]"
    diameter_unit_: str = Field(default="arc second", alias="diameter_unit")  # provided as "[\"]"
    dawn: str = Field(default=None, pattern=OPTIONAL_HM_TIME_REGEX)  # "ADämm"  # sun only
    dusk: str = Field(default=None, pattern=OPTIONAL_HM_TIME_REGEX)  # "EDämm"  # sun only
    phase: float = Field(default=None, ge=-1, le=1)  # "Phase"  # moon only
    age: float = Field(default=None)  # "Alter"  # moon only
    elongation: float = Field(default=None)  # "Elong"  # planet only  # -180° <-> 180°

    # Unclear *what* they really are...
    phas_w: str = Field(default=None)  # [2]  # "Phas.W."  # unit appears to be 180° signed
    physical_ephemeris__np__or__pa_n: str = Field(default=None)  # NP | PA_N in degrees (°) [1]  # [2]  # "Pos.W."
    physical_ephemeris__sep_delta: str = Field(default=None)  # SEP(δ) in degrees (°) [1]  # [2]  # "BrErde"
    physical_ephemeris__sep_omega: str = Field(default=None)  # SEP(ω) in degrees (°) [1]  # [2]  # "ZM"  # 0° <-> 360°
    moon_specific_lib_longitude: str = Field(default=None)  # [2]  # "Lib Lg."
    moon_specific_lib_latitude: str = Field(default=None)  # [2]  # "[Lib ]Br."
    moon_specific_colong: str = Field(default=None)  # [2]  # "Colong."  # 0° <-> 360°
    moon_specific_br: str = Field(default=None)  # [2]  # "Br."
    # [1]: This was the only (remotely) helpful page I've found: https://ssp.imcce.fr/forms/physical-ephemeris
    # [2]: When and if they are used these specific arguments will get deprecated and replaced

    @property
    def distance_unit(self) -> str | None:
        """Returns the unit of ``distance`` if ``distance`` is set."""
        if self.distance is None:  # no distance set
            return None
        return self.distance_unit_ or "km" if self.bound_object.is_moon else "AU"

    @property
    def diameter_unit(self) -> str | None:
        """Returns the unit of ``diameter`` if ``diameter`` is set."""
        if self.diameter is None:  # no diameter set
            return None
        return self.diameter_unit_


class DataModel(BoundToObservableObjectBaseModel, BaseModel):
    """Represents all data connected to an observable object."""

    model_config = ConfigDict(frozen=True)

    metadata: MetaDataModel
    rows: list[RowModel]
