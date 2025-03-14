"""Type definitions for the terminal UI elements."""

from typing import (
    Dict,
    List,
    Literal,
    Optional,
    Tuple,
    Union,
)
from enum import Enum


# Enums
class StyleEnum(str, Enum):
    """Border style options for UI elements."""

    SINGLE = "single"
    DOUBLE = "double"
    BOLD = "bold"
    SIMPLE = "simple"

    @classmethod
    def list(cls) -> List[str]:
        """List all enum values."""
        return list(map(lambda c: c.value, cls))


class AlignEnum(str, Enum):
    """Alignment options for text positioning."""

    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"

    @classmethod
    def list(cls) -> List[str]:
        """List all enum values."""
        return list(map(lambda c: c.value, cls))


class HeaderEnum(str, Enum):
    """Header options for table configuration."""

    NONE = "None"
    FROM_DATA = "from_data"

    @classmethod
    def list(cls) -> List[str]:
        """List all enum values."""
        return list(map(lambda c: c.value, cls))


class IndexEnum(str, Enum):
    """Index formatting options for menu items."""

    NUMBER_DOT = "number.dot"
    NUMBER_PARENTHESES = "number.parentheses"
    LETTER_UPPER_DOT = "letter.upper.dot"
    LETTER_UPPER_PARENTHESES = "letter.upper.parentheses"
    LETTER_LOWER_DOT = "letter.lower.dot"
    LETTER_LOWER_PARENTHESES = "letter.lower.parentheses"

    @classmethod
    def list(cls) -> List[str]:
        """List all enum values."""
        return list(map(lambda c: c.value, cls))


# Border Types
BorderCharType = Literal[
    "TL", "TR", "BL", "BR", "H", "V", "C", "ML", "MR", "MT", "MB", "HB"
]
"""Border character keys for style dictionaries"""

StyleType = Literal[
    StyleEnum.SINGLE,
    StyleEnum.DOUBLE,
    StyleEnum.BOLD,
    StyleEnum.SIMPLE,
]
"""Available border styles for UI elements"""

BorderDict = Dict[BorderCharType, str]
"""Mapping of border positions to their character representations"""

# Alignment Types
AlignType = Literal[
    AlignEnum.LEFT,
    AlignEnum.CENTER,
    AlignEnum.RIGHT,
]
"""Text alignment options within UI elements"""

# Padding Types
SinglePaddingType = Tuple[int, int]
"""Basic padding configuration (left, right)"""

# Message Types
MessageTextType = Union[str, List[str]]
"""Content for message display (single string or multiple lines)"""

MessagePaddingType = Union[SinglePaddingType, int]
"""Message padding configuration (tuple or uniform integer)"""


# Menu Types
MenuItemsType = List[str]
"""List of menu options to display"""

MenuAlignType = Tuple[AlignType, AlignType, AlignType]
"""Menu section alignment (header, items, footer)"""

MenuSectionPadding = Tuple[
    SinglePaddingType, SinglePaddingType, SinglePaddingType
]
MenuPaddingType = Union[MenuSectionPadding, int]
"""Menu section padding ((header), (items), (footer)) or uniform integer"""

IndexType = Union[
    None,
    Literal[
        IndexEnum.NUMBER_DOT,
        IndexEnum.NUMBER_PARENTHESES,
        IndexEnum.LETTER_UPPER_DOT,
        IndexEnum.LETTER_UPPER_PARENTHESES,
        IndexEnum.LETTER_LOWER_DOT,
        IndexEnum.LETTER_LOWER_PARENTHESES,
    ],
]
"""Menu item numbering format including None for no indexing"""

CustomPrefixType = Optional[List[str]]
"""Custom prefixes for menu items"""

# Table Types
TableDataType = Union[List[List[str]], List[Dict[str, str]]]
"""Table data in list or dictionary format
- List format: List[List[str]] where each inner list is a row
- Dict format: List[Dict[str, str]] where each dict is a row with column keys

Examples:
    List format:
        [
            ["row1 col1", "row1 col2"],
            ["row2 col1", "row2 col2"]
        ]
    
    Dict format:
        [
            {"col1": "row1 val1", "col2": "row1 val2"},
            {"col1": "row2 val1", "col2": "row2 val2"}
        ]
"""

TableHeaderType = Union[
    HeaderEnum,
    List[str],
]
"""Table header configuration options:
- HeaderEnum.NONE: No headers
- HeaderEnum.FROM_DATA: Extract headers from data
- List[str]: Custom header labels
"""

TableAlignType = Tuple[AlignType, AlignType]
"""Table section alignment (header, data)"""

TablePaddingType = Union[
    Tuple[SinglePaddingType, SinglePaddingType],
    int,
]
"""Table section padding ((header), (data)) or uniform integer"""

TableMinWidthType = Union[int, Dict[int, int]]
"""Column width specifications (uniform or per-column)"""
