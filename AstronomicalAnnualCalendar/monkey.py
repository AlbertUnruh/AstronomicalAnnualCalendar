# standard library
from typing import TYPE_CHECKING

# third party
from matplotlib.text import Text
from matplotlib.transforms import Transform

if TYPE_CHECKING:
    # third party
    import numpy as np


__all__ = ("WrapText",)


class WrapText(Text):
    """
    Text-class to have a wrapping text with fixed width.

    Thanks to https://gist.github.com/dneuman/90af7551c258733954e3b1d1c17698fe
    """

    _width: float
    _width_coords: Transform | None

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        text: str = "",
        width: float = 0,
        width_coords: Transform | None = None,
        **kwargs: ...,
    ):
        super().__init__(x, y, text, wrap=True, **kwargs)
        self._width = width
        self._width_coords = width_coords

    def _get_wrap_line_width(self) -> float:
        if self._width_coords is None:
            return self._width

        a = self._width_coords.transform_point([(0, 0), (self._width, 0)])
        line_width: np.float64 = a[1][0] - a[0][0]  # type: ignore
        return line_width
