# third party
from annotated_types import LowerCase
from pydantic import BaseModel, PositiveFloat
from pydantic_extra_types.color import Color


__all__ = ("ObservableObjectModel",)


class ObservableObjectModel(BaseModel):  # noqa: D101  # ToDo: add documentation
    internal_id: LowerCase
    line_color: Color
    line_thickness: PositiveFloat = 2  # non-default only used by sun

    @property
    def name(self) -> str:
        """Returns the name of the object (should be equivalent to ``.internal_id``)."""
        return self.internal_id

    @property
    def localized_name(self) -> str:
        """Returns the localized name of the object."""
        return self.name  # ToDo: use gettext() aka _()
