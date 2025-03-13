from typing import Dict, List, Tuple, Union
from .types import (
    StyleType,
    AlignType,
    TableDataType,
    TableHeaderType,
    TableAlignType,
    TablePaddingType,
    TableMinWidthType,
    StyleEnum,
    AlignEnum,
    HeaderEnum,
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
    MT,
    MB,
    C,
    HB,
    MAX_COLUMN_WIDTH,
    MAX_TABLE_WIDTH,
)
from .helpers import calculate_table_inner_width
from .base import BorderedElement
from .exceptions import ValidationError, PaddingError


class Table(BorderedElement):
    """
    Generates a bordered table with advanced styling and formatting options.

    Args:
        table_data (TableDataType):
            The data to display in table format:
            - List[List[str]]: Each inner list is a row
            - List[Dict[str, str]]: Each dict is a row with column keys

        headers (TableHeaderType, optional):
            Table header configuration. Options:
            - HeaderEnum.NONE: No headers
            - HeaderEnum.FROM_DATA: Auto-generate from data
            - List[str]: Custom header labels
            Defaults to HeaderEnum.FROM_DATA.

        index (bool, optional):
            Whether to show row numbers.
            Defaults to False.

        align (TableAlignType, optional):
            Default alignment for headers and data.
            Format: (header_align, data_align)
            Defaults to (LEFT, LEFT).

        custom_align (Dict[int, Union[AlignType, List[AlignType]]], optional):
            Custom alignment per column:
            - {col_idx: align_type}: Same alignment for all rows
            - {col_idx: [row_aligns]}: Different alignment per row
            Defaults to empty dict.

        min_width (TableMinWidthType, optional):
            Minimum column widths:
            - int: Same width for all columns
            - Dict[int, int]: Different width per column
            Defaults to 0.

        style (StyleType, optional):
            Border style for the table.
            Defaults to StyleEnum.SINGLE.

        padx (TablePaddingType, optional):
            Horizontal padding configuration:
            Format: ((header_left, header_right), (data_left, data_right))
            Defaults to ((0, 0), (0, 0)).

        row_sep (bool, optional):
            Whether to show separators between rows.
            Defaults to False.

    Raises:
        ValidationError:
            - Invalid data structure
            - Invalid header configuration
            - Invalid alignment settings
            - Invalid width settings
            - Column index out of range

        PaddingError:
            - Invalid padding configuration
            - Padding/alignment conflicts
    """

    def __init__(
        self,
        table_data: TableDataType,
        headers: TableHeaderType = HeaderEnum.FROM_DATA,
        index: bool = False,
        align: TableAlignType = (AlignEnum.LEFT.value, AlignEnum.LEFT.value),
        custom_align: Dict[int, Union[AlignType, List[AlignType]]] = {},
        min_width: TableMinWidthType = 0,
        style: StyleType = StyleEnum.SINGLE.value,
        padx: TablePaddingType = ((0, 0), (0, 0)),
        row_sep: bool = False,
    ) -> None:
        """Initialize table with configuration."""
        super().__init__(style=style, align=align[0])

        # Initialize state
        self._is_dict_table = False
        self._is_custom_headers = headers != HeaderEnum.FROM_DATA
        self._column_count = 0
        self._row_count = 0

        # Validate and set properties
        self.table_data = table_data
        self.headers = headers
        self.index = index
        self.align = align
        self.custom_align = custom_align
        self.min_width = min_width
        self.padx = padx
        self.row_separator = row_sep

        # Calculate dimensions
        self._calculate_dimensions()

        # Generate table
        self._content = self._generate_table()

    def _calculate_dimensions(self) -> None:
        """Calculate table dimensions and validate sizes."""
        self._inner_width = calculate_table_inner_width(
            table_data=self._table_data,
            headers=self._headers,
            padx=self._padx,
            minimum_width=self._min_width,
            is_dict_table=self._is_dict_table,
            indexing=self._index,
        )

        if MAX_TABLE_WIDTH != 0:
            # Validate column widths
            total_width = sum(self._inner_width.values()) + (
                len(self._inner_width) - 1
            )
            if total_width > MAX_TABLE_WIDTH:
                raise ValidationError(
                    ERROR_MESSAGES["TABLE"]["TABLE_TOO_WIDE"].format(
                        width=total_width, max_width=MAX_TABLE_WIDTH
                    )
                )

        if MAX_COLUMN_WIDTH != 0:
            for col, width in self._inner_width.items():
                if width > MAX_COLUMN_WIDTH:
                    raise ValidationError(
                        ERROR_MESSAGES["TABLE"]["COLUMN_TOO_WIDE"].format(
                            column=col, width=width, max_width=MAX_COLUMN_WIDTH
                        )
                    )

    def _validate_cell_content(self, content: str, col_idx: int) -> str:
        """
        Validate and normalize cell content.

        Args:
            content: Cell content to validate
            col_idx: Column index for error reporting

        Returns:
            Normalized content string

        Raises:
            ValidationError: If content is invalid
        """

        if content is None:
            return "None"

        if not isinstance(content, (str, int, float)):
            raise ValidationError(
                ERROR_MESSAGES["TABLE"]["INVALID_CELL_TYPE"].format(
                    column=col_idx, value=type(content).__name__
                )
            )

        content_str = str(content)
        if MAX_COLUMN_WIDTH != 0 and len(content_str) > MAX_COLUMN_WIDTH:
            raise ValidationError(
                ERROR_MESSAGES["TABLE"]["CELL_TOO_LONG"].format(
                    column=col_idx,
                    length=len(content_str),
                    max_length=MAX_COLUMN_WIDTH,
                )
            )

        return content_str

    def _generate_border(self, border_type: str) -> str:
        """
        Generate a table border line.

        Args:
            border_type: Type of border (top, middle, bottom)

        Returns:
            Formatted border string
        """
        if border_type == "top":
            left, mid, right = self.style[TL], self.style[MT], self.style[TR]
            line = self.style[H]
        elif border_type == "middle":
            left, mid, right = self.style[ML], self.style[C], self.style[MR]
            line = self.style[HB]
        elif border_type == "row_separator":
            left, mid, right = self.style[ML], self.style[C], self.style[MR]
            line = self.style[H]
        else:  # bottom
            left, mid, right = self.style[BL], self.style[MB], self.style[BR]
            line = self.style[H]

        sections = [line * width for width in self._inner_width.values()]
        result = f"{left}{mid.join(sections)}{right}"

        # Only add newline if it's not the bottom border
        return f"{result}\n" if border_type != "bottom" else result

    def _format_row(
        self,
        row: Union[List[str], Dict[str, str]],
        row_idx: int,
        is_header: bool = False,
    ) -> str:
        """
        Format a table row.

        Args:
            row: Row data as list or dict
            row_idx: Row index for alignment
            is_header: Whether this is a header row

        Returns:
            Formatted row string
        """
        cells = []

        # Add index if enabled
        if self._index and not is_header:
            cells.append(f"{row_idx:>{self._inner_width[0]}}")
        elif self._index:
            cells.append(" " * self._inner_width[0])

        # Format each cell
        start_idx = 1 if self._index else 0
        if isinstance(row, dict):
            for col_idx, key in enumerate(self._headers, start_idx):
                content = self._validate_cell_content(row[key], col_idx)
                align = self._get_alignment(col_idx, row_idx, is_header)
                padding = self._padx[0] if is_header else self._padx[1]
                cells.append(
                    self._format_cell(content, align, padding, col_idx)
                )
        else:
            for col_idx, content in enumerate(row, start_idx):
                content = self._validate_cell_content(content, col_idx)
                align = self._get_alignment(col_idx, row_idx, is_header)
                padding = self._padx[0] if is_header else self._padx[1]
                cells.append(
                    self._format_cell(content, align, padding, col_idx)
                )

        return f"{self.style[V]}{self.style[V].join(cells)}{self.style[V]}\n"

    def _get_alignment(
        self, col_idx: int, row_idx: int, is_header: bool
    ) -> AlignType:
        """
        Get alignment for a specific cell.

        Args:
            col_idx: Column index
            row_idx: Row index
            is_header: Whether this is a header cell

        Returns:
            Alignment value for the cell
        """
        if is_header:
            return self.align[0]

        if col_idx in self._custom_align:
            align_setting = self._custom_align[col_idx]
            if isinstance(align_setting, list):
                return align_setting[row_idx]
            return align_setting

        return self.align[1]

    def _format_cell(
        self,
        content: str,
        alignment: AlignType,
        padding: Tuple[int, int],
        col_idx: int,
    ) -> str:
        """
        Format a cell's content with alignment and padding.

        Args:
            content: Cell content
            alignment: Desired alignment
            padding: (left, right) padding
            col_idx: Column index for width

        Returns:
            Formatted cell content
        """
        width = self._inner_width[col_idx]

        if alignment == AlignEnum.CENTER.value:
            return f"{content:^{width}}"

        lpad, rpad = padding
        if alignment == AlignEnum.RIGHT.value:
            space_left = width - len(content) - rpad
            return f"{' ' * space_left}{content}{' ' * rpad}"

        space_right = width - len(content) - lpad
        return f"{' ' * lpad}{content}{' ' * space_right}"

    def _generate_table(self) -> str:
        """
        Generate the complete formatted table.

        Returns:
            Formatted table string
        """
        # Initialize with top border
        table = [self._generate_border("top")]
        self._width = len(table[0].strip("\n"))

        # Add headers if enabled
        if self._headers != HeaderEnum.NONE.value:
            table.append(self._format_row(self._headers, 0, True))
            table.append(self._generate_border("middle"))

        # Add data rows
        row_count = len(self._table_data)
        for idx, row in enumerate(self._table_data, 1):
            table.append(self._format_row(row, idx))

            # Add row separator if enabled and not last row
            if self._row_separator and idx < row_count:
                table.append(self._generate_border("row_separator"))

        # Add bottom border
        table.append(self._generate_border("bottom"))

        # Join and store height
        result = "".join(table)
        self._height = len(result.split("\n"))
        return result

    @property
    def column_count(self) -> int:
        """Get number of columns (excluding index)."""
        return self._column_count

    @property
    def row_count(self) -> int:
        """Get number of data rows (excluding headers)."""
        return self._row_count

    @property
    def effective_widths(self) -> Dict[int, int]:
        """Get effective column widths."""
        return self._inner_width.copy()

    @property
    def table_data(self) -> TableDataType:
        """Get the current table data."""
        return self._table_data

    @table_data.setter
    def table_data(self, value: TableDataType) -> None:
        """
        Set and validate table data.

        Args:
            value: Table data as list of lists or list of dicts.

        Raises:
            ValidationError: If data structure is invalid.
        """
        if not isinstance(value, list):
            raise ValidationError(
                ERROR_MESSAGES["TABLE"]["INVALID_DATA_TYPE"].format(
                    value=f"{type(value).__name__}"
                )
            )

        if not value:
            raise ValidationError(
                ERROR_MESSAGES["TABLE"]["EMPTY_TABLE"].format(
                    value="empty list"
                )
            )

        # Handle list of lists
        if all(isinstance(row, list) for row in value):
            if len(value) <= 1 and not self._is_custom_headers:
                raise ValidationError(
                    ERROR_MESSAGES["TABLE"]["INSUFFICIENT_ROWS"].format(
                        value=len(value)
                    )
                )

            row_lengths = {len(row) for row in value}
            if len(row_lengths) > 1:
                raise ValidationError(
                    ERROR_MESSAGES["TABLE"]["INCONSISTENT_ROWS"]
                )

            self._table_data = value
            self._column_count = row_lengths.pop()
            self._row_count = len(value)

        # Handle list of dicts
        elif all(isinstance(row, dict) for row in value):
            first_keys = set(value[0].keys()) if value else set()
            if not all(set(row.keys()) == first_keys for row in value):
                raise ValidationError(
                    ERROR_MESSAGES["TABLE"]["INCONSISTENT_KEYS"].format(
                        value=", ".join(str(set(row.keys())) for row in value)
                    )
                )

            self._table_data = value
            self._is_dict_table = True
            self._column_count = len(first_keys)
            self._row_count = len(value)

        else:
            raise ValidationError(
                ERROR_MESSAGES["TABLE"]["INVALID_DATA_TYPE"].format(
                    value=f"list containing non-list and non-dict items"
                )
            )

    @property
    def headers(self) -> TableHeaderType:
        """Get the current headers configuration."""
        return self._headers

    @headers.setter
    def headers(self, value: TableHeaderType) -> None:
        """
        Set and validate table headers.

        Args:
            value: Header configuration or custom labels.

        Raises:
            ValidationError: If header format is invalid.
        """
        if value == HeaderEnum.NONE.value:
            self._headers = []
        elif value == HeaderEnum.FROM_DATA.value:
            if self._is_dict_table:
                if not self._table_data:
                    raise ValidationError(
                        ERROR_MESSAGES["TABLE"]["EMPTY_TABLE"]
                    )
                self._headers = list(self._table_data[0].keys())
            else:
                if len(self._table_data) < 2:
                    raise ValidationError(
                        ERROR_MESSAGES["TABLE"]["INSUFFICIENT_ROWS"].format(
                            value=len(self._table_data)
                        )
                    )
                self._headers = self._table_data.pop(0)
        elif isinstance(value, list) and all(
            isinstance(x, str) for x in value
        ):
            if len(value) != self._column_count:
                raise ValidationError(
                    ERROR_MESSAGES["TABLE"]["HEADER_COUNT_MISMATCH"].format(
                        value=len(value), column_count=self._column_count
                    )
                )
            self._headers = value
        else:
            raise ValidationError(
                ERROR_MESSAGES["TABLE"]["INVALID_HEADERS"].format(
                    value=f"{type(value).__name__}"
                )
            )

    @property
    def index(self) -> bool:
        """Get the current index setting."""
        return self._index

    @index.setter
    def index(self, value: bool) -> None:
        """
        Set and validate index display option.

        Args:
            value: Whether to show row numbers.

        Raises:
            ValidationError: If value is not boolean.
        """
        if not isinstance(value, bool):
            raise ValidationError(
                ERROR_MESSAGES["TABLE"]["INVALID_INDEX"].format(
                    value=f"{type(value).__name__}"
                )
            )
        self._index = value

    @property
    def align(self) -> TableAlignType:
        """Get the current alignment configuration."""
        return self._align

    @align.setter
    def align(self, value: TableAlignType) -> None:
        """
        Set and validate alignment configuration.

        Args:
            value: Tuple of alignments for headers and data.

        Raises:
            ValidationError: If alignment format is invalid.
        """
        if not isinstance(value, tuple) or len(value) != 2:
            raise ValidationError(
                ERROR_MESSAGES["TABLE"]["INVALID_ALIGN"].format(
                    value=f"{type(value).__name__}"
                )
            )

        valid_alignments = [e.value for e in AlignEnum]
        if not all(x in valid_alignments for x in value):
            raise ValidationError(
                ERROR_MESSAGES["TABLE"]["INVALID_ALIGN"].format(
                    value=f"invalid alignment(s): {value}"
                )
            )
        self._align = value

    @property
    def custom_align(self) -> Dict[int, Union[AlignType, List[AlignType]]]:
        """Get the current custom alignment configuration."""
        return self._custom_align

    @custom_align.setter
    def custom_align(
        self, value: Dict[int, Union[AlignType, List[AlignType]]]
    ) -> None:
        """
        Set and validate custom alignment configuration.

        Args:
            value: Dictionary mapping columns to alignments.

        Raises:
            ValidationError: If alignment configuration is invalid.
        """
        if not isinstance(value, dict):
            raise ValidationError(
                ERROR_MESSAGES["TABLE"]["INVALID_CUSTOM_ALIGN"].format(
                    value=f"{type(value).__name__}"
                )
            )

        valid_alignments = [e.value for e in AlignEnum]

        for col_idx, alignment in value.items():
            if not isinstance(col_idx, int):
                raise ValidationError(
                    ERROR_MESSAGES["TABLE"]["INVALID_COLUMN_INDEX"].format(
                        value=f"{type(col_idx).__name__}"
                    )
                )

            if col_idx >= self._column_count:
                raise ValidationError(
                    ERROR_MESSAGES["TABLE"][
                        "COLUMN_INDEX_OUT_OF_RANGE"
                    ].format(value=col_idx, max_index=self._column_count - 1)
                )

            if isinstance(alignment, list):
                if len(alignment) != self._row_count:
                    raise ValidationError(
                        ERROR_MESSAGES["TABLE"][
                            "ALIGNMENT_COUNT_MISMATCH"
                        ].format(
                            value=len(alignment), row_count=self._row_count
                        )
                    )
                if not all(a in valid_alignments for a in alignment):
                    raise ValidationError(
                        ERROR_MESSAGES["TABLE"][
                            "INVALID_ALIGNMENT_VALUE"
                        ].format(value=alignment)
                    )
            elif alignment not in valid_alignments:
                raise ValidationError(
                    ERROR_MESSAGES["TABLE"]["INVALID_ALIGNMENT_VALUE"].format(
                        value=alignment
                    )
                )

        self._custom_align = value

    @property
    def min_width(self) -> TableMinWidthType:
        """Get the current minimum width configuration."""
        return self._min_width

    @min_width.setter
    def min_width(self, value: TableMinWidthType) -> None:
        """
        Set and validate minimum width configuration.

        Args:
            value: Integer or dictionary of minimum column widths.

        Raises:
            ValidationError: If width configuration is invalid.
        """
        if isinstance(value, int):
            if value < 0:
                raise ValidationError(
                    ERROR_MESSAGES["TABLE"]["INVALID_MIN_WIDTH_VALUES"].format(
                        value=value
                    )
                )
            self._min_width = value
        elif isinstance(value, dict):
            if not all(
                isinstance(k, int) and isinstance(v, int) and v >= 0
                for k, v in value.items()
            ):
                raise ValidationError(
                    ERROR_MESSAGES["TABLE"]["INVALID_MIN_WIDTH_VALUES"].format(
                        value=value
                    )
                )

            for col_idx in value:
                if col_idx >= self._column_count:
                    raise ValidationError(
                        ERROR_MESSAGES["TABLE"][
                            "COLUMN_INDEX_OUT_OF_RANGE"
                        ].format(
                            value=col_idx, max_index=self._column_count - 1
                        )
                    )

            self._min_width = value
        else:
            raise ValidationError(
                ERROR_MESSAGES["TABLE"]["INVALID_MIN_WIDTH_TYPE"].format(
                    value=f"{type(value).__name__}"
                )
            )

    @property
    def padx(self) -> TablePaddingType:
        """Get the current padding configuration."""
        return self._padx

    @padx.setter
    def padx(self, value: TablePaddingType) -> None:
        """
        Set and validate padding configuration.

        Args:
            value: Padding configuration for headers and data.

        Raises:
            PaddingError: If padding is invalid or conflicts with alignment.
        """
        if isinstance(value, int):
            if value < 0:
                raise PaddingError(
                    ERROR_MESSAGES["TABLE"]["INVALID_PADDING"].format(
                        value=value
                    )
                )
            self._padx = ((value, value), (value, value))
        elif (
            isinstance(value, tuple)
            and len(value) == 2
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
                ERROR_MESSAGES["TABLE"]["INVALID_PADDING"].format(
                    value=f"{type(value).__name__}"
                )
            )

        # Check for center alignment conflicts
        sections = ["headers", "data"]
        for idx, section in enumerate(sections):
            if self.align[idx] == AlignEnum.CENTER.value and self._padx[
                idx
            ] != (0, 0):
                raise PaddingError(
                    ERROR_MESSAGES["TABLE"]["CENTER_PADDING_CONFLICT"].format(
                        section=section, value=self._padx[idx]
                    )
                )

    @property
    def row_separator(self) -> bool:
        """Get the current row separator setting."""
        return self._row_separator

    @row_separator.setter
    def row_separator(self, value: bool) -> None:
        """
        Set and validate row separator display option.

        Args:
            value: Whether to show row separators.

        Raises:
            ValidationError: If value is not boolean.
        """
        if not isinstance(value, bool):
            raise ValidationError(
                ERROR_MESSAGES["TABLE"]["INVALID_ROW_SEP"].format(
                    value=f"{type(value).__name__}"
                )
            )
        self._row_separator = value

    @property
    def table(self) -> str:
        """Get the complete formatted table."""
        return self._content

    def __str__(self) -> str:
        """Get string representation of the table."""
        return self._content


if __name__ == "__main__":
    pass
