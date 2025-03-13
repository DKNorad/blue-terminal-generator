from typing import List
from .types import (
    StyleType,
    AlignType,
    MessagePaddingType,
    StyleEnum,
    AlignEnum,
    MessageTextType,
)
from .constants import ERROR_MESSAGES, TL, TR, BL, BR, H, V
from .base import BorderedElement
from .exceptions import ValidationError, PaddingError
from .helpers import calculate_inner_width


class Message(BorderedElement):
    """
    Generates a message with borders and styling options.

    Args:
        message_text (MessageTextType):
            The text for the message. Can be either:
            - A string (will be split on newlines)
            - A list of strings (each string is a line)

        align (AlignType, optional):
            Text alignment. Defaults to AlignEnum.LEFT.value
            Valid options: left, center, right

        min_width (int, optional):
            Minimum width of the frame. Defaults to 0
            Must be a non-negative integer

        style (StyleType, optional):
            Border style to use. Defaults to StyleEnum.SINGLE.value
            Valid options: single, double, bold, simple

        padx (MessagePaddingType, optional):
            Horizontal padding around text. Defaults to (0, 0)
            Can be either:
            - A positive integer for uniform padding
            - A tuple (left_pad, right_pad) for custom padding

    Raises:
        ValidationError: For invalid text, width, or alignment
        PaddingError: For invalid padding or padding/alignment conflicts

    Examples:
        >>> # Single line message
        >>> msg1 = Message("Hello World!", align="center")

        >>> # Multi-line message with custom style
        >>> msg2 = Message(
        ...     ["Header", "Content", "Footer"],
        ...     style="double",
        ...     min_width=20
        ... )

        >>> # Message with padding
        >>> msg3 = Message(
        ...     "Padded text",
        ...     padx=(2, 1),
        ...     style="bold"
        ... )
    """

    def __init__(
        self,
        message_text: MessageTextType,
        align: AlignType = AlignEnum.LEFT.value,
        min_width: int = 0,
        style: StyleType = StyleEnum.SINGLE.value,
        padx: MessagePaddingType = (0, 0),
    ) -> None:
        """Initialize a message with the specified configuration."""
        super().__init__(style=style, align=align)

        # Set properties with validation
        self.message_text = message_text
        self.min_width = min_width
        self.padx = padx

        # Calculate dimensions and generate content
        self._inner_width = self._calculate_width()
        self._content = self._generate_message()

    @property
    def message_text(self) -> List[str]:
        """Get the current message text as a list of strings."""
        return self._message_text

    @message_text.setter
    def message_text(self, value: MessageTextType) -> None:
        """
        Set and validate the message text.

        Args:
            value: String or list of strings for the message.

        Raises:
            ValidationError: If text is invalid or empty.
        """
        # First validate the type
        if not isinstance(value, (str, list)):
            raise ValidationError(
                ERROR_MESSAGES["MESSAGE"]["INVALID_TEXT"].format(
                    value=f"{type(value).__name__}"
                )
            )

        # Convert string to list of strings
        if isinstance(value, str):
            text_lines = value.split("\n")
        else:
            # Validate all items in list are strings
            if not all(isinstance(x, str) for x in value):
                raise ValidationError(
                    ERROR_MESSAGES["MESSAGE"]["INVALID_TEXT"].format(
                        value="list with non-string items"
                    )
                )
            text_lines = value

        # Check for empty message
        if not any(line.strip() for line in text_lines):
            raise ValidationError(
                ERROR_MESSAGES["MESSAGE"]["EMPTY_MESSAGE"].format(
                    value="empty text"
                )
            )

        self._message_text = text_lines

    @property
    def min_width(self) -> int:
        """Get the minimum width setting."""
        return self._min_width

    @min_width.setter
    def min_width(self, value: int) -> None:
        """
        Set and validate the minimum width.

        Args:
            value: Minimum width value.

        Raises:
            ValidationError: If width is invalid.
        """
        if not isinstance(value, int):
            raise ValidationError(
                ERROR_MESSAGES["COMMON"]["INVALID_TYPE"].format(
                    expected_type="integer", value=f"{type(value).__name__}"
                )
            )

        if value < 0:
            raise ValidationError(
                ERROR_MESSAGES["COMMON"]["INVALID_MIN_WIDTH"].format(
                    value=value
                )
            )

        self._min_width = value

    @property
    def padx(self) -> MessagePaddingType:
        """Get the current padding configuration."""
        return self._padx

    @padx.setter
    def padx(self, value: MessagePaddingType) -> None:
        """
        Set and validate the padding configuration.

        Args:
            value: Padding value(s).

        Raises:
            PaddingError: If padding is invalid or conflicts with alignment.
        """
        # Handle single integer case
        if isinstance(value, int):
            if value < 0:
                raise PaddingError(
                    ERROR_MESSAGES["MESSAGE"]["INVALID_PADDING"].format(
                        value=value
                    )
                )
            self._padx = (value, value)

        # Handle tuple case
        elif isinstance(value, tuple):
            if (
                len(value) != 2
                or not all(isinstance(x, int) for x in value)
                or not all(x >= 0 for x in value)
            ):
                raise PaddingError(
                    ERROR_MESSAGES["MESSAGE"]["INVALID_PADDING"].format(
                        value=value
                    )
                )
            self._padx = value

        else:
            raise PaddingError(
                ERROR_MESSAGES["MESSAGE"]["INVALID_PADDING"].format(
                    value=f"{type(value).__name__}"
                )
            )

        # Check for center alignment conflict
        if self.align == AlignEnum.CENTER.value and any(
            x > 0 for x in self._padx
        ):
            raise PaddingError(
                ERROR_MESSAGES["MESSAGE"]["CENTER_PADDING_CONFLICT"].format(
                    value=self._padx
                )
            )

    def _calculate_width(self) -> int:
        """
        Calculate the inner width of the message frame.

        Returns:
            The calculated inner width.
        """
        return calculate_inner_width(
            head=self._message_text,
            minimum_width=self._min_width,
            padx=self._padx,
        )

    def _generate_message(self) -> str:
        """
        Generate the formatted message with borders and alignment.

        Returns:
            The complete formatted message string.
        """
        # Start with top border
        lines = [
            f"{self.style[TL]}{self.style[H] * self._inner_width}{self.style[TR]}\n"
        ]

        # Store total width
        self._width = len(lines[0].strip("\n"))

        # Add each line of text
        for line in self._message_text:
            if self.align == AlignEnum.CENTER.value:
                formatted_line = f"{line:^{self._inner_width}}"
            elif self.align == AlignEnum.RIGHT.value:
                pad_left = self._inner_width - len(line) - self._padx[1]
                formatted_line = f"{' ' * pad_left}{line}{' ' * self._padx[1]}"
            else:  # LEFT alignment
                pad_right = self._inner_width - len(line) - self._padx[0]
                formatted_line = (
                    f"{' ' * self._padx[0]}{line}{' ' * pad_right}"
                )

            lines.append(f"{self.style[V]}{formatted_line}{self.style[V]}\n")

        # Add bottom border
        lines.append(
            f"{self.style[BL]}{self.style[H] * self._inner_width}{self.style[BR]}"
        )

        # Store height and return joined lines
        self._height = len(lines)
        return "".join(lines)

    @property
    def message(self) -> str:
        """Get the complete formatted message."""
        return self._content

    def __str__(self) -> str:
        """Get string representation of the message."""
        return self._content


if __name__ == "__main__":
    pass
