from typing import Union, Dict, List, Tuple
from .types import (
    SinglePaddingType,
    MenuPaddingType,
    TablePaddingType,
    TableHeaderType,
    TableMinWidthType,
    TableDataType,
)


def calculate_inner_width(
    head: Union[List[str], None],
    foot: Union[List[str], None] = None,
    opt: List[str] = [],
    minimum_width: int = 0,
    padx: Union[SinglePaddingType, MenuPaddingType] = (0, 0),
) -> int:
    """
    Help function to calculate the width of the item based on the longest
        string in the item. Used for 'message' and 'menu'.

    Args:
        head (list, None):
            The header to calculate the width for.

        foot (str, None, optional):
            The footer to calculate the width for. Defaults to `None`.

        opt (list, optional):
            The menu options to calculate the width for. Defaults to `None`.

        minimum_width (int, optional):
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

    def apply_padding(text: List[str], padding: Tuple[int, int]) -> List[str]:
        """Apply padding to a list of text lines."""
        lpad, rpad = padding
        return [f"{' ' * lpad}{line}{' ' * rpad}" for line in text]

    if padx:
        if len(padx) == 2 and all(isinstance(x, int) for x in padx):
            # Message padding
            head = apply_padding(head, padx) if head else head
            opt = apply_padding(opt, padx) if opt else opt
            foot = apply_padding(foot, padx) if foot else foot

        elif len(padx) == 3:
            # Menu padding
            head = apply_padding(head, padx[0]) if head else head
            opt = apply_padding(opt, padx[1]) if opt else opt
            foot = apply_padding(foot, padx[2]) if foot else foot

    max_str_width = max(
        max(len(h) for h in head) if head else 0,
        max(len(f) for f in foot) if foot else 0,
        max(len(o) for o in opt) if opt else 0,
    )

    return (
        max_str_width if max_str_width > minimum_width else minimum_width - 2
    )


def calculate_table_inner_width(
    table_data: TableDataType,
    headers: TableHeaderType,
    padx: TablePaddingType,
    minimum_width: TableMinWidthType,
    is_dict_table: bool,
    indexing: bool,
) -> Dict[int, int]:
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

        headers (Union[list, str], optional):
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

    column_widths: Dict[int, int] = {}
    header_padx, data_padx = padx
    starting_index = 0

    if indexing:
        index_width = len(str(len(table_data)))
        column_widths[0] = index_width
        starting_index = 1

    if headers != "None":
        for col_i, header in enumerate(headers, starting_index):
            column_widths[col_i] = max(
                len(str(header)) + sum(header_padx),
                (
                    minimum_width
                    if isinstance(minimum_width, int)
                    else minimum_width[col_i - 1 if indexing else col_i]
                ),
            )

    if is_dict_table:
        for row in table_data:
            for col_i, (_, column_name) in enumerate(
                zip(row, headers), starting_index
            ):
                col_width = len(str(row[column_name])) + sum(data_padx)
                if col_i not in column_widths:
                    column_widths[col_i] = max(
                        col_width,
                        (
                            minimum_width
                            if isinstance(minimum_width, int)
                            else (minimum_width[col_i])
                        ),
                    )
                else:
                    column_widths[col_i] = max(
                        column_widths[col_i],
                        col_width,
                        (
                            minimum_width
                            if isinstance(minimum_width, int)
                            else (
                                minimum_width[col_i - 1 if indexing else col_i]
                            )
                        ),
                    )

    else:

        def calculate_column_width(
            col_value: str,
            col_i: int,
            data_padx: Tuple[int, int],
            minimum_width: TableMinWidthType,
            indexing: bool,
        ) -> int:
            """Calculate the width of a single column."""
            col_width = len(str(col_value)) + sum(data_padx)
            return max(
                col_width,
                (
                    minimum_width
                    if isinstance(minimum_width, int)
                    else (minimum_width[col_i - 1 if indexing else col_i])
                ),
            )

        for row in table_data:
            for col_i, col_value in enumerate(row, starting_index):
                col_width = calculate_column_width(
                    col_value, col_i, data_padx, minimum_width, indexing
                )
                if col_i not in column_widths:
                    column_widths[col_i] = col_width
                else:
                    column_widths[col_i] = max(column_widths[col_i], col_width)

    return column_widths
