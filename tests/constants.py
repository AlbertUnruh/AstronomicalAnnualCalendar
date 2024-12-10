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
            right_ascension="18h42m04.3s",
            declination="-23°05'10\"",
            ecliptic_longitude="279°40'02\"",
            ecliptic_latitude="+ 0°00'12\"",
            rise="8h44m",
            culmination="12h34m",
            set="16h23m",
            azimut_rise="131°",
            azimut_set="229°",
            distance=0.98332,
            brightness=-26.8,
            diameter=1951.8,
            dawn="6h35m",
            dusk="18h32m",
            physical_ephemeris__np__or__pa_n="2.3",
            physical_ephemeris__sep_delta="-3.0",
            physical_ephemeris__sep_omega="228.0",
        ),
        RowModel(
            bound_object=ObservableObjectEnum.SUN,
            date_and_time=_day2,
            right_ascension="18h46m29.3s",
            declination="-23°00'30\"",
            ecliptic_longitude="280°41'10\"",
            ecliptic_latitude="+ 0°00'11\"",
            rise="8h44m",
            culmination="12h34m",
            set="16h24m",
            azimut_rise="131°",
            azimut_set="229°",
            distance=0.98331,
            brightness=-26.8,
            diameter=1951.8,
            dawn="6h35m",
            dusk="18h33m",
            physical_ephemeris__np__or__pa_n="1.8",
            physical_ephemeris__sep_delta="-3.1",
            physical_ephemeris__sep_omega="214.8",
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
            right_ascension="10h33m21.6s",
            declination="+12°57'52\"",
            ecliptic_longitude="155°09'37\"",
            ecliptic_latitude="+ 3°35'50\"",
            rise="22h19m",
            culmination="4h28m",
            set="11h39m",
            azimut_rise="68°",
            azimut_set="292°",
            distance=404636,
            brightness=-11.0,
            diameter=1772.1,
            phase=-0.69,
            age=-10.2,
            phas_w="-55.5",
            moon_specific_lib_longitude="0.9",
            moon_specific_lib_latitude="-4.7",
            moon_specific_colong="144.6",
            moon_specific_br="-1.5",
        ),
        RowModel(
            bound_object=ObservableObjectEnum.MOON,
            date_and_time=_day2,
            right_ascension="11h16m29.2s",
            declination="+ 7°43'11\"",
            ecliptic_longitude="166°58'50\"",
            ecliptic_latitude="+ 2°47'59\"",
            rise="23h31m",
            culmination="5h07m",
            set="11h48m",
            azimut_rise="77°",
            azimut_set="283°",
            distance=404850,
            brightness=-10.8,
            diameter=1771.1,
            phase=-0.63,
            age=-9.3,
            phas_w="-66.3",
            moon_specific_lib_longitude="-0.5",
            moon_specific_lib_latitude="-3.6",
            moon_specific_colong="156.7",
            moon_specific_br="-1.5",
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
            diameter_ring=33.1,
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
            diameter_ring=33.1,
            elongation=52.3,
            phas_w="4.6",
            physical_ephemeris__np__or__pa_n="5.9",
            physical_ephemeris__sep_delta="9.3",
            physical_ephemeris__sep_omega="72.6",
        ),
    ],
)
