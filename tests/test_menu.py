import pytest
from bluetermgen.menu import Menu
from bluetermgen.exceptions import ValidationError, PaddingError


# Style Tests
@pytest.mark.parametrize("style", ["single", "double", "simple", "bold"])
def test_various_styles(
    style, default_menu_items, menu_header, menu_footer, menu_styles
):
    """Test that each style renders correctly with the expected border format."""
    menu = Menu(
        menu_items=default_menu_items,
        header=menu_header,
        footer=menu_footer,
        style=style,
    )
    assert menu.menu == menu_styles[style]


# Basic Rendering Tests
def test_basic_menu(default_menu_items):
    """Test rendering of basic menu without header or footer."""
    menu = Menu(menu_items=default_menu_items)
    expected = (
        "┌────────┐\n"
        "│Option 1│\n"
        "│Option 2│\n"
        "│Option 3│\n"
        "└────────┘"
    )
    assert menu.menu == expected


def test_menu_with_header_footer(default_menu_items, menu_header, menu_footer):
    """Test rendering of menu with header and footer."""
    menu = Menu(
        menu_items=default_menu_items,
        header=menu_header,
        footer=menu_footer,
    )
    expected = (
        "┌─────────┐\n"
        "│Main Menu│\n"
        "├╌╌╌╌╌╌╌╌╌┤\n"
        "│Option 1 │\n"
        "│Option 2 │\n"
        "│Option 3 │\n"
        "├─────────┤\n"
        "│x) Exit  │\n"
        "└─────────┘"
    )
    assert str(menu) == expected


# Indexing Tests
@pytest.mark.parametrize(
    "index_type,expected",
    [
        (
            "letter.upper.dot",
            "┌───────────┐\n"
            "│A. Option 1│\n"
            "│B. Option 2│\n"
            "└───────────┘",
        ),
        (
            "number.dot",
            "┌───────────┐\n"
            "│1. Option 1│\n"
            "│2. Option 2│\n"
            "└───────────┘",
        ),
    ],
)
def test_menu_indexing(index_type, expected):
    """Test different indexing options."""
    menu = Menu(menu_items=["Option 1", "Option 2"], index=index_type)
    assert menu.menu == expected


# Alignment Tests
@pytest.mark.parametrize(
    "align,header,footer,expected",
    [
        (
            ("center", "left", "center"),
            "Centered Header",
            "Centered Footer",
            "┌──────────────────┐\n"
            "│ Centered Header  │\n"
            "├╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤\n"
            "│Option 1          │\n"
            "├──────────────────┤\n"
            "│ Centered Footer  │\n"
            "└──────────────────┘",
        ),
        (
            ("right", "left", "right"),
            "Right Header",
            "Right Footer",
            "┌──────────────────┐\n"
            "│      Right Header│\n"
            "├╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤\n"
            "│Option 1          │\n"
            "├──────────────────┤\n"
            "│      Right Footer│\n"
            "└──────────────────┘",
        ),
    ],
)
def test_menu_alignment(align, header, footer, expected, min_width):
    """Test different alignment configurations."""
    menu = Menu(
        menu_items=["Option 1"],
        header=header,
        footer=footer,
        align=align,
        min_width=min_width,
    )
    assert menu.menu == expected


# Padding Tests
@pytest.mark.parametrize(
    "padx,items,expected",
    [
        (
            ((0, 0), (2, 2), (0, 0)),
            ["Padded Option"],
            "┌───────────────────┐\n"
            "│  Padded Option    │\n"
            "└───────────────────┘",
        ),
        (
            ((0, 0), (2, 2), (0, 0)),
            ["Option 1"],
            "┌───────────────────┐\n"
            "│         Option 1  │\n"
            "└───────────────────┘",
        ),
    ],
)
def test_menu_padding(padx, items, expected):
    """Test padding configurations."""
    menu = Menu(
        menu_items=items,
        padx=padx,
        style="single",
        align=(
            ("left", "right", "left")
            if len(items) == 1 and items[0] == "Option 1"
            else ("left", "left", "left")
        ),
        min_width=21,
    )
    assert menu.menu == expected


# Error Handling Tests
@pytest.mark.parametrize(
    "test_input,expected_error",
    [
        (
            {"menu_items": "Invalid Items"},
            ValidationError,
        ),  # Invalid menu_items
        (
            {"menu_items": ["Option 1"], "index": "invalid"},
            ValidationError,
        ),  # Invalid index
        (
            {
                "menu_items": ["Option 1"],
                "align": ("center", "left", "left"),
                "padx": ((1, 1), (0, 0), (0, 0)),
            },
            PaddingError,
        ),  # Center padding conflict
        ({"menu_items": []}, ValidationError),  # Empty menu
    ],
)
def test_menu_errors(test_input, expected_error):
    """Test various error conditions."""
    with pytest.raises(expected_error):
        Menu(**test_input)


# Edge Cases
def test_menu_with_empty_items():
    """Test handling of empty menu items."""
    with pytest.raises(ValidationError):
        Menu(menu_items=[])


@pytest.mark.parametrize(
    "items,index,custom_prefix",
    [
        (
            ["Option 1"],
            "number.dot",
            ["1."],
        ),  # Can't use both index and custom prefix
    ],
)
def test_index_prefix_conflict(items, index, custom_prefix):
    """Test conflicts between index and custom prefix."""
    with pytest.raises(ValidationError):
        Menu(menu_items=items, index=index, custom_index_prefix=custom_prefix)
