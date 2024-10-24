import unittest
from bluetermgen.menu import Menu


class TestMenu(unittest.TestCase):

    # Test basic menu without header or footer
    def test_basic_menu(self):
        menu = Menu(menu_items=["Option 1", "Option 2", "Option 3"])
        expected = (
            "┌────────┐\n" "│Option 1│\n" "│Option 2│\n" "│Option 3│\n" "└────────┘"
        )
        self.assertEqual(menu.menu, expected)

    # Test the __str__ dunder method
    def test_str(self):
        menu = Menu(menu_items=["Option 1", "Option 2", "Option 3"])
        expected = (
            "┌────────┐\n" "│Option 1│\n" "│Option 2│\n" "│Option 3│\n" "└────────┘"
        )
        self.assertEqual(str(menu), expected)

    # Test the __str__ dunder method with header and footer
    def test_str_with_header_footer(self):
        menu = Menu(
            menu_items=["Option 1", "Option 2", "Option 3"],
            header="Main Menu",
            footer="x) Exit",
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
        self.assertEqual(str(menu), expected)

    # Test menu with a header and footer
    def test_menu_with_header_footer(self):
        menu = Menu(
            menu_items=["Option 1", "Option 2", "Option 3"],
            header="Main Menu",
            footer="x) Exit",
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
        self.assertEqual(menu.menu, expected)

    # Test menu with letter-based numbering (uppercase, dot)
    def test_menu_letter_upper_dot(self):
        menu = Menu(
            menu_items=["Option 1", "Option 2"],
            index="letter_upper_dot",
        )
        expected = "┌───────────┐\n" "│A. Option 1│\n" "│B. Option 2│\n" "└───────────┘"
        self.assertEqual(menu.menu, expected)

    # Test menu with letter-based numbering (lowercase, dot)
    def test_menu_letter_lower_dot(self):
        menu = Menu(
            menu_items=["Option 1", "Option 2"],
            index="letter_lower_dot",
        )
        expected = "┌───────────┐\n" "│a. Option 1│\n" "│b. Option 2│\n" "└───────────┘"
        self.assertEqual(menu.menu, expected)

    # Test menu with number-based numbering (number, dot)
    def test_menu_number_dot(self):
        menu = Menu(menu_items=["Option 1", "Option 2"], index="number_dot")
        expected = "┌───────────┐\n" "│1. Option 1│\n" "│2. Option 2│\n" "└───────────┘"
        self.assertEqual(menu.menu, expected)

    # Test menu with letter-based numbering (uppercase, parentheses)
    def test_menu_letter_upper_parantheses(self):
        menu = Menu(
            menu_items=["Option 1", "Option 2"],
            index="letter_upper_parentheses",
        )
        expected = "┌───────────┐\n" "│A) Option 1│\n" "│B) Option 2│\n" "└───────────┘"
        self.assertEqual(menu.menu, expected)

    # Test menu with letter-based numbering (lowercase, parentheses)
    def test_menu_letter_lower_parantheses(self):
        menu = Menu(
            menu_items=["Option 1", "Option 2"],
            index="letter_lower_parentheses",
        )
        expected = "┌───────────┐\n" "│a) Option 1│\n" "│b) Option 2│\n" "└───────────┘"
        self.assertEqual(menu.menu, expected)

    # Test menu with number-based numbering (number, parentheses)
    def test_menu_number_parentheses(self):
        menu = Menu(
            menu_items=["Option 1", "Option 2"],
            index="number_parentheses",
        )
        expected = "┌───────────┐\n" "│1) Option 1│\n" "│2) Option 2│\n" "└───────────┘"
        self.assertEqual(menu.menu, expected)

    # Test center alignment of header and footer
    def test_center_header_footer(self):
        menu = Menu(
            menu_items=["Option 1"],
            header="Centered Header",
            footer="Centered Footer",
            align=("center", "left", "center"),
            min_width=21,
        )
        expected = (
            "┌───────────────────┐\n"
            "│  Centered Header  │\n"
            "├╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤\n"
            "│Option 1           │\n"
            "├───────────────────┤\n"
            "│  Centered Footer  │\n"
            "└───────────────────┘"
        )
        self.assertEqual(menu.menu, expected)

    # Test right alignment of header and footer
    def test_right_header_footer(self):
        menu = Menu(
            menu_items=["Option 1"],
            header="Right Header",
            footer="Right Footer",
            align=("right", "left", "right"),
            min_width=21,
        )
        expected = (
            "┌───────────────────┐\n"
            "│       Right Header│\n"
            "├╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤\n"
            "│Option 1           │\n"
            "├───────────────────┤\n"
            "│       Right Footer│\n"
            "└───────────────────┘"
        )
        self.assertEqual(menu.menu, expected)

    # Test right alignment with padding
    def test_right_aligned_with_padding(self):
        menu = Menu(
            menu_items=["Option 1"],
            align=("left", "right", "left"),
            min_width=21,
            padx=((0, 0), (2, 2), (0, 0)),
        )
        expected = (
            "┌───────────────────┐\n" "│         Option 1  │\n" "└───────────────────┘"
        )
        self.assertEqual(menu.menu, expected)

    # Test padding on menu options
    def test_menu_with_padding_on_options(self):
        menu = Menu(
            menu_items=["Padded Option"],
            padx=((0, 0), (2, 2), (0, 0)),
            style="single",
        )
        expected = "┌─────────────────┐\n" "│  Padded Option  │\n" "└─────────────────┘"
        self.assertEqual(menu.menu, expected)

    # Test menu with minimum width enforced
    def test_menu_with_min_width(self):
        menu = Menu(menu_items=["Wide Menu"], min_width=30, style="double")
        expected = (
            "╔════════════════════════════╗\n"
            "║Wide Menu                   ║\n"
            "╚════════════════════════════╝"
        )
        self.assertEqual(menu.menu, expected)

    # Test menu with padding around items with  centered footer and header.
    def test_menu_with_padding_center_options(self):
        menu = Menu(
            menu_items=["Option 1"],
            header="Centered Header",
            footer="Centered Footer",
            min_width=21,
            style="single",
            align=("center", "left", "center"),
            padx=((0, 0), (2, 0), (0, 0)),
        )
        expected = (
            "┌───────────────────┐\n"
            "│  Centered Header  │\n"
            "├╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤\n"
            "│  Option 1         │\n"
            "├───────────────────┤\n"
            "│  Centered Footer  │\n"
            "└───────────────────┘"
        )
        self.assertEqual(menu.menu, expected)

    # Test invalid menu_items (non-list)
    def test_invalid_menu_items(self):
        with self.assertRaises(ValueError):
            Menu(menu_items="Invalid Items")  # Should be a list of strings

    # Test invalid numbering type
    def test_invalid_index(self):
        with self.assertRaises(ValueError):
            Menu(menu_items=["Option 1"], index="invalid")

    # Test invalid padding tuple
    def test_invalid_padx(self):
        with self.assertRaises(ValueError):
            Menu(menu_items=["Option 1"], padx=((1, 1), (1, -1), (0, 0)))

    # Test center and padx conflict
    def test_center_padx_conflict(self):
        with self.assertRaises(ValueError):
            Menu(
                menu_items=["Option 1"],
                align=("center", "left", "left"),
                padx=((1, 1), (0, 0), (0, 0)),
            )

    # Test multiple lines for header and footer
    def test_menu_with_multiline_header_footer(self):
        menu = Menu(
            menu_items=["Option 1"],
            header=["Line 1", "Line 2"],
            footer=["Footer 1", "Footer 2"],
        )
        expected = (
            "┌────────┐\n"
            "│Line 1  │\n"
            "│Line 2  │\n"
            "├╌╌╌╌╌╌╌╌┤\n"
            "│Option 1│\n"
            "├────────┤\n"
            "│Footer 1│\n"
            "│Footer 2│\n"
            "└────────┘"
        )
        self.assertEqual(menu.menu, expected)

    # Test the get_width method with
    def test_get_width(self):
        menu = Menu(
            menu_items=["A very wide option 1"],
            header="Header",
            footer="Footer",
            align=("left", "left", "left"),
            min_width=15,
        )
        self.assertEqual(menu.get_width(), 22)

    # Test the get_width method with multiple lines
    def test_get_width_multi_line(self):
        menu = Menu(
            menu_items=["Option 1", "Option 2"],
            header=["Header 1", "Header 2"],
            footer="Footer",
        )
        self.assertEqual(menu.get_width(), 10)

    # Test the get_height method
    def test_get_height(self):
        menu = Menu(
            menu_items=["Option 1"],
            header="Header",
            footer="Footer",
            align=("left", "left", "left"),
            min_width=21,
        )
        self.assertEqual(menu.get_height(), 7)

    # Test the get_height method with multiple lines
    def test_get_height_multi_line(self):
        menu = Menu(
            menu_items=["Option 1", "Option 2"],
            header=["Header 1", "Header 2"],
        )
        self.assertEqual(menu.get_height(), 7)

    # Test header with empty string in the list.
    def test_header_with_empty_string(self):
        menu = Menu(
            menu_items=["Option 1"],
            header=["", "Header 2"],
        )
        expected = (
            "┌────────┐\n"
            "│        │\n"
            "│Header 2│\n"
            "├╌╌╌╌╌╌╌╌┤\n"
            "│Option 1│\n"
            "└────────┘"
        )
        self.assertEqual(menu.menu, expected)

    # Test footer with empty string in the list.
    def test_footer_with_empty_string(self):
        menu = Menu(
            menu_items=["Option 1"],
            footer=["Footer 1", ""],
        )
        expected = (
            "┌────────┐\n"
            "│Option 1│\n"
            "├────────┤\n"
            "│Footer 1│\n"
            "│        │\n"
            "└────────┘"
        )
        self.assertEqual(menu.menu, expected)

    # Test options with empty string in the list.
    def test_options_with_empty_string(self):
        menu = Menu(
            menu_items=["Option 1", ""],
        )
        expected = (
            "┌────────┐\n" "│Option 1│\n" "├────────┤\n" "│        │\n" "└────────┘"
        )
        self.assertEqual(menu.menu, expected)


if __name__ == "__main__":
    unittest.main()
