import unittest
from bluetermgen.message import Message


class TestMessage(unittest.TestCase):

    # Test for different styles
    def test_single_style_message(self):
        message = Message("Hello World", style="single")
        expected = "┌───────────┐\n" "│Hello World│\n" "└───────────┘"
        self.assertEqual(message.message, expected)

    def test_double_style_message(self):
        message = Message("Hello World", style="double")
        expected = "╔═══════════╗\n" "║Hello World║\n" "╚═══════════╝"
        self.assertEqual(message.message, expected)

    def test_ascii_style_message(self):
        message = Message("Hello World", style="ascii")
        expected = "+-----------+\n" "|Hello World|\n" "+-----------+"
        self.assertEqual(message.message, expected)

    # Test padding and center alignment
    def test_message_with_padding(self):
        message = Message("Padded", padx=3, style="single")
        expected = "┌────────────┐\n" "│   Padded   │\n" "└────────────┘"
        self.assertEqual(message.message, expected)

    def test_message_centered(self):
        message = Message("Center", center=True, min_width=20, style="double")
        expected = (
            "╔══════════════════╗\n"
            "║      Center      ║\n"
            "╚══════════════════╝"
        )
        self.assertEqual(message.message, expected)

    # Test for multiple lines
    def test_multi_line_message(self):
        message = Message(["Line 1", "Line 2", "Line 3"], style="ascii")
        expected = (
            "+------+\n" "|Line 1|\n" "|Line 2|\n" "|Line 3|\n" "+------+"
        )
        self.assertEqual(message.message, expected)

    # Test padx with tuple
    def test_message_with_different_padx(self):
        message = Message("Pad Test", padx=(2, 5), style="single")
        expected = (
            "┌───────────────┐\n" "│  Pad Test     │\n" "└───────────────┘"
        )
        self.assertEqual(message.message, expected)

    # Test minimum width without centering
    def test_min_width_no_center(self):
        message = Message("Short", min_width=15, style="double")
        expected = "╔═════════════╗\n" "║Short        ║\n" "╚═════════════╝"
        self.assertEqual(message.message, expected)

    # Test invalid inputs
    def test_invalid_style(self):
        with self.assertRaises(ValueError):
            Message("Invalid style", style="nonexistent")

    def test_invalid_padx(self):
        with self.assertRaises(ValueError):
            Message("Invalid padx", padx=(-1, 1))

    def test_invalid_message_type(self):
        with self.assertRaises(ValueError):
            Message(123)  # Non-string, non-list

    # Test both center and padx raise ValueError
    def test_center_with_padx(self):
        with self.assertRaises(ValueError):
            Message("Invalid combo", center=True, padx=(2, 2))

    # Test empty message
    def test_empty_message(self):
        message = Message("", style="ascii")
        expected = "++\n" "||\n" "++"
        self.assertEqual(message.message, expected)

    # Test empty list as message
    def test_empty_list_message(self):
        message = Message([], style="single")
        expected = "┌┐\n" "└┘"
        self.assertEqual(message.message, expected)


if __name__ == "__main__":
    unittest.main()
