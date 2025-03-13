from typing import Tuple
from .types import StyleType, AlignType, BorderDict, StyleEnum, AlignEnum
from .exceptions import ValidationError, StyleError
from .constants import ERROR_MESSAGES, STYLES


class BorderedElement:
    """
    Base class for bordered UI elements.

    Provides common functionality for Message, Menu, and Table classes including
    border styling, alignment, and dimension calculations.

    Args:
        style (StyleType):
            Border style to use. Defaults to StyleEnum.SINGLE.value
            Valid options: single, double, bold, simple

        align (AlignType):
            Text alignment. Defaults to AlignEnum.LEFT.value
            Valid options: left, center, right

    Raises:
        StyleError: If style is not a valid style option
        ValidationError: If align is not a valid alignment option
    """

    def __init__(
        self,
        style: StyleType = StyleEnum.SINGLE.value,
        align: AlignType = AlignEnum.LEFT.value,
    ) -> None:
        """Initialize a bordered element with style and alignment."""
        # Initialize dimensions and content
        self._width: int = 0
        self._height: int = 0
        self._inner_width: int = 0
        self._content: str = ""

        # Validate and set style and alignment
        self._validate_and_set_style(style)
        self._validate_and_set_align(align)

    def _validate_and_set_style(self, style: StyleType) -> None:
        """
        Validate and set the border style.

        Args:
            style: Border style to use from StyleEnum options.

        Raises:
            StyleError: If the style is not valid.
        """
        if not isinstance(style, str):
            raise StyleError(
                ERROR_MESSAGES["COMMON"]["INVALID_TYPE"].format(
                    expected_type="string",
                    value=f"{type(style).__name__}",
                )
            )

        if style not in STYLES:
            raise StyleError(
                ERROR_MESSAGES["COMMON"]["INVALID_STYLE"].format(value=style)
            )

        self._style = STYLES[style]

    def _validate_and_set_align(self, align: AlignType) -> None:
        """
        Validate and set the text alignment.

        Args:
            align: Text alignment to use from AlignEnum options.

        Raises:
            ValidationError: If the alignment is not valid.
        """
        if not isinstance(align, str):
            raise ValidationError(
                ERROR_MESSAGES["COMMON"]["INVALID_TYPE"].format(
                    expected_type="string", value=f"{type(align).__name__}"
                )
            )

        valid_alignments = [e.value for e in AlignEnum]
        if align not in valid_alignments:
            raise ValidationError(
                ERROR_MESSAGES["COMMON"]["INVALID_ALIGN"].format(value=align)
            )

        self._align = align

    @property
    def style(self) -> BorderDict:
        """Get the current border style configuration."""
        return self._style

    @property
    def align(self) -> AlignType:
        """Get the current text alignment setting."""
        return self._align

    @property
    def width(self) -> int:
        """Get the total width of the element."""
        return self._width

    @property
    def height(self) -> int:
        """Get the total height of the element."""
        return self._height

    @property
    def inner_width(self) -> int:
        """Get the inner width (excluding borders) of the element."""
        return self._inner_width

    def get_dimensions(self) -> Tuple[int, int]:
        """
        Get the element's dimensions.

        Returns:
            Tuple containing (width, height) of the element.
        """
        return self._width, self._height

    def _format_line(self, text: str, width: int) -> str:
        """
        Format a line of text according to current alignment.

        Args:
            text: The text to format.
            width: The total width to format within.

        Returns:
            The formatted text string.
        """
        if not isinstance(text, str):
            text = str(text)

        if self._align == AlignEnum.CENTER.value:
            return f"{text:^{width}}"
        elif self._align == AlignEnum.RIGHT.value:
            return f"{text:>{width}}"
        return f"{text:<{width}}"

    def __str__(self) -> str:
        """
        Get the string representation of the element.

        Returns:
            The formatted content string.
        """
        return self._content
