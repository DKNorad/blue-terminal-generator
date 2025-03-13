import unittest
from bluetermgen.message import Message
from bluetermgen.exceptions import ValidationError, StyleError, PaddingError


class TestMessageStyles(unittest.TestCase):

    def setUp(self):
        self.default_message = "Hello World"
        self.styles = {
            "single": f"┌───────────┐\n│{self.default_message}│\n└───────────┘",
            "double": f"╔═══════════╗\n║{self.default_message}║\n╚═══════════╝",
            "simple": f"+-----------+\n|{self.default_message}|\n+-----------+",
            "bold": f"┏━━━━━━━━━━━┓\n┃{self.default_message}┃\n┗━━━━━━━━━━━┛",
        }

    def test_various_styles(self):
        """[Message] Test that each style renders correctly with the expected border
        format"""
        for style, expected_output in self.styles.items():
            with self.subTest(style=style):
                message = Message(self.default_message, style=style)
                self.assertEqual(message.message, expected_output)


class TestMessageAlignment(unittest.TestCase):

    def setUp(self):
        self.default_message = "Hello World"
        self.min_width = 20

    def test_message_centered(self):
        """[Message] Test center alignment with double border and specified min_width"""
        message = Message(
            self.default_message,
            align="center",
            min_width=self.min_width,
            style="double",
        )
        expected_output = (
            "╔══════════════════╗\n"
            "║   Hello World    ║\n"
            "╚══════════════════╝"
        )
        self.assertEqual(message.message, expected_output)

    def test_message_right_aligned(self):
        """[Message] Test right alignment with simple border and specified min_width"""
        message = Message(
            "Right", align="right", min_width=self.min_width, style="simple"
        )
        expected_output = (
            "+------------------+\n"
            "|             Right|\n"
            "+------------------+"
        )
        self.assertEqual(message.message, expected_output)

    def test_message_right_aligned_with_padx(self):
        """[Message] Test right alignment with padding and simple border"""
        message = Message(
            "Right",
            align="right",
            min_width=self.min_width,
            padx=3,
            style="simple",
        )
        expected_output = (
            "+------------------+\n"
            "|          Right   |\n"
            "+------------------+"
        )
        self.assertEqual(message.message, expected_output)


class TestMessagePadding(unittest.TestCase):

    def setUp(self):
        self.default_message = "Padded"

    def test_message_with_padding(self):
        """[Message] Test padding with single border"""
        message = Message(self.default_message, padx=3, style="single")
        expected_output = "┌────────────┐\n│   Padded   │\n└────────────┘"
        self.assertEqual(message.message, expected_output)

    def test_str_method_with_padding(self):
        """[Message] Test __str__ method with padding and single border"""
        message = Message(self.default_message, padx=3, style="single")
        expected_output = "┌────────────┐\n│   Padded   │\n└────────────┘"
        self.assertEqual(str(message), expected_output)

    def test_message_with_different_padx(self):
        """[Message] Test padding with tuple values for padx in single border"""
        message = Message("Pad Test", padx=(2, 5), style="single")
        expected_output = (
            "┌───────────────┐\n│  Pad Test     │\n└───────────────┘"
        )
        self.assertEqual(message.message, expected_output)

    def test_padding_with_large_padx(self):
        """[Message] Test large padx value with single border"""
        message = Message("Large Padding", padx=10, style="single")
        expected_output = (
            "┌─────────────────────────────────┐\n"
            "│          Large Padding          │\n"
            "└─────────────────────────────────┘"
        )
        self.assertEqual(message.message, expected_output)


class TestMessageDimensions(unittest.TestCase):

    def setUp(self):
        self.default_message = "Test"
        self.multi_line_message = ["Line 1", "Line 2", "Line 3"]

    def test_get_dimensions(self):
        """[Message] Test get_dimensions method for single-line message in simple border"""
        message = Message(self.default_message, style="simple")
        expected_dimensions = (6, 3)
        self.assertEqual(message.get_dimensions(), expected_dimensions)

    def test_get_dimensions_multi_line(self):
        """[Message] Test get_dimensions method for multi-line message in simple border"""
        message = Message(self.multi_line_message, style="simple")
        expected_dimensions = (8, 5)
        self.assertEqual(message.get_dimensions(), expected_dimensions)


class TestMessageErrorHandling(unittest.TestCase):

    def setUp(self):
        self.default_message = "Invalid input"

    def test_invalid_style(self):
        """[Message] Test StyleError raised for invalid style"""
        with self.assertRaises(StyleError):
            Message(self.default_message, style="nonexistent")

    def test_invalid_padx(self):
        """[Message] Test PaddingError raised for invalid padx values"""
        with self.assertRaises(PaddingError):
            Message(self.default_message, padx=(-1, 1))

    def test_invalid_message_type(self):
        """[Message] Test ValidationError raised for non-string, non-list message input"""
        with self.assertRaises(ValidationError):
            Message(123)  # Non-string, non-list

    def test_center_with_padx(self):
        """[Message] Test PaddingError raised for combining center alignment with padx"""
        with self.assertRaises(PaddingError):
            Message(self.default_message, align="center", padx=(2, 2))


class TestMessageEdgeCases(unittest.TestCase):

    def setUp(self):
        self.empty_message = ""
        self.multi_line_message = ["Line 1", "Line 2", "Line 3"]

    def test_empty_message(self):
        """[Message] Test rendering of empty message with simple border"""
        with self.assertRaises(ValidationError):
            Message(self.empty_message, style="simple")

    def test_empty_list_message(self):
        """[Message] Test rendering of empty list message with single border"""
        with self.assertRaises(ValidationError):
            Message([], style="single")

    def test_multi_line_message(self):
        """[Message] Test rendering of multi-line message with simple border"""
        message = Message(self.multi_line_message, style="simple")
        expected_output = "+------+\n|Line 1|\n|Line 2|\n|Line 3|\n+------+"
        self.assertEqual(message.message, expected_output)

    def test_long_single_line_message(self):
        """[Message] Test long single-line message handling with simple border"""
        message_text = "This is a very long single line message"
        message = Message(message_text, style="simple")
        expected_output = (
            "+---------------------------------------+\n"
            "|This is a very long single line message|\n"
            "+---------------------------------------+"
        )
        self.assertEqual(message.message, expected_output)


if __name__ == "__main__":
    unittest.main()
