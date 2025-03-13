from typing import Dict, Final, List, Union
from .types import (
    StyleEnum,
    StyleType,
    AlignType,
    BorderDict,
    IndexEnum,
    HeaderEnum,
    TableHeaderType,
)

# Maximum dimensions
MAX_COLUMN_WIDTH: Final[int] = 0  # Maximum width of a single column
MAX_TABLE_WIDTH: Final[int] = 0  # Maximum width of entire table

# Border style key constants
TL = "TL"  # Top Left
TR = "TR"  # Top Right
BL = "BL"  # Bottom Left
BR = "BR"  # Bottom Right
H = "H"  # Horizontal
V = "V"  # Vertical
C = "C"  # Center
ML = "ML"  # Middle Left
MR = "MR"  # Middle Right
MT = "MT"  # Middle Top
MB = "MB"  # Middle Bottom
HB = "HB"  # Header Bottom

BOLD_STYLE: Final[BorderDict] = {
    TL: "┏",
    TR: "┓",
    BL: "┗",
    BR: "┛",
    H: "━",
    V: "┃",
    C: "╋",
    ML: "┣",
    MR: "┫",
    MT: "┳",
    MB: "┻",
    HB: "╍",
}

DOUBLE_STYLE: Final[BorderDict] = {
    TL: "╔",
    TR: "╗",
    BL: "╚",
    BR: "╝",
    H: "═",
    V: "║",
    C: "╬",
    ML: "╠",
    MR: "╣",
    MT: "╦",
    MB: "╩",
    HB: "═",
}

SINGLE_STYLE: Final[BorderDict] = {
    TL: "┌",
    TR: "┐",
    BL: "└",
    BR: "┘",
    H: "─",
    V: "│",
    C: "┼",
    ML: "├",
    MR: "┤",
    MT: "┬",
    MB: "┴",
    HB: "╌",
}

ASCII_STYLE: Final[BorderDict] = {
    TL: "+",
    TR: "+",
    BL: "+",
    BR: "+",
    H: "-",
    V: "|",
    C: "+",
    ML: "|",
    MR: "|",
    MT: "+",
    MB: "+",
    HB: "=",
}

# Border Styles
STYLES: Final[Dict[StyleType, BorderDict]] = {
    StyleEnum.DOUBLE.value: DOUBLE_STYLE,
    StyleEnum.SINGLE.value: SINGLE_STYLE,
    StyleEnum.SIMPLE.value: ASCII_STYLE,
    StyleEnum.BOLD.value: BOLD_STYLE,
}

# Available Options
VALID_ALIGNMENTS: Final[List[AlignType]] = ["left", "center", "right"]
VALID_HEADERS: Final[List[TableHeaderType]] = [
    HeaderEnum.NONE.value,
    HeaderEnum.FROM_DATA.value,
]
INDEX_VALUES: Final[List[Union[None, str]]] = [
    None,
    IndexEnum.NUMBER_DOT.value,
    IndexEnum.NUMBER_PARENTHESES.value,
    IndexEnum.LETTER_UPPER_DOT.value,
    IndexEnum.LETTER_UPPER_PARENTHESES.value,
    IndexEnum.LETTER_LOWER_DOT.value,
    IndexEnum.LETTER_LOWER_PARENTHESES.value,
]

ERROR_MESSAGES: Final[Dict[str, Dict[str, str]]] = {
    # Common errors shared across classes
    "COMMON": {
        "INVALID_STYLE": (
            "Style must be one of: single, double, bold, simple.\n"
            "Got: {value}\n"
            "Hint: Use StyleEnum values or their string representations"
        ),
        "INVALID_MIN_WIDTH": (
            "Minimum width must be a positive number.\n"
            "Got: {value}\n"
            "Hint: Use a number greater than or equal to 0"
        ),
        "INVALID_TYPE": (
            "Expected {expected_type} but received different type.\n"
            "Got: {value}\n"
            "Hint: Check the type of your input"
        ),
        "VALUE_OUT_OF_RANGE": (
            "Value must be between {min_value} and {max_value}.\n"
            "Got: {value}\n"
            "Hint: Ensure the value is within the acceptable range"
        ),
    },
    # Message-specific errors
    "MESSAGE": {
        # Content Errors
        "INVALID_TEXT": (
            "Message content must be a string or list of strings.\n"
            "Got: {value}\n"
            "Hint: Provide text as a string or ['line1', 'line2', ...]"
        ),
        "EMPTY_MESSAGE": (
            "Message content cannot be empty.\n"
            "Got: {value}\n"
            "Hint: Provide at least one character or line of text"
        ),
        "INVALID_LINE_LENGTH": (
            "All lines in a message must fit within the minimum width.\n"
            "Got line with length: {value}\n"
            "Hint: Adjust the text or increase the minimum width"
        ),
        # Configuration Errors
        "INVALID_ALIGN": (
            "Message alignment must be one of: left, center, right.\n"
            "Got: {value}\n"
            "Hint: Default is left alignment"
        ),
        "INVALID_WRAP": (
            "Text wrap must be either True or False.\n"
            "Got: {value}\n"
            "Hint: Enable text wrapping with True, disable with False"
        ),
        # Padding Errors
        "INVALID_PADDING": (
            "Message padding must be either:\n"
            "- A positive number for uniform padding\n"
            "- A pair of numbers (left, right)\n"
            "Got: {value}\n"
            "Hint: Use 1 for uniform padding or (1, 1) for custom padding"
        ),
        "CENTER_PADDING_CONFLICT": (
            "Cannot use padding with center alignment in message.\n"
            "Got padding: {value}\n"
            "Hint: Use 0 padding with center alignment or choose left/right alignment"
        ),
    },
    # Table-specific errors
    "TABLE": {
        # Data Structure Errors
        "INVALID_DATA_TYPE": (
            "Table data must be a list of lists or list of dictionaries.\n"
            "Got: {value}\n"
            "Hint: Make sure your data is formatted as [[row1], [row2], ...] or "
            "as a list of dictionaries"
        ),
        "INSUFFICIENT_ROWS": (
            "Table must have at least 2 rows when using automatic headers.\n"
            "Got: {value} rows\n"
            "Hint: Add more rows or specify custom headers"
        ),
        "INCONSISTENT_ROWS": (
            "All rows must have the same number of columns.\n"
            "Got rows with different lengths\n"
            "Hint: Check that each row has the same number of items"
        ),
        "INCONSISTENT_KEYS": (
            "All dictionaries in table data must have matching keys.\n"
            "Got mismatched keys: {value}\n"
            "Hint: Ensure all dictionaries have the same set of keys"
        ),
        "EMPTY_TABLE": (
            "Table cannot be empty.\n"
            "Got: {value}\n"
            "Hint: Provide at least one row of data"
        ),
        # Size limit errors
        "TABLE_TOO_WIDE": (
            "Total table width exceeds maximum allowed width.\n"
            "Got width: {width}, maximum allowed: {max_width}\n"
            "Hint: Reduce column widths or number of columns"
        ),
        "COLUMN_TOO_WIDE": (
            "Column {column} exceeds maximum allowed width.\n"
            "Got width: {width}, maximum allowed: {max_width}\n"
            "Hint: Reduce content length or increase wrapping"
        ),
        "CELL_TOO_LONG": (
            "Content in column {column} exceeds maximum length.\n"
            "Got length: {length}, maximum allowed: {max_length}\n"
            "Hint: Shorten content or enable text wrapping"
        ),
        "INVALID_CELL_TYPE": (
            "Cell content must be string, integer, or float.\n"
            "Got invalid type in column {column}: {value}\n"
            "Hint: Convert cell content to string format"
        ),
        # Configuration Errors
        "INVALID_HEADERS": (
            "Headers must be one of: None, from_data, or a list of strings.\n"
            "Got: {value}\n"
            "Hint: Use None for no headers, from_data for automatic headers, "
            "or provide a list of column names"
        ),
        "INVALID_INDEX": (
            "Index must be either True or False.\n"
            "Got: {value}\n"
            "Hint: Use True to show row numbers, False to hide them"
        ),
        "INVALID_ROW_SEP": (
            "Row separator must be either True or False.\n"
            "Got: {value}\n"
            "Hint: Use True to show lines between rows, False to hide them"
        ),
        "HEADER_COUNT_MISMATCH": (
            "Number of headers must match number of columns.\n"
            "Got: {value} headers for {column_count} columns\n"
            "Hint: Provide one header for each column"
        ),
        # Styling Errors
        "INVALID_ALIGN": (
            "Alignment must be a tuple of two values from: left, center, right.\n"
            "Got: {value}\n"
            "Hint: Use (left, left) for default alignment"
        ),
        "INVALID_CUSTOM_ALIGN": (
            "Custom alignment must be a dictionary of column alignments.\n"
            "Got: {value}\n"
            "Hint: Use {column_index: alignment} format"
        ),
        "INVALID_MIN_WIDTH_TYPE": (
            "Minimum width must be a positive number or a dictionary of column widths.\n"
            "Got: {value}\n"
            "Hint: Use a single number for all columns or {column_index: width}"
        ),
        "INVALID_MIN_WIDTH_VALUES": (
            "All minimum width values must be positive numbers.\n"
            "Got: {value}\n"
            "Hint: Make sure all width values are greater than 0"
        ),
        "COLUMN_INDEX_OUT_OF_RANGE": (
            "Column index in custom settings is out of range.\n"
            "Got index: {value}, valid range: 0-{max_index}\n"
            "Hint: Use column indices within the table's column count"
        ),
        # Padding Errors
        "INVALID_PADDING": (
            "Padding must be either:\n"
            "- A positive number for all sections\n"
            "- Two pairs of numbers for headers and data padding\n"
            "Got: {value}\n"
            "Hint: Use 1 for uniform padding or ((1,1), (1,1)) for custom padding"
        ),
        "CENTER_PADDING_CONFLICT": (
            "Cannot use padding with center alignment in {section}.\n"
            "Got padding: {value}\n"
            "Hint: Use 0 padding with center alignment or choose left/right alignment"
        ),
    },
    # Menu-specific errors
    "MENU": {
        # Content Errors
        "INVALID_OPTIONS": (
            "Menu options must be a non-empty list of strings.\n"
            "Got: {value}\n"
            "Hint: Provide at least one option as a string"
        ),
        "INVALID_PREFIX": (
            "Custom prefix must be a list of strings matching the number of menu items.\n"
            "Got: {value}\n"
            "Hint: Make sure the prefix list length matches your menu items"
        ),
        "EMPTY_MENU": (
            "Menu cannot be empty.\n"
            "Got: {value}\n"
            "Hint: Provide at least one menu option"
        ),
        "INVALID_HEADER": (
            "Menu header must be None, a string, or a list of strings.\n"
            "Got: {value}\n"
            "Hint: Use None for no header, a string, or ['line1', 'line2', ...]"
        ),
        "INVALID_FOOTER": (
            "Menu footer must be None, a string, or a list of strings.\n"
            "Got: {value}\n"
            "Hint: Use None for no footer, a string, or ['line1', 'line2', ...]"
        ),
        # Configuration Errors
        "INVALID_INDEX": (
            "Index type must be one of: number.dot, number.parentheses, "
            "letter.upper.dot, letter.upper.parentheses, letter.lower.dot, "
            "letter.lower.parentheses.\n"
            "Got: {value}\n"
            "Hint: Choose one of the available index formats or None"
        ),
        "INVALID_ALIGN": (
            "Alignment must be one of: left, center, right.\n"
            "Got: {value}\n"
            "Hint: Default is left alignment"
        ),
        "PREFIX_INDEX_CONFLICT": (
            "Cannot use both custom prefix and index type simultaneously.\n"
            "Got: prefix={prefix}, index={index}\n"
            "Hint: Choose either custom prefix or index type, not both"
        ),
        # Padding Errors
        "INVALID_PADDING": (
            "Padding must be either:\n"
            "- A positive number for all sections\n"
            "- Two pairs of numbers for headers and data padding\n"
            "Got: {value}\n"
            "Hint: Use 1 for uniform padding or ((1,1), (1,1)) for custom padding"
        ),
        "CENTER_PADDING_CONFLICT": (
            "Cannot use padding with center alignment in {section}.\n"
            "Got padding: {value}\n"
            "Hint: Use 0 padding with center alignment or choose left/right alignment"
        ),
    },
}
