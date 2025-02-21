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
    rows=[
        RowModel(
            bound_object=ObservableObjectEnum.SUN,
            date_and_time=_day1,
            culmination=timedelta(hours=12, minutes=34),
        ),
        RowModel(
            bound_object=ObservableObjectEnum.SUN,
            date_and_time=_day2,
            culmination=timedelta(hours=12, minutes=34),
        ),
    ],
)
sample_data_moon: DataModel = DataModel(
    bound_object=ObservableObjectEnum.MOON,
    metadata=sample_data_metadata_w_equinox,
    rows=[
        RowModel(
            bound_object=ObservableObjectEnum.MOON,
            date_and_time=_day1,
            culmination=timedelta(hours=4, minutes=28),
        ),
        RowModel(
            bound_object=ObservableObjectEnum.MOON,
            date_and_time=_day2,
            culmination=timedelta(hours=5, minutes=7),
        ),
    ],
)
sample_data_saturn: DataModel = DataModel(
    bound_object=ObservableObjectEnum.SATURN,
    metadata=sample_data_metadata_w_equinox,
    rows=[
        RowModel(
            bound_object=ObservableObjectEnum.SATURN,
            date_and_time=_day1,
            culmination=timedelta(hours=16, minutes=16),
        ),
        RowModel(
            bound_object=ObservableObjectEnum.SATURN,
            date_and_time=_day2,
            culmination=timedelta(hours=16, minutes=12),
        ),
    ],
)
