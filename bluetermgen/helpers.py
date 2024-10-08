from typing import Union, Tuple


def calculate_inner_width(
    head: list,
    foot: str = None,
    opt: list = None,
    minimum_width: int = 0,
    padx: Tuple = (0, 0),
) -> int:
    """
    Help function to calculate the width of the item based on the longest
        string in the item. Used for 'message' and 'menu'.

    Args:
        header (list):
            The header to calculate the width for.

        footer (str, optional):
            The footer to calculate the width for. Defaults to `None`.

        options (list, optional):
            The menu options to calculate the width for. Defaults to `None`.

        min_width (int, optional):
            The minimum width of the item. Defaults to `0`.

        padx (tuple, optional):
            Padding to add around the `header`, `footer`, and `options`.
            Defaults to `(0, 0)`.
            - For message:
            (a, b) = (left, right)


            - For menu:
            (1, 1) = (left, right)
            ((1, 1), (1, 1), (1, 1)) = ((header), (footer), (options))
            1 = (1, 1)

    Returns:
        int: The width of the item.
    """

    if padx:
        # If padx is a list of two integers, apply to all parts
        if len(padx) == 2 and all(isinstance(x, int) for x in padx):
            lpad, rpad = padx

        # If padx has nested tuples with specific
        # paddings for head, opt, and foot
        elif len(padx) == 3 and all(
            len(p) == 2 and all(isinstance(x, int) for x in p) for p in padx
        ):
            (lpad, rpad), (opt_lpad, opt_rpad), (foot_lpad, foot_rpad) = padx

        head = [f"{' ' * lpad}{h}{' ' * rpad}" for h in head] if head else head
        opt = (
            [f"{' ' * opt_lpad}{o}{' ' * opt_rpad}" for o in opt]
            if opt
            else opt
        )
        foot = (
            [f"{' ' * foot_lpad}{f}{' ' * foot_rpad}" for f in foot]
            if foot
            else foot
        )

    max_str_width = max(
        max(len(h) for h in head) if head else 0,
        max(len(f) for f in foot) if foot else 0,
        max(len(o) for o in opt) if opt else 0,
    )

    width = (
        max_str_width if max_str_width > minimum_width else minimum_width - 2
    )

    return width


def calculate_table_inner_width(
    table_data: list,
    headers: list,
    padx: tuple,
    minimum_width: Union[int, dict],
    is_dict_table: bool,
    indexing: bool,
) -> dict:
    """
    Calculates the width for each column in the `table_data`,
    optionally applying padding.

    Args:
        table_data (list):
            The table data to calculate the width for.
            It can be a list of dictionaries or a list of lists.

            Examples:
                [
                    ["header 1", "header 2"],
                    ["row 1, col 1", "row 1, col 2"],
                    ["row 2, col 1", "row 2, col 2"],
                ]

                [
                    {"header 1": ["row 1, col 1", "row 1, col 2"]},
                    {"header 2": ["row 2, col 1", "row 2, col 2"]},
                ]

        headers (list, optional):
            The table headers.

        padx (tuple, optional):
            Padding to add around the table.

        minimum_width (int | dict, optional):
            The minimum width for all the columns or for each column.

        is_dict_table (bool, optional):
            Whether the table is a dictionary table.

        indexing (bool, optional):
            Whether the table has an index column.

    Returns:
        dict:
            The width for each column in the `'table_data'` and
            the updated `'table_data'` if padding is applied.

            Example:
            {col1: width, col2: width, ...}
    """

    column_widths = {}
    header_padx, data_padx = padx
    starting_index = 0

    # Calculate the number of rows to get the index width if set.
    if indexing:
        index_width = len(str(len(table_data)))
        column_widths[0] = index_width
        starting_index = 1

    if headers != "None":
        for col_i, header in enumerate(headers, starting_index):
            column_widths[col_i] = max(
                len(header) + sum(header_padx), minimum_width
            )

    if is_dict_table:
        for row in table_data:
            for col_i, value in enumerate(row.values(), starting_index):
                col_width = len(str(value)) + sum(data_padx)
                if col_i not in column_widths:
                    column_widths[col_i] = max(col_width, minimum_width)
                else:
                    column_widths[col_i] = max(
                        column_widths[col_i], col_width, minimum_width
                    )

    else:
        for row in table_data:
            for col_index, col_value in enumerate(row, starting_index):
                col_width = len(str(col_value)) + sum(data_padx)
                col_width = max(col_width, minimum_width)
                if col_index not in column_widths:
                    column_widths[col_index] = col_width
                else:
                    column_widths[col_index] = max(
                        column_widths[col_index], col_width, minimum_width
                    )

    return column_widths


""" Styles legend:
tl - top left
tr - top right
bl - bottom left
br - bottom right
h - horizontal
v - vertical
c - cross
ml - middle left
mr - middle right
mt - middle top
mb - middle bottom
hb - header bottom
"""

BOLD_STYLE = {
    "tl": "┏",
    "tr": "┓",
    "bl": "┗",
    "br": "┛",
    "h": "━",
    "v": "┃",
    "c": "╋",
    "ml": "┣",
    "mr": "┫",
    "mt": "┳",
    "mb": "┻",
    "hb": "╍",
}

DOUBLE_STYLE = {
    "tl": "╔",
    "tr": "╗",
    "bl": "╚",
    "br": "╝",
    "h": "═",
    "v": "║",
    "c": "╬",
    "ml": "╠",
    "mr": "╣",
    "mt": "╦",
    "mb": "╩",
    "hb": "═",
}
SINGLE_STYLE = {
    "tl": "┌",
    "tr": "┐",
    "bl": "└",
    "br": "┘",
    "h": "─",
    "v": "│",
    "c": "┼",
    "ml": "├",
    "mr": "┤",
    "mt": "┬",
    "mb": "┴",
    "hb": "╌",
}
ASCII_STYLE = {
    "tl": "+",
    "tr": "+",
    "bl": "+",
    "br": "+",
    "h": "-",
    "v": "|",
    "c": "+",
    "ml": "|",
    "mr": "|",
    "mt": "+",
    "mb": "+",
    "hb": "=",
}

STYLES = {
    "double": DOUBLE_STYLE,
    "single": SINGLE_STYLE,
    "simple": ASCII_STYLE,
    "bold": BOLD_STYLE,
}
