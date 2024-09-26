from .helpers import calculate_inner_width, STYLES


class Menu:
    """
    Generates a menu with borders with different options.

    Args:
        menu_items (list):
            The menu options.

        header (str, optional):
            The menu header. Can be a string or a list of strings for
            multiple lines. Defaults to `""`.

        footer (str | list, optional):
            The menu footer. Can be a string or a list of strings for
            multiple lines. Defaults to `""`.

        index (str, optional):
            The type of numbering to use. Default to `None`.

            Options:
            "None" - No numbering.
            "number_dot" - 1.
            "number_parentheses" - 1)
            "letter_upper_dot" - A.
            "letter_upper_parentheses" - A)
            "letter_lower_dot" - a.
            "letter_lower_parentheses" - b)

        align (tuple, optional):
            How to align the menu parts.
            Defaults to `("left", "left", "left")`.

            Example:
            (a, b, c) = (header, options, footer)

        min_width (int, optional):
            The minimum width of the menu. Defaults to `0`.

        style (str, optional):
            The frame style to use. Defaults to `single`.

        padx (tuple | int, optional):
            Padding to add around the menu parts.
            Defaults to `((0, 0), (0, 0), (0, 0))`.

            Example:
            (1, 1) = (left, right)
            ((1, 1), (1, 1), (1, 1)) = ((header), (footer), (options))
            1 = (1, 1)

    Raises:
        ValueError:
            If the `menu_items` property is not a list.

        ValueError:
            If the `header` property is not a string or a list of strings.

        ValueError:
            If the `footer` property is not a string or a list of strings.

        ValueError:
            If the `index` property is not a string from the list:
            "None"
            "number_dot"
            "number_parentheses"
            "letter_upper_dot"
            "letter_upper_parentheses"
            "letter_lower_dot"
            "letter_lower_parentheses"

        ValueError:
            If the `align` property is not a tuple of length 3
            and any element is not part of the list:
            "left"
            "center"
            "right"

        ValueError:
            If the `min_width` property is not an integer.

        ValueError:
            If the `style` property is not a string.

        ValueError:
            If the `padx` is not:
            - A single positive integer.
            - A tuple of 3 tuples, each containing 2 positive integers.

        ValueError:
            If the `padx` property is set and the `'align'` property is
            `center` for the same part of the menu.

    Examples:
        >>> menu = Menu(
        ...     menu_items=["Option 1", "Option 2", "Option 3", "Option 4"],
        ...     header="Main Menu",
        ...     footer="x) Exit.",
        ...     align=("center", "left", "left"),
        ...     min_width=30,
        ...     index="letter_lower_parentheses",
        ...     padx=((0, 0), (1, 0), (1, 0))
        ... )
    """

    def __init__(
        self,
        menu_items: list,
        header: str | list = "",
        footer: str | list = "",
        index: str = "None",
        align: tuple = ("left", "left", "left"),
        min_width: int = 0,
        style: str = "single",
        padx: tuple = ((0, 0), (0, 0), (0, 0)),
    ) -> None:
        self.menu_items = menu_items
        self.header = header
        self.footer = footer
        self.index = index
        self.align = align
        self.min_width = min_width
        self.style = style
        self.padx = padx
        self._inner_width = self._calculate_width()
        self._width = 0
        self._height = 0
        self._menu = self._generate_menu()

    @property
    def menu_items(self) -> list:
        return self.__menu_items

    @menu_items.setter
    def menu_items(self, value: str | list):
        if isinstance(value, list) and all(isinstance(x, str) for x in value):
            self.__menu_items = value
        else:
            raise ValueError(
                "The 'menu_items' property must be a list of strings."
            )

    @property
    def header(self) -> str | list:
        return self.__header

    @header.setter
    def header(self, value: str | list):
        if isinstance(value, str):
            self.__header = value.split("\n")
        elif isinstance(value, list) and all(
            isinstance(x, str) for x in value
        ):
            self.__header = value
        else:
            raise ValueError(
                "The 'header' property must be a string or a list of strings."
            )

    @property
    def footer(self) -> str | list:
        return self.__footer

    @footer.setter
    def footer(self, value: str | list):
        if isinstance(value, str):
            self.__footer = value.split("\n")
        elif isinstance(value, list) and all(
            isinstance(x, str) for x in value
        ):
            self.__footer = value
        else:
            raise ValueError(
                "The 'footer' property must be a string or a list of strings."
            )

    @property
    def index(self) -> str:
        return self.__index

    @index.setter
    def index(self, value: str):
        valid_types = [
            "None",
            "number_dot",
            "number_parentheses",
            "letter_upper_dot",
            "letter_upper_parentheses",
            "letter_lower_dot",
            "letter_lower_parentheses",
        ]
        if isinstance(value, str) and value in valid_types:
            self.__index = value
        else:
            raise ValueError(
                f"The 'index' property must be one of {valid_types}."
            )

    @property
    def align(self) -> bool:
        return self.__align

    @align.setter
    def align(self, value: bool):
        valid_alignments = ["left", "center", "right"]
        if isinstance(value, tuple) and all(
            alignment in valid_alignments for alignment in value
        ):
            self.__align = value
        else:
            raise ValueError(
                f"The 'align' property must be one of {valid_alignments}."
            )

    @property
    def min_width(self) -> int:
        return self.__min_width

    @min_width.setter
    def min_width(self, value: int):
        if isinstance(value, int) and value >= 0:
            self.__min_width = value
        else:
            raise ValueError(
                "The 'min_width' property must be a non-negative integer."
            )

    @property
    def style(self) -> str:
        return self.__style

    @style.setter
    def style(self, value: str):
        valid_styles = list(STYLES.keys())
        if isinstance(value, str) and value in valid_styles:
            self.__style = STYLES[value]
        else:
            raise ValueError(
                f"The 'style' property must be one of {valid_styles}."
            )

    @property
    def padx(self) -> tuple:
        return self.__padx

    @padx.setter
    def padx(self, value: tuple | int):
        def validate_padx_structure(padx_tuple):
            """
            Helper function to validate that the tuple structure is correct.
            """
            return all(
                isinstance(x, tuple) and len(x) == 2 and all(n >= 0 for n in x)
                for x in padx_tuple
            )

        if isinstance(value, int) and value >= 0:
            self.__padx = ((value, value), (value, value), (value, value))
        elif (
            isinstance(value, tuple)
            and len(value) == 3
            and validate_padx_structure(value)
        ):
            self.__padx = value
        else:
            raise ValueError(
                "The 'padx' property must be either:\n"
                "- A single positive integer.\n"
                "- A tuple of 3 tuples, each containing 2 positive integers."
            )

        # Validate 'center' conflict with padding
        for idx, section in enumerate(["header", "menu items", "footer"]):
            if self.align[idx] == "center" and self.__padx[idx] != (0, 0):
                raise ValueError(
                    f"""The 'padx' for the '{section}' cannot be used
                    when 'align' is "center" for the same."""
                )

    def get_width(self) -> int:
        """
        Returns:
            int: The entire width of the menu including the borders.
        """
        return self._width

    def get_height(self) -> int:
        """
        Returns:
            int: The entire height of the menu including the borders.
        """
        return self._height

    def _calculate_width(self) -> int:
        if self.__index != "None":
            modified_menu_items = [
                f"{idx + 1}. {line}"
                for idx, line in enumerate(self.__menu_items)
            ]

        return calculate_inner_width(
            head=self.__header,
            foot=self.__footer,
            opt=(
                self.__menu_items
                if self.__index == "None"
                else modified_menu_items
            ),
            minimum_width=self.__min_width,
            padx=self.__padx,
        )

    def _generate_menu(self) -> str:
        def format_line(line: str, alignment: str, padx: tuple) -> str:
            """Helper to format a line based on alignment."""
            if alignment == "center":
                return (
                    f"{self.__style['v']}"
                    f"{line:^{self._inner_width}}"
                    f"{self.__style['v']}\n"
                )
            elif alignment == "right":
                lpadx, rpadx = padx
                return (
                    f"{self.__style['v']}"
                    f"{' ' * (self._inner_width - len(line) - rpadx)}"
                    f"{line}"
                    f"{' ' * rpadx}"
                    f"{self.__style['v']}\n"
                )
            else:
                lpadx, _ = padx
                return (
                    f"{self.__style['v']}"
                    f"{' ' * lpadx}"
                    f"{line}"
                    f"{' ' * (self._inner_width - len(line) - lpadx)}"
                    f"{self.__style['v']}\n"
                )

        def add_numbering(line: str, idx: int) -> str:
            """Helper to add numbering to a line for the menu items."""
            index_map = {
                "number_dot": f"{idx + 1}. ",
                "number_parentheses": f"{idx + 1}) ",
                "letter_lower_dot": f"{chr(ord('a') + idx)}. ",
                "letter_upper_dot": f"{chr(ord('A') + idx)}. ",
                "letter_lower_parentheses": f"{chr(ord('a') + idx)}) ",
                "letter_upper_parentheses": f"{chr(ord('A') + idx)}) ",
            }
            prefix = index_map.get(self.__index, "")
            return f"{prefix}{line}"

        # Prepare the top border
        item = [
            f"{self.__style['tl']}"
            f"{self.__style['h'] * self._inner_width}"
            f"{self.__style['tr']}\n"
        ]

        # Get the width of the menu
        self._width = len(item[0].strip("\n"))

        # Prepare the menu headers
        if self.__header[0]:
            for line in self.__header:
                item.append(format_line(line, self.__align[0], self.__padx[0]))

            # Prepare the headers bottom border
            item.append(
                f"{self.__style['ml']}"
                f"{self.__style['h'] * self._inner_width}"
                f"{self.__style['mr']}\n"
            )

        # Prepare the menu items with optional numbering
        for idx, line in enumerate(self.__menu_items):
            if self.__index:
                line = add_numbering(line, idx)
            item.append(format_line(line, self.__align[1], self.__padx[1]))

        # Prepare the footer data
        if self.__footer[0]:
            item.append(
                f"{self.__style['ml']}"
                f"{self.__style['h'] * self._inner_width}"
                f"{self.__style['mr']}\n"
            )
            for line in self.__footer:
                item.append(format_line(line, self.__align[2], self.__padx[2]))

        # Add the bottom line
        item.append(
            f"{self.__style['bl']}"
            f"{self.__style['h'] * self._inner_width}"
            f"{self.__style['br']}"
        )

        # Get the height of the menu
        self._height = len(item)

        return "".join(item)

    @property
    def menu(self) -> str:
        return self._menu

    def __str__(self) -> str:
        return self._menu


if __name__ == "__main__":
    pass
