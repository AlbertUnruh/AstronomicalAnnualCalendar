# third party
from annotated_types import LowerCase
from pydantic import BaseModel
from pydantic.config import ConfigDict
from pydantic.fields import Field
from pydantic.types import PositiveFloat
from pydantic_extra_types.color import Color


__all__ = ("ObservableObjectModel",)


_SUN_LINE_STRENGTH_MULTIPLIER: float = 2


class ObservableObjectModel(BaseModel):  # noqa: D101  # ToDo: add documentation
    model_config = ConfigDict(frozen=True)

    internal_id: LowerCase = Field(alias="id")
    line_color: Color
    is_sun_: bool = Field(default=None, alias="is_sun")
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
    def line_strength(self) -> PositiveFloat:
        """Returns the appropriate line-strength for the object."""
        return self.line_strength_ * (_SUN_LINE_STRENGTH_MULTIPLIER if self.is_sun else 1)
