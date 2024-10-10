# third party
from annotated_types import LowerCase
from pydantic import BaseModel, PositiveFloat
from pydantic_extra_types.color import Color


__all__ = ("ObservableObjectModel",)


_SUN_LINE_STRENGTH_MULTIPLIER: float = 2


class ObservableObjectModel(BaseModel):  # noqa: D101  # ToDo: add documentation
    internal_id: LowerCase
    line_color: Color
    _is_sun: bool = None  # ToDo: find way to have it appear available in init
    _line_strength: PositiveFloat = 2
    """NOTE: if the object is a sun the line_strength will get modified!"""

    @property
    def name(self) -> str:
        """Returns the name of the object (should be equivalent to ``.internal_id``)."""
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
        if self._is_sun is None:
            return self.internal_id == "sun"
        return self._is_sun

    @property
    def line_strength(self) -> PositiveFloat:
        """Returns the appropriate line-strength for the object."""
        return self._line_strength * (_SUN_LINE_STRENGTH_MULTIPLIER if self.is_sun else 1)
