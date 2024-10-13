# standard library
from datetime import timedelta

# first party
from AstronomicalAnnualCalendar.models import CoordinateModel, MetaDataModel


__all__ = (
    "sample_data_metadata_w_equinox",
    "sample_data_metadata_wo_equinox",
)


sample_data_metadata_w_equinox: MetaDataModel = MetaDataModel(
    place="Papenburg",
    coordinate=CoordinateModel(lat="53°05' N", lon="7°25' O"),
    equinox=2000.0,
    delta_t=timedelta(seconds=73.9),
)

sample_data_metadata_wo_equinox: MetaDataModel = sample_data_metadata_w_equinox.model_copy(update={"equinox": None})
