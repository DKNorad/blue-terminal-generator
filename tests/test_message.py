import pytest
from bluetermgen.message import Message
from bluetermgen.exceptions import ValidationError, StyleError, PaddingError


# Style Tests
@pytest.mark.parametrize("style", ["single", "double", "simple", "bold"])
def test_various_styles(style, default_message, message_styles):
    """Test that each style renders correctly with the expected border format."""
    message = Message(default_message, style=style)
    assert message.message == message_styles[style]


# Alignment Tests
def test_message_centered(default_message, min_width):
    """Test center alignment with double border and specified min_width."""
    message = Message(
        default_message,
        align="center",
        min_width=min_width,
        style="double",
    )
    expected = (
        "╔══════════════════╗\n"
        "║   Hello World    ║\n"
        "╚══════════════════╝"
    )
    assert message.message == expected


@pytest.mark.parametrize(
    "text,align,expected_content",
    [
        ("Right", "right", "|             Right|"),
        ("Left", "left", "|Left              |"),
    ],
)
def test_message_alignment(text, align, expected_content, min_width):
    """Test different alignment options."""
    message = Message(
        text,
        align=align,
        min_width=min_width,
        style="simple",
    )
    # Get the middle line of the message (excluding borders)
    actual_content = str(message).split("\n")[1]
    assert actual_content == expected_content


# Padding Tests
@pytest.mark.parametrize(
    "padx,text,expected",
    [
        (3, "Padded", "┌────────────┐\n" "│   Padded   │\n" "└────────────┘"),
        (
            (2, 5),
            "Pad Test",
            "┌───────────────┐\n" "│  Pad Test     │\n" "└───────────────┘",
        ),
    ],
)
def test_message_padding(padx, text, expected):
    """Test different padding configurations."""
    message = Message(text, padx=padx, style="single")
    assert message.message == expected


# Dimension Tests
@pytest.mark.parametrize(
    "text,style,expected_dimensions",
    [
        ("Test", "simple", (6, 3)),
        (["Line 1", "Line 2", "Line 3"], "simple", (8, 5)),
    ],
)
def test_get_dimensions(text, style, expected_dimensions):
    """Test dimension calculations for different message types."""
    message = Message(text, style=style)
    assert message.get_dimensions() == expected_dimensions


# Error Handling Tests
def test_invalid_style(default_message):
    """Test StyleError raised for invalid style."""
    with pytest.raises(StyleError):
        Message(default_message, style="nonexistent")


def test_invalid_padx(default_message):
    """Test PaddingError raised for invalid padx values."""
    with pytest.raises(PaddingError):
        Message(default_message, padx=(-1, 1))


@pytest.mark.parametrize(
    "invalid_input",
    [
        123,  # non-string/non-list
        [],  # empty list
        "",  # empty string
        [1, 2, 3],  # list of non-strings
    ],
)
def test_invalid_message_input(invalid_input):
    """Test ValidationError raised for various invalid inputs."""
    with pytest.raises(ValidationError):
        Message(invalid_input)


def test_center_with_padx(default_message):
    """Test PaddingError raised for combining center alignment with padx."""
    with pytest.raises(PaddingError):
        Message(default_message, align="center", padx=(2, 2))


# Edge Cases
def test_multi_line_message(multi_line_message):
    """Test rendering of multi-line message."""
    message = Message(multi_line_message, style="simple")
    expected = "+------+\n|Line 1|\n|Line 2|\n|Line 3|\n+------+"
    assert message.message == expected


def test_long_single_line_message():
    """Test long single-line message handling."""
    text = "This is a very long single line message"
    message = Message(text, style="simple")
    expected = (
        "+---------------------------------------+\n"
        "|This is a very long single line message|\n"
        "+---------------------------------------+"
    )
    assert message.message == expected
