from typing import Tuple, Union

from .helpers import STYLES, calculate_table_inner_width


class Table:
    """
    Generates a table with borders with different options.

    Args:
        table_data (list):
            The data to display in the table.

            Two types are supported:
            - A list of lists:
            [
                ["header 1", "header 2", "header 3"],
                ["r1_c1", "r1_c2", "r1_c3"],
                ["r2_c1", "r2_c2", "r2_c3"],
                ["r3_c1", "r3_c2", "r3_c3"],
            ]

            - A list of dictionaries:
            [
                {"header 1": "r1_c1", "header 2": "r1_c2", "header 3": "r1_c3"},
                {"header 1": "r2_c1", "header 2": "r2_c2", "header 3": "r2_c3"},
                {"header 1": "r3_c1", "header 2": "r3_c2", "header 3": "r3_c3"},
            ]

        headers (str | list, optional):
            The table headers. Defaults to `from_data`.

            Options:
            "None" - No headers.
            "from_data" - Get the headers from the table_data:
                - First list if the data is a list of lists.
                - Dictionary keys if the data is a list of dictionaries.
            ["header 1", "header 2", "header 3"] - Custom headers.

        index (str, optional):
            Add a column with an index for each row.

            Options:
            "None" - No index.
            "number" - 1, 2, 3, etc.

        align (tuple, optional):
            How to align the table parts. Defaults to `("left", "left")`.
            Options - left, right, center

            Overwritten by custom_align.

            Example:
            (a, b) = (headers, table_data)

        custom_align (dict, optional):
            Custom alignment for each column. Must be a dictionary with the
            column index as the key and the alignment or list of alignments as
            the value.
            Options - left, right, center

            Overwrites align.

            Example:
            {0: "center", 1: ["center", "left", "right"]}
            {col1: all rows, col2: [row1, row2, row3]}

        min_width (int | dict, optional):
            The minimum width for all the columns.
            You can also specify a value for each column.
            Defaults to `0`.

            Example:
            {0: 10, 1: 20, 2: 10, ....}
            {col1: min_width, col2: min_width, ...}

        style (str, optional):
            The table style to use. Defaults to `single`.

        padx (tuple | int, optional):
            Padding to add around the table header or data.
            Defaults to `((0, 0), (0, 0))`.
            - `((1, 1), (1, 1))` = `((header left, header right), (data left, data right))`
            - `1` = `((1, 1), (1, 1))`

        row_sep (bool, optional):
            Add a row separator between each row. Defaults to `False`.

    Raises:
        ValueError:
            If the `table_data` is not a list of lists or a list of dictionaries.

        ValueError:
            If the `headers` is not a list or a string.

        ValueError:
            If the `index` is not a string or a valid option.

            Options:
            "None" - No index column.
            "number" - 1, 2, 3, etc.

        ValueError:
            If the `align` is not a tuple of length 2 containing:
            - "left" | "center" | "right"

        ValueError:
            If the `custom_align` is not a dictionary.

        ValueError:
            If the `min_width` is not an integer or a dictionary.

        ValueError:
            If the `style` property is not a string or a valid option.
            Defaults to `single`.

        ValueError:
            If the `padx` is not a tuple or an integer.

        ValueError:
            If the `row_sep` is not a boolean.


    Example:
        >>> table = Table(
                [
        ...         ["header 1", "header 2", "header 3"],
        ...         ["r1_c1", "r1_c2", "r1_c3"],
        ...         ["r2_c1", "r2_c2", "r2_c3"],
        ...         ["r3_c1", "r3_c2", "r3_c3"],
        ...     ],
        ...     index="number",
        ...     style="single",
        ...     row_sep=True,
        ... )

    """

    def __init__(
        self,
        table_data: Union[list, dict],
        headers: Union[str, list] = "from_data",
        index: str = "None",
        align: Tuple = ("left", "left"),
        custom_align: dict = {},
        min_width: Union[int, dict] = 0,
        style: str = "single",
        padx: Tuple = ((0, 0), (0, 0)),
        row_sep: bool = False,
    ) -> None:
        self._is_dict_table = False
        self.table_data = table_data
        self.headers = headers
        self.index = index
        self.align = align
        self.custom_align = custom_align
        self.min_width = min_width
        self.style = style
        self.padx = padx
        self.row_separator = row_sep

        self._inner_width = calculate_table_inner_width(
            table_data=self.__table_data,
            headers=self.__headers,
            padx=self.__padx,
            minimum_width=self.__min_width,
            is_dict_table=self._is_dict_table,
            indexing=self.__index != "None",
        )

        self._width = 0
        self._height = 0
        self._table = self._generate_table()

    @property
    def table_data(self) -> list:
        return self.__table_data

    @table_data.setter
    def table_data(self, value: Union[list, dict]):
        # Check if the value is a list of lists with all string elements
        if isinstance(value, list) and all(
            isinstance(row, list) for row in value
        ):
            self.__table_data = value

        # Check if the value is a list of dictionaries with matching keys
        elif isinstance(value, list) and all(
            isinstance(row, dict) for row in value
        ):
            # Extract the keys of the first dictionary to check consistency
            first_keys = set(value[0].keys()) if value else set()

            if all(set(row.keys()) == first_keys for row in value):
                self.__table_data = value
                self._is_dict_table = True
            else:
                raise ValueError(
                    "All dictionaries in 'table_data' must have the same keys."
                )

        # Raise an error if neither condition is met
        else:
            raise ValueError(
                "The 'table_data' property must be a list of lists "
                "(with all strings) or a list of dictionaries"
                "(with matching keys)."
            )

    @property
    def headers(self) -> Union[str, list]:
        return self.__headers

    @headers.setter
    def headers(self, value: Union[str, list]):
        if value == "None":
            self.__headers = value
        elif value == "from_data":
            # If table_data is a list of lists, take the first list as headers
            if all(isinstance(row, list) for row in self.__table_data):
                try:
                    self.__headers = self.__table_data.pop(0)
                except IndexError:
                    self.__headers = []

            # If table_data is a list of dicts, take the keys as headers
            else:
                self.__headers = list(self.__table_data[0].keys())
        else:
            # If a custom list is provided
            if isinstance(value, list):
                self.__headers = value
            else:
                raise ValueError("The 'headers' property must be a list.")

    @property
    def index(self) -> str:
        return self.__index

    @index.setter
    def index(self, value: str):
        valid_types = [
            "None",
            "number",
        ]
        if isinstance(value, str) and value in valid_types:
            self.__index = value
        else:
            raise ValueError(
                f"The 'index' property must be one of {valid_types}."
            )

    @property
    def align(self) -> Tuple:
        return self.__align

    @align.setter
    def align(self, value: Tuple):
        if (
            isinstance(value, tuple)
            and len(value) == 2
            and all(x in ["left", "center", "right"] for x in value)
        ):
            self.__align = value
        else:
            raise ValueError(
                f"The 'align' property must be a tuple of length 2 containing"
                f"'left', 'center', or 'right'."
            )

    @property
    def custom_align(self) -> dict:
        return self.__custom_align

    @custom_align.setter
    def custom_align(self, value: dict):
        if isinstance(value, dict):
            self.__custom_align = value
        else:
            raise ValueError(
                "The 'custom_align' property must be a dictionary."
            )

    @property
    def min_width(self) -> Union[int, dict]:
        return self.__min_width

    @min_width.setter
    def min_width(self, value: Union[int, dict]):
        if isinstance(value, int):
            self.__min_width = value
        elif isinstance(value, dict):
            if len(value) > len(self.__table_data[0]):
                raise ValueError(
                    "The 'min_width' dictionary has more keys than the number of columns."
                )
            for k, v in value.items():
                if not isinstance(v, int):
                    raise ValueError(
                        "The values in the 'min_width' dictionary must be integers."
                    )
                if not isinstance(k, int):
                    raise ValueError(
                        "The keys in the 'min_width' dictionary must be integers."
                    )

            self.__min_width = value
            for i in range(len(self.__table_data[0])):
                if i not in value:
                    self.__min_width[i] = 0

        else:
            raise ValueError(
                "The 'min_width' property must be an integer or a dictionary."
            )

    @property
    def style(self) -> dict:
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
    def padx(self) -> Tuple:
        return self.__padx

    @padx.setter
    def padx(self, value: Union[Tuple, int]):
        def validate_padx_structure(padx_tuple):
            """
            Helper function to validate that the tuple structure is correct.
            """
            return all(
                isinstance(x, tuple) and len(x) == 2 and all(n >= 0 for n in x)
                for x in padx_tuple
            )

        if isinstance(value, int) and value >= 0:
            self.__padx = ((value, value), (value, value))
        elif (
            isinstance(value, tuple)
            and len(value) == 2
            and validate_padx_structure(value)
        ):
            self.__padx = value
        else:
            raise ValueError(
                "The 'padx' property must be either:\n"
                "- A single positive integer.\n"
                "- A tuple of 2 tuples, each containing 2 positive integers."
            )

        # Validate 'center' conflict with padding
        for idx, section in enumerate(["headers", "table_data"]):
            if self.align[idx] == "center" and self.__padx[idx] != (0, 0):
                raise ValueError(
                    f"The 'padx' for the '{section}' cannot be used "
                    f"when 'align' is 'center' for the same."
                )

    @property
    def row_separator(self) -> bool:
        return self.__row_separator

    @row_separator.setter
    def row_separator(self, value: bool):
        if isinstance(value, bool):
            self.__row_separator = value
        else:
            raise ValueError("The 'row_separator' property must be a boolean.")

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

    def _generate_table(self) -> str:
        def format_line(
            line: Union[str, int], alignment: str, padx: Tuple, col_index: int
        ) -> str:
            """Helper to format a line based on alignment and padding."""
            line = str(line)

            if alignment == "center":
                return f"{line:^{self._inner_width[col_index]}}"
            elif alignment == "right":
                lpadx, rpadx = padx
                return f"{' ' * (self._inner_width[col_index] - len(line) - rpadx)}{line}{' ' * rpadx}"

            else:
                lpadx, _ = padx
                return f"{' ' * lpadx}{line}{' ' * (self._inner_width[col_index] - len(line) - lpadx)}"

        # Set the starting index for the inner_width based on the index attribute
        starting_index = 1 if self.__index != "None" else 0

        # Prepare the top border
        item = [
            f"{self.__style['tl']}"
            f"{self.__style['mt'].join([self.__style['h'] * self._inner_width[i] for i in range(len(self._inner_width))])}"
            f"{self.__style['tr']}\n"
        ]

        # Get the total width of the table
        self._width = len(item[0].strip("\n"))

        # Prepare headers if any
        if self.__headers != "None":
            item.append(self.__style["v"])
            headings = (
                [" " * self._inner_width[0]] if self.__index != "None" else []
            )
            for col_i, line in enumerate(
                self.__headers, 1 if self.__index != "None" else 0
            ):
                headings.append(
                    format_line(line, self.align[0], self.__padx[0], col_i)
                )
            item.append(self.__style["v"].join(headings))
            item.append(f"{self.__style['v']}\n")

            # Add headers bottom border (no vertical lines at the end)
            item.append(
                f"{self.__style['ml']}"
                f"{self.__style['c'].join([self.__style['hb'] * self._inner_width[i] for i in range(len(self._inner_width))])}"
                f"{self.__style['mr']}\n"
            )

        # Prepare table data rows
        separators = len(self.__table_data) - 1
        for row_i, row in enumerate(self.__table_data, starting_index):
            # Start each row with a vertical border
            item.append(self.__style["v"])

            # Add index column if needed
            row_data = (
                [f"{row_i}{' ' * (self._inner_width[0] - len(str(row_i)))}"]
                if self.__index != "None"
                else []
            )

            # Handle dictionary-based tables
            if self._is_dict_table:
                for col_i, (line, column_name) in enumerate(
                    zip(row, self.__headers), starting_index
                ):
                    # Check for custom alignment.
                    if self.__custom_align and col_i in self.__custom_align:
                        if isinstance(self.__custom_align[col_i], list):
                            try:
                                alignment = self.__custom_align[col_i][row_i]
                            except IndexError:
                                alignment = self.__align[1]
                        else:
                            alignment = self.__custom_align[col_i]
                    else:
                        alignment = self.__align[1]

                    row_data.append(
                        format_line(
                            row[column_name], alignment, self.__padx[1], col_i
                        )
                    )

            # Handle list-based tables
            else:
                for col_i, line in enumerate(row, starting_index):

                    # Check for custom alignment.
                    if self.__custom_align and col_i in self.__custom_align:
                        if isinstance(self.__custom_align[col_i], list):
                            try:
                                alignment = self.__custom_align[col_i][row_i]
                            except IndexError:
                                alignment = self.__align[1]
                        else:
                            alignment = self.__custom_align[col_i]
                    else:
                        alignment = self.__align[1]

                    row_data.append(
                        format_line(line, alignment, self.__padx[1], col_i)
                    )

            item.append(self.__style["v"].join(row_data))
            item.append(f"{self.__style['v']}\n")

            # Add row separator for list table,
            # but only if it's not the last row
            if self.__row_separator and separators != 0:
                separators -= 1
                separator = (
                    f"{self.__style['ml']}"
                    f"{self.__style['c'].join([self.__style['h'] * self._inner_width[i] for i in range(len(self._inner_width))])}"
                    f"{self.__style['mr']}\n"
                )
                item.append(separator)

        # Add the table bottom border
        item.append(
            f"{self.__style['bl']}"
            f"{self.__style['mb'].join([self.__style['h'] * self._inner_width[i] for i in range(len(self._inner_width))])}"
            f"{self.__style['br']}"
        )

        # Join all the pieces together into a single string
        item = "".join(item)

        # Set table height
        self._height = len(item.split("\n"))

        return item

    @property
    def table(self) -> str:
        return self._table

    def __str__(self) -> str:
        return self._table


if __name__ == "__main__":
    pass
