# standard library
from datetime import timedelta

# first party
from AstronomicalAnnualCalendar.models import MetaDataModel


__all__ = ("sample_data_metadata",)


sample_data_metadata: MetaDataModel = MetaDataModel(
    place="Papenburg",
    coordinates="53°05' N    7°25' O",
    equinox=2000.0,
    delta_t=timedelta(seconds=73.9),
)
