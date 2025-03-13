from typing import Union, List, Optional, Tuple
from .types import (
    StyleType,
    AlignType,
    MenuPaddingType,
    MenuAlignType,
    IndexType,
    CustomPrefixType,
    MenuItemsType,
    StyleEnum,
    AlignEnum,
    IndexEnum,
)
from .constants import (
    ERROR_MESSAGES,
    TL,
    TR,
    BL,
    BR,
    H,
    V,
    ML,
    MR,
    HB,
)
from .helpers import calculate_inner_width
from .base import BorderedElement
from .exceptions import ValidationError, PaddingError


class Menu(BorderedElement):
    """
    Generates a menu with borders and styling options.

    Args:
        menu_items (MenuItemsType):
            List of strings representing menu options.
            Each item must be a non-empty string.

        header (Union[str, List[str], None], optional):
            Menu header text. Can be:
            - A string (split on newlines)
            - A list of strings (multi-line)
            - None (no header)
            Defaults to None.

        footer (Union[str, List[str], None], optional):
            Menu footer text. Same format as header.
            Defaults to None.

        index (IndexType, optional):
            Numbering style for menu items. Options:
            - number.dot ("1.")
            - number.parentheses ("1)")
            - letter.upper.dot ("A.")
            - letter.upper.parentheses ("A)")
            - letter.lower.dot ("a.")
            - letter.lower.parentheses ("a)")
            - None (no numbering)
            Defaults to None.

        custom_index_prefix (CustomPrefixType, optional):
            List of custom prefixes for menu items.
            Must match number of menu items.
            Cannot be used with index.
            Defaults to None.

        align (MenuAlignType, optional):
            Tuple of alignments (header, items, footer).
            Each can be: "left", "center", "right"
            Defaults to ("left", "left", "left").

        min_width (int, optional):
            Minimum width of menu in characters.
            Must be non-negative.
            Defaults to 0.

        style (StyleType, optional):
            Border style to use.
            Options: "single", "double", "bold", "simple"
            Defaults to "single".

        padx (MenuPaddingType, optional):
            Horizontal padding configuration:
            - Integer for uniform padding
            - Tuple of 3 (left, right) tuples for sections
            Defaults to ((0, 0), (0, 0), (0, 0)).

    Raises:
        ValidationError:
            - Invalid menu items
            - Invalid header/footer format
            - Invalid index type
            - Invalid custom prefix
            - Invalid alignment
            - Invalid minimum width
            - Index and custom prefix conflict

        PaddingError:
            - Invalid padding format
            - Padding conflicts with center alignment

    Example:
        >>> menu = Menu(
        ...     menu_items=["New Game", "Load Game", "Settings", "Exit"],
        ...     header="Main Menu",
        ...     footer="Use arrow keys to navigate",
        ...     index=IndexEnum.NUMBER_DOT.value,
        ...     align=("center", "left", "right"),
        ...     min_width=30,
        ...     style="double",
        ...     padx=((0, 0), (2, 1), (1, 1))
        ... )
        >>> print(menu)
    """

    def __init__(
        self,
        menu_items: MenuItemsType,
        header: Union[str, List[str], None] = None,
        footer: Union[str, List[str], None] = None,
        index: IndexType = None,
        custom_index_prefix: CustomPrefixType = None,
        align: MenuAlignType = (
            AlignEnum.LEFT.value,
            AlignEnum.LEFT.value,
            AlignEnum.LEFT.value,
        ),
        min_width: int = 0,
        style: StyleType = StyleEnum.SINGLE.value,
        padx: MenuPaddingType = ((0, 0), (0, 0), (0, 0)),
    ) -> None:
        """Initialize a menu with the specified configuration."""
        # Initialize parent class
        super().__init__(style=style)

        # Validate index and custom prefix conflict
        if index and custom_index_prefix:
            raise ValidationError(
                ERROR_MESSAGES["MENU"]["PREFIX_INDEX_CONFLICT"].format(
                    prefix=custom_index_prefix, index=index
                )
            )

        # Set and validate properties
        self.menu_items = menu_items
        self.header = self._process_text(header) if header else None
        self.footer = self._process_text(footer) if footer else None
        self.index = index
        self.custom_index_prefix = custom_index_prefix
        self.align = align
        self.min_width = min_width
        self.padx = padx

        # Calculate dimensions and generate content
        self._inner_width = self._calculate_width()
        self._content = self._generate_menu()

    def _process_text(self, text: Union[str, List[str]]) -> List[str]:
        """
        Process text input into a list of strings.

        Args:
            text: String or list of strings to process.

        Returns:
            List of strings, with any string input split on newlines.

        Raises:
            ValidationError: If text format is invalid.
        """
        try:
            if isinstance(text, str):
                return text.split("\n")
            elif isinstance(text, list) and all(
                isinstance(x, str) for x in text
            ):
                return text
            raise ValidationError(
                ERROR_MESSAGES["MENU"]["INVALID_TEXT"].format(
                    value=f"{type(text).__name__}"
                )
            )
        except Exception as e:
            raise ValidationError(
                ERROR_MESSAGES["MENU"]["INVALID_TEXT"].format(value=str(e))
            ) from e

    def _calculate_width(self) -> int:
        """
        Calculate the inner width of the menu.

        Returns:
            The calculated inner width considering all content and padding.
        """
        modified_items = []

        if self.index is not None:
            modified_items = [
                self._add_numbering(line, idx)
                for idx, line in enumerate(self.menu_items)
            ]
        elif self.custom_index_prefix is not None:
            if len(self.custom_index_prefix) != len(self.menu_items):
                raise ValidationError(
                    ERROR_MESSAGES["MENU"]["INVALID_PREFIX"].format(
                        value=f"expected {len(self.menu_items)} prefixes, got {len(self.custom_index_prefix)}"
                    )
                )
            modified_items = [
                f"{prefix} {line}"
                for prefix, line in zip(
                    self.custom_index_prefix, self.menu_items
                )
            ]
        else:
            modified_items = self.menu_items.copy()

        return calculate_inner_width(
            head=self.header,
            foot=self.footer,
            opt=modified_items,
            minimum_width=self.min_width,
            padx=self.padx,
        )

    def _add_numbering(self, text: str, index: int) -> str:
        """
        Add numbering or custom prefix to a menu item.

        Args:
            text: The menu item text.
            index: The index of the item in the menu.

        Returns:
            Formatted string with appropriate prefix.

        Notes:
            CLI menu numbering:
            - Single digit (1-9): Quick access for most common options
            - Two digits (01-99): Standard menu items
            - Three digits (100+): Extended menu items

            When using letter-based indexing:
            - Single letter (a-z): First 26 items
            - Two digits (01-99): Next 99 items
            - Three digits (100+): Extended items
        """
        if self.custom_index_prefix:
            try:
                return f"{self.custom_index_prefix[index]} {text}"
            except IndexError:
                return text

        # Handle number-based indexing
        if self.index in [
            IndexEnum.NUMBER_DOT.value,
            IndexEnum.NUMBER_PARENTHESES.value,
        ]:
            if index < 9:
                # Single digit for quick access (1-9)
                prefix = str(index + 1)
            elif index < 99:
                # Two digits for standard items (01-99)
                prefix = f"{index + 1:02d}"
            else:
                # Three digits for extended items (100+)
                prefix = f"{index + 1:03d}"

            suffix = "." if self.index == IndexEnum.NUMBER_DOT.value else ")"
            return f"{prefix}{suffix} {text}"

        # Handle letter-based indexing
        elif self.index in [
            IndexEnum.LETTER_UPPER_DOT.value,
            IndexEnum.LETTER_UPPER_PARENTHESES.value,
            IndexEnum.LETTER_LOWER_DOT.value,
            IndexEnum.LETTER_LOWER_PARENTHESES.value,
        ]:
            is_upper = self.index in [
                IndexEnum.LETTER_UPPER_DOT.value,
                IndexEnum.LETTER_UPPER_PARENTHESES.value,
            ]
            is_dot = self.index in [
                IndexEnum.LETTER_UPPER_DOT.value,
                IndexEnum.LETTER_LOWER_DOT.value,
            ]

            if index < 26:
                # Single letter for first 26 items
                prefix = chr(65 + index if is_upper else 97 + index)
            elif index < 99:
                # Two digits for next 99 items (01-99)
                prefix = f"{index - 25:02d}"
            else:
                # Three digits for extended items (100+)
                prefix = f"{index - 25:03d}"

            suffix = "." if is_dot else ")"
            return f"{prefix}{suffix} {text}"

        return text

    def _format_line(
        self, text: str, align: AlignType, padding: Tuple[int, int]
    ) -> str:
        """
        Format a line of text with alignment and padding.

        Args:
            text: Text to format.
            align: Alignment to use.
            padding: (left, right) padding values.

        Returns:
            Formatted line with borders, alignment, and padding.
        """
        lpad, rpad = padding

        if align == AlignEnum.CENTER.value:
            formatted = f"{text:^{self._inner_width}}"
        elif align == AlignEnum.RIGHT.value:
            padding_left = " " * (self._inner_width - len(text) - rpad)
            padding_right = " " * rpad
            formatted = f"{padding_left}{text}{padding_right}"
        else:  # LEFT alignment
            padding_left = " " * lpad
            padding_right = " " * (self._inner_width - len(text) - lpad)
            formatted = f"{padding_left}{text}{padding_right}"

        return f"{self.style[V]}{formatted}{self.style[V]}\n"

    @property
    def menu_items(self) -> MenuItemsType:
        """Get the list of menu items."""
        return self._menu_items

    @menu_items.setter
    def menu_items(self, value: MenuItemsType) -> None:
        """
        Set and validate menu items.

        Args:
            value: List of strings for menu items.

        Raises:
            ValidationError: If value is not a list of non-empty strings.
        """
        if not isinstance(value, list):
            raise ValidationError(
                ERROR_MESSAGES["MENU"]["INVALID_OPTIONS"].format(
                    value=f"{type(value).__name__}"
                )
            )

        if not value:
            raise ValidationError(
                ERROR_MESSAGES["MENU"]["EMPTY_MENU"].format(value="empty list")
            )

        if not all(isinstance(x, str) for x in value):
            raise ValidationError(
                ERROR_MESSAGES["MENU"]["INVALID_OPTIONS"].format(
                    value="list contains non-string items"
                )
            )

        self._menu_items = value

    @property
    def header(self) -> Optional[List[str]]:
        """Get the menu header text."""
        return self._header

    @header.setter
    def header(self, value: Optional[Union[str, List[str]]]) -> None:
        """
        Set and validate the menu header.

        Args:
            value: String, list of strings, or None for the header.

        Raises:
            ValidationError: If value format is invalid.
        """
        if value is None:
            self._header = None
            return

        if isinstance(value, str):
            self._header = value.split("\n")
        elif isinstance(value, list) and all(
            isinstance(x, str) for x in value
        ):
            self._header = value
        else:
            raise ValidationError(
                ERROR_MESSAGES["MENU"]["INVALID_HEADER"].format(
                    value=f"{type(value).__name__}"
                )
            )

    @property
    def footer(self) -> Optional[List[str]]:
        """Get the menu footer text."""
        return self._footer

    @footer.setter
    def footer(self, value: Optional[Union[str, List[str]]]) -> None:
        """
        Set and validate the menu footer.

        Args:
            value: String, list of strings, or None for the footer.

        Raises:
            ValidationError: If value format is invalid.
        """
        if value is None:
            self._footer = None
            return

        if isinstance(value, str):
            self._footer = value.split("\n")
        elif isinstance(value, list) and all(
            isinstance(x, str) for x in value
        ):
            self._footer = value
        else:
            raise ValidationError(
                ERROR_MESSAGES["MENU"]["INVALID_FOOTER"].format(
                    value=f"{type(value).__name__}"
                )
            )

    @property
    def index(self) -> IndexType:
        """Get the current index type."""
        return self._index

    @index.setter
    def index(self, value: IndexType) -> None:
        """
        Set and validate the index type.

        Args:
            value: Index type from IndexEnum or None.

        Raises:
            ValidationError: If value is invalid.
        """
        if value is not None and value not in IndexEnum.list():
            raise ValidationError(
                ERROR_MESSAGES["MENU"]["INVALID_INDEX"].format(value=value)
            )
        self._index = value

    @property
    def custom_index_prefix(self) -> CustomPrefixType:
        """Get the custom index prefixes."""
        return self._custom_index_prefix

    @custom_index_prefix.setter
    def custom_index_prefix(self, value: CustomPrefixType) -> None:
        """
        Set and validate custom index prefixes.

        Args:
            value: List of prefix strings or None.

        Raises:
            ValidationError: If value format is invalid.
        """
        if value is not None:
            if not isinstance(value, list):
                raise ValidationError(
                    ERROR_MESSAGES["MENU"]["INVALID_PREFIX"].format(
                        value=f"{type(value).__name__}"
                    )
                )
            if not all(isinstance(x, str) for x in value):
                raise ValidationError(
                    ERROR_MESSAGES["MENU"]["INVALID_PREFIX"].format(
                        value="list contains non-string items"
                    )
                )
        self._custom_index_prefix = value

    @property
    def align(self) -> MenuAlignType:
        """Get the alignment configuration."""
        return self._align

    @align.setter
    def align(self, value: MenuAlignType) -> None:
        """
        Set and validate the alignment configuration.

        Args:
            value: Tuple of three alignment values.

        Raises:
            ValidationError: If alignment format or values are invalid.
        """
        if not isinstance(value, tuple) or len(value) != 3:
            raise ValidationError(
                ERROR_MESSAGES["MENU"]["INVALID_ALIGN"].format(
                    value=f"{type(value).__name__} of length {len(value) if isinstance(value, tuple) else 'N/A'}"
                )
            )

        valid_alignments = [e.value for e in AlignEnum]
        if not all(a in valid_alignments for a in value):
            raise ValidationError(
                ERROR_MESSAGES["MENU"]["INVALID_ALIGN"].format(
                    value=f"contains invalid alignment(s): {value}"
                )
            )
        self._align = value

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
    def padx(self) -> MenuPaddingType:
        """Get the padding configuration."""
        return self._padx

    @padx.setter
    def padx(self, value: MenuPaddingType) -> None:
        """
        Set and validate the padding configuration.

        Args:
            value: Integer or tuple of three (left, right) padding tuples.

        Raises:
            PaddingError: If padding is invalid or conflicts with alignment.
        """
        if isinstance(value, int):
            if value < 0:
                raise PaddingError(
                    ERROR_MESSAGES["MENU"]["INVALID_PADDING"].format(
                        value=value
                    )
                )
            self._padx = ((value, value), (value, value), (value, value))
        elif (
            isinstance(value, tuple)
            and len(value) == 3
            and all(
                isinstance(x, tuple)
                and len(x) == 2
                and all(isinstance(n, int) and n >= 0 for n in x)
                for x in value
            )
        ):
            self._padx = value
        else:
            raise PaddingError(
                ERROR_MESSAGES["MENU"]["INVALID_PADDING"].format(
                    value=f"{type(value).__name__}"
                )
            )

        # Check for center alignment conflicts
        sections = ["header", "items", "footer"]
        for idx, section in enumerate(sections):
            if self.align[idx] == AlignEnum.CENTER.value and self._padx[
                idx
            ] != (0, 0):
                raise PaddingError(
                    ERROR_MESSAGES["MENU"]["CENTER_PADDING_CONFLICT"].format(
                        section=section, value=self._padx[idx]
                    )
                )

    def _generate_menu(self) -> str:
        """
        Generate the complete formatted menu.

        Returns:
            Formatted menu string with borders, content, and styling.
        """
        # Initialize with top border
        lines = [
            f"{self.style[TL]}{self.style[H] * self._inner_width}{self.style[TR]}\n"
        ]

        # Store total width
        self._width = len(lines[0].strip("\n"))

        # Add header if present
        if self.header:
            for line in self.header:
                lines.append(
                    self._format_line(line, self.align[0], self.padx[0])
                )
            # Add header separator
            lines.append(
                f"{self.style[ML]}{self.style[HB] * self._inner_width}{self.style[MR]}\n"
            )

        # Add menu items
        for idx, line in enumerate(self.menu_items):
            if self.index or self.custom_index_prefix:
                line = self._add_numbering(line, idx)
            lines.append(self._format_line(line, self.align[1], self.padx[1]))

        # Add footer if present
        if self.footer:
            # Add footer separator
            lines.append(
                f"{self.style[ML]}{self.style[H] * self._inner_width}{self.style[MR]}\n"
            )
            # Add footer content
            for line in self.footer:
                lines.append(
                    self._format_line(line, self.align[2], self.padx[2])
                )

        # Add bottom border
        lines.append(
            f"{self.style[BL]}{self.style[H] * self._inner_width}{self.style[BR]}"
        )

        # Store height and return joined content
        self._height = len(lines)
        return "".join(lines)

    @property
    def menu(self) -> str:
        """Get the complete formatted menu."""
        return self._content

    def __str__(self) -> str:
        """Get string representation of the menu."""
        return self._content


if __name__ == "__main__":
    pass
