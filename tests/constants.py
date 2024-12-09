# standard library
from datetime import datetime, timedelta, timezone

# first party
from AstronomicalAnnualCalendar.enums import ObservableObjectEnum
from AstronomicalAnnualCalendar.models import CoordinateModel, DataModel, MetaDataModel, RowModel


__all__ = (
    "sample_data_metadata_w_equinox",
    "sample_data_metadata_wo_equinox",
    "sample_data_moon",
    "sample_data_saturn",
    "sample_data_sun",
)


sample_data_metadata_w_equinox: MetaDataModel = MetaDataModel(
    place="Papenburg",
    coordinate=CoordinateModel(lat="53°05' N", lon="7°25' O"),
    equinox=2000.0,
    delta_t=timedelta(seconds=73.9),
)

sample_data_metadata_wo_equinox: MetaDataModel = sample_data_metadata_w_equinox.model_copy(update={"equinox": None})


_tz: timezone = timezone(timedelta(hours=1))  # MEZ
_day1: datetime = datetime(2024, 1, 1, 0, 0, 0, tzinfo=_tz)
_day2: datetime = datetime(2024, 1, 2, 0, 0, 0, tzinfo=_tz)


sample_data_sun: DataModel = DataModel(
    bound_object=ObservableObjectEnum.SUN,
    metadata=sample_data_metadata_w_equinox,
    rows=[],
)
sample_data_moon: DataModel = DataModel(
    bound_object=ObservableObjectEnum.MOON,
    metadata=sample_data_metadata_w_equinox,
    rows=[],
)
sample_data_saturn: DataModel = DataModel(
    bound_object=ObservableObjectEnum.SATURN,
    metadata=sample_data_metadata_w_equinox,
    rows=[
        RowModel(
            bound_object=ObservableObjectEnum.SATURN,
            date_and_time=_day1,
            right_ascension="22h21m50.2s",
            declination="-11°57'39\"",
            ecliptic_longitude="332°54'29\"",
            ecliptic_latitude="- 1°37'58\"",
            rise="11h21m",
            culmination="16h16m",
            set="21h10m",
            azimut_rise="110°",
            azimut_set="250°",
            distance=10.29415,
            brightness=0.9,
            diameter=14.3,
            elongation=53.3,
            phas_w="4.6",
            physical_ephemeris__np__or__pa_n="5.9",
            physical_ephemeris__sep_delta="9.3",
            physical_ephemeris__sep_omega="308.5",
        ),
        RowModel(
            bound_object=ObservableObjectEnum.SATURN,
            date_and_time=_day2,
            right_ascension="22h22m10.4s",
            declination="-11°55'39\"",
            ecliptic_longitude="332°59'50\"",
            ecliptic_latitude="- 1°37'54\"",
            rise="11h17m",
            culmination="16h12m",
            set="21h07m",
            azimut_rise="110°",
            azimut_set="250°",
            distance=10.30734,
            brightness=0.9,
            diameter=14.3,
            elongation=52.3,
            phas_w="4.6",
            physical_ephemeris__np__or__pa_n="5.9",
            physical_ephemeris__sep_delta="9.3",
            physical_ephemeris__sep_omega="72.6",
        ),
    ],
)
