# standard library
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
    "DataModel",
    "CoordinateModel",
    "HeaderModel",
)


_SUN_LINE_STRENGTH_MULTIPLIER: float = 2


class ObservableObjectModel(BaseModel):  # noqa: D101  # ToDo: add documentation
    model_config = ConfigDict(frozen=True)

    internal_id: LowerCase = Field(alias="id")
    line_color: Color
    is_sun_: bool = Field(default=None, alias="is_sun")
    is_moon_: bool = Field(default=None, alias="is_moon")
    line_strength_: PositiveFloat = Field(default=2, alias="line_strength")
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
    def line_strength(self) -> PositiveFloat:
        """Returns the appropriate line-strength for the object."""
        return self.line_strength_ * (_SUN_LINE_STRENGTH_MULTIPLIER if self.is_sun else 1)


class BoundToObservableObjectBaseModel(BaseModel):
    bound_object: ObservableObjectModel = Field(frozen=True)


class CoordinateModel(BaseModel):  # noqa: D101  # ToDo: add documentation
    lat: str
    lon: str

    @property
    def coordinate(self) -> str:
        """Returns combined latitude and longitude."""
        return " ".join([self.lat, self.lon])


class MetaDataModel(BaseModel):  # noqa: D101  # ToDo: add documentation
    place: str
    coordinate: CoordinateModel
    equinox: float | None
    delta_t: timedelta


class DataModel(BoundToObservableObjectBaseModel, BaseModel):  # noqa: D101  # ToDo: add documentation
    metadata: MetaDataModel


# "header" refers to the top of the table/csv
class HeaderModel(BoundToObservableObjectBaseModel, BaseModel):  # noqa: D101  # ToDo: add documentation
    date_and_time: datetime  # "Datum" & "MEZ" *or other timezone*
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
    elongation: float = Field(default=None)  # "Elong"  # planet only

    # Unclear *what* they really are...
    physical_ephemeris__np__or__pa_n: str = Field(default=None)  # NP | PA_N in degrees (°) [1]  # [2]  # "Pos.W."
    physical_ephemeris__sep_delta: str = Field(default=None)  # SEP(δ) in degrees (°) [1]  # [2]  # "BrErde"
    physical_ephemeris__sep_omega: str = Field(default=None)  # SEP(ω) in degrees (°) [1]  # [2]  # "ZM"
    moon_specific_phas_w: str = Field(default=None)  # [2]  # "Phas.W."
    moon_specific_lib_longitude: str = Field(default=None)  # [2]  # "Lib Lg."
    moon_specific_lib_latitude: str = Field(default=None)  # [2]  # "[Lib ]Br."
    moon_specific_colong: str = Field(default=None)  # [2]  # "Colong."
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
