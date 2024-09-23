import unittest
from bluetermgen.menu import Menu


class TestMenu(unittest.TestCase):

    # Test basic menu without header or footer
    def test_basic_menu(self):
        menu = Menu(menu_items=["Option 1", "Option 2", "Option 3"])
        expected = (
            "┌────────┐\n"
            "│Option 1│\n"
            "│Option 2│\n"
            "│Option 3│\n"
            "└────────┘"
        )
        self.assertEqual(menu.menu, expected)

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
            "├─────────┤\n"
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
            numbering_type="letter_upper_dot",
        )
        expected = (
            "┌───────────┐\n"
            "│A. Option 1│\n"
            "│B. Option 2│\n"
            "└───────────┘"
        )
        self.assertEqual(menu.menu, expected)

    # Test menu with letter-based numbering (lowercase, dot)
    def test_menu_letter_lower_dot(self):
        menu = Menu(
            menu_items=["Option 1", "Option 2"],
            numbering_type="letter_lower_dot",
        )
        expected = (
            "┌───────────┐\n"
            "│a. Option 1│\n"
            "│b. Option 2│\n"
            "└───────────┘"
        )
        self.assertEqual(menu.menu, expected)

    # Test menu with number-based numbering (number, dot)
    def test_menu_number_dot(self):
        menu = Menu(
            menu_items=["Option 1", "Option 2"], numbering_type="number_dot"
        )
        expected = (
            "┌───────────┐\n"
            "│1. Option 1│\n"
            "│2. Option 2│\n"
            "└───────────┘"
        )
        self.assertEqual(menu.menu, expected)

    # Test menu with letter-based numbering (uppercase, parentheses)
    def test_menu_letter_upper_parantheses(self):
        menu = Menu(
            menu_items=["Option 1", "Option 2"],
            numbering_type="letter_upper_parentheses",
        )
        expected = (
            "┌───────────┐\n"
            "│A) Option 1│\n"
            "│B) Option 2│\n"
            "└───────────┘"
        )
        self.assertEqual(menu.menu, expected)

    # Test menu with letter-based numbering (lowercase, parentheses)
    def test_menu_letter_lower_parantheses(self):
        menu = Menu(
            menu_items=["Option 1", "Option 2"],
            numbering_type="letter_lower_parentheses",
        )
        expected = (
            "┌───────────┐\n"
            "│a) Option 1│\n"
            "│b) Option 2│\n"
            "└───────────┘"
        )
        self.assertEqual(menu.menu, expected)

    # Test menu with number-based numbering (number, parentheses)
    def test_menu_number_parentheses(self):
        menu = Menu(
            menu_items=["Option 1", "Option 2"],
            numbering_type="number_parentheses",
        )
        expected = (
            "┌───────────┐\n"
            "│1) Option 1│\n"
            "│2) Option 2│\n"
            "└───────────┘"
        )
        self.assertEqual(menu.menu, expected)

    # Test center alignment of header and footer
    def test_center_header_footer(self):
        menu = Menu(
            menu_items=["Option 1"],
            header="Centered Header",
            footer="Centered Footer",
            center=(True, False, True),
            min_width=21,
        )
        expected = (
            "┌───────────────────┐\n"
            "│  Centered Header  │\n"
            "├───────────────────┤\n"
            "│Option 1           │\n"
            "├───────────────────┤\n"
            "│  Centered Footer  │\n"
            "└───────────────────┘"
        )
        self.assertEqual(menu.menu, expected)

    # Test padding on menu options
    def test_menu_with_padding_on_options(self):
        menu = Menu(
            menu_items=["Padded Option"],
            padx=((0, 0), (2, 2), (0, 0)),
            style="single",
        )
        expected = (
            "┌─────────────────┐\n"
            "│  Padded Option  │\n"
            "└─────────────────┘"
        )
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
            center=(True, False, True),
            padx=((0, 0), (2, 0), (0, 0)),
        )
        expected = (
            "┌───────────────────┐\n"
            "│  Centered Header  │\n"
            "├───────────────────┤\n"
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
    def test_invalid_numbering_type(self):
        with self.assertRaises(ValueError):
            Menu(menu_items=["Option 1"], numbering_type="invalid")

    # Test invalid padding tuple
    def test_invalid_padx(self):
        with self.assertRaises(ValueError):
            Menu(menu_items=["Option 1"], padx=((1, 1), (1, -1), (0, 0)))

    # Test center and padx conflict
    def test_center_padx_conflict(self):
        with self.assertRaises(ValueError):
            Menu(
                menu_items=["Option 1"],
                center=(True, False, False),
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
            "├────────┤\n"
            "│Option 1│\n"
            "├────────┤\n"
            "│Footer 1│\n"
            "│Footer 2│\n"
            "└────────┘"
        )
        self.assertEqual(menu.menu, expected)


if __name__ == "__main__":
    unittest.main()
