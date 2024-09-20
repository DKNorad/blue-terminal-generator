from helpers import calculate_inner_width, STYLES


class Menu:
    """
    Prints a menu in the terminal.

    Args:
        menu_items (list):
            The menu options.
        header (str, optional):
            The menu header. Can be a string or a list of strings for
            multiple lines. Defaults to None.
        footer (str | list, optional):
            The menu footer. Can be a string or a list of strings for
            multiple lines. Defaults to None.
        numbering_type (str, optional):
            The type of numbering to use:
            - "None" - No numbering.
            - "number_dot" - 1.
            - "number_parentheses" - 1)
            - "letter_upper_dot" - A.
            - "letter_upper_parentheses" - A)
            - "letter_lower_dot" - a.
            - "letter_lower_parentheses" - b)
        center (tuple, optional):
            Whether to center parts of the menu.
            Defaults to (False, False, False).
            (a, b, c) = (header, options, footer)
            a = header center
            b = options center
            c = footer center
        min_width (int, optional):
            The minimum width of the menu. Defaults to 0.
        style (str, optional):
            The frame style to use. Defaults to "single".
        padx (tuple | int, optional):
            Padding to add around the menu parts.
            Defaults to ((0, 0), (0, 0), (0, 0)).
            (1, 1) = (left, right)
            ((1, 1), (1, 1), (1, 1)) = ((header), (footer), (options))
            1 = (1, 1)

    Raises:
        ValueError:
            If the 'menu_items' property is not a list.
        ValueError:
            If the 'header' property is not a string or a list of strings.
        ValueError:
            If the 'footer' property is not a string or a list of strings.
        ValueError:
            If the 'numbering_type' property is not a string from the list:
            "None", "number_dot", "number_parentheses", "letter_upper_dot",
            "letter_upper_parentheses", "letter_lower_dot",
            "letter_lower_parentheses".
        ValueError:
            If the 'center' property is not a tuple of length 3.
        ValueError:
            If the 'min_width' property is not an integer.
        ValueError:
            If the 'style' property is not a string.
        ValueError:
            If the 'padx' is not:
            - A single positive integer.
            - A tuple of 3 tuples, each containing 2 positive integers.
        ValueError:
            If the 'padx' property is set and the 'center' property is True for
            the same part of the menu.

    Examples:
        >>> menu = Menu(
        ...     menu_items=["Option 1", "Option 2", "Option 3", "Option 4"],
        ...     header="Main Menu",
        ...     footer="x) Exit.",
        ...     center=(True, False, False),
        ...     min_width=30,
        ...     numbering_type="letter_lower_parentheses",
        ...     padx=((0, 0), (1, 0), (1, 0))
        ... )
    """

    def __init__(
        self,
        menu_items: list,
        header: str | list = None,
        footer: str | list = None,
        numbering_type: str = "None",
        center: tuple = (False, False, False),
        min_width: int = 0,
        style: str = "single",
        padx: tuple = ((0, 0), (0, 0), (0, 0))
    ) -> None:
        self.menu_items = menu_items
        self.header = header
        self.footer = footer
        self.numbering_type = numbering_type
        self.center = center
        self.min_width = min_width
        self.style = style
        self.padx = padx
        self._inner_width = self.calculate_width()
        self._width = 0
        self._height = 0
        self._menu = self.generate_menu()

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
        elif isinstance(value, list) and all(isinstance(x, str) for x in value):
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
        elif isinstance(value, list) and all(isinstance(x, str) for x in value):
            self.__footer = value
        else:
            raise ValueError(
                "The 'footer' property must be a string or a list of strings."
            )

    @property
    def numbering_type(self) -> str:
        return self.__numbering_type

    @numbering_type.setter
    def numbering_type(self, value: str):
        valid_types = ["None", "number_dot", "number_parentheses",
                       "letter_upper_dot", "letter_upper_parentheses",
                       "letter_lower_dot", "letter_lower_parentheses"]
        if isinstance(value, str) and value in valid_types:
            self.__numbering_type = value
        else:
            raise ValueError(
                f"The 'numbering_type' property must be one of {valid_types}."
            )

    @property
    def center(self) -> bool:
        return self.__center

    @center.setter
    def center(self, value: bool):
        if isinstance(value, tuple) and all(isinstance(x, bool) for x in value):
            self.__center = value
        else:
            raise ValueError("The 'center' property must be a boolean.")

    @property
    def min_width(self) -> int:
        return self.__min_width

    @min_width.setter
    def min_width(self, value: int):
        if isinstance(value, int) and value >= 0:
            self.__min_width = value
        else:
            raise ValueError(
                "The 'min_width' property must be a non-negative integer.")

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
                f"The 'style' property must be one of {valid_styles}.")

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
        for idx, section in enumerate(['header', 'menu items', 'footer']):
            if self.__center[idx] and self.__padx[idx] != (0, 0):
                raise ValueError(
                    f"""The 'padx' for the '{section}' cannot be used
                    when 'center' is True for the same."""
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

    def calculate_width(self) -> int:
        if self.__numbering_type != "None":
            modified_menu_items = [
                f"{idx + 1}. {line}"
                for idx, line in enumerate(self.__menu_items)
            ]

        return calculate_inner_width(
            head=self.__header,
            foot=self.__footer,
            opt=(self.__menu_items if self.__numbering_type ==
                 "None" else modified_menu_items),
            minimum_width=self.__min_width,
            padx=self.__padx
        )

    def generate_menu(self) -> str:
        def format_line(line: str, centered: bool, padx: tuple) -> str:
            """Helper to format a line based on center alignment."""
            if centered:
                return (
                    f"{self.__style['v']}"
                    f"{line:^{self._inner_width}}"
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
            numbering_type_map = {
                "number_dot": f"{idx + 1}. ",
                "number_parentheses": f"{idx + 1}) ",
                "letter_lower_dot": f"{chr(ord('a') + idx)}. ",
                "letter_upper_dot": f"{chr(ord('A') + idx)}. ",
                "letter_lower_parentheses": f"{chr(ord('a') + idx)}) ",
                "letter_upper_parentheses": f"{chr(ord('A') + idx)}) "
            }
            prefix = numbering_type_map.get(self.__numbering_type, "")
            return f"{prefix}{line}"

        # Start the menu with the top line
        item = [
            f"{self.__style['tl']}"
            f"{self.__style['h'] * self._inner_width}"
            f"{self.__style['tr']}\n"
        ]

        # Get the width of the menu
        self._width = len(item[0].strip("\n"))

        # Add header lines
        if self.__header:
            for line in self.__header:
                item.append(format_line(
                    line, self.__center[0], self.__padx[0]
                ))
            item.append(
                f"{self.__style['ml']}"
                f"{self.__style['h'] * self._inner_width}"
                f"{self.__style['mr']}\n"
            )

        # Add menu items with optional numbering
        for idx, line in enumerate(self.__menu_items):
            if self.__numbering_type:
                line = add_numbering(line, idx)
            item.append(format_line(line, self.__center[1], self.__padx[1]))
        item.append(
            f"{self.__style['ml']}"
            f"{self.__style['h'] * self._inner_width}"
            f"{self.__style['mr']}\n"
        )

        # Add footer lines
        if self.__footer:
            for line in self.__footer:
                item.append(format_line(
                    line, self.__center[2], self.__padx[2]))

        # Add the bottom line
        item.append(
            f"{self.__style['bl']}"
            f"{self.__style['h'] * self._inner_width}"
            f"{self.__style['br']}"
        )

        # Get the height of the menu
        self._height = len(item)

        return "".join(item)

    @ property
    def menu(self) -> str:
        return self._menu


if __name__ == "__main__":
    pass
