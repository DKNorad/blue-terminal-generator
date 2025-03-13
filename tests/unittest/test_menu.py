import unittest
from bluetermgen.menu import Menu
from bluetermgen.exceptions import ValidationError, PaddingError


class TestMenuStyles(unittest.TestCase):

    def setUp(self):
        self.menu_items = ["Option 1", "Option 2", "Option 3"]
        self.header = "Main Menu"
        self.footer = "x) Exit"
        self.styles = {
            "single": (
                "┌─────────┐\n"
                f"│{self.header}│\n"
                "├╌╌╌╌╌╌╌╌╌┤\n"
                f"│{self.menu_items[0]} │\n"
                f"│{self.menu_items[1]} │\n"
                f"│{self.menu_items[2]} │\n"
                "├─────────┤\n"
                f"│{self.footer}  │\n"
                "└─────────┘"
            ),
            "double": (
                "╔═════════╗\n"
                f"║{self.header}║\n"
                "╠═════════╣\n"
                f"║{self.menu_items[0]} ║\n"
                f"║{self.menu_items[1]} ║\n"
                f"║{self.menu_items[2]} ║\n"
                "╠═════════╣\n"
                f"║{self.footer}  ║\n"
                "╚═════════╝"
            ),
            "simple": (
                "+---------+\n"
                f"|{self.header}|\n"
                "|=========|\n"
                f"|{self.menu_items[0]} |\n"
                f"|{self.menu_items[1]} |\n"
                f"|{self.menu_items[2]} |\n"
                "|---------|\n"
                f"|{self.footer}  |\n"
                "+---------+"
            ),
            "bold": (
                "┏━━━━━━━━━┓\n"
                f"┃{self.header}┃\n"
                "┣╍╍╍╍╍╍╍╍╍┫\n"
                f"┃{self.menu_items[0]} ┃\n"
                f"┃{self.menu_items[1]} ┃\n"
                f"┃{self.menu_items[2]} ┃\n"
                "┣━━━━━━━━━┫\n"
                f"┃{self.footer}  ┃\n"
                "┗━━━━━━━━━┛"
            ),
        }

    def test_various_styles(self):
        """[Menu] Test that each style renders correctly with the expected_output border format"""
        for style, expected_output_output in self.styles.items():
            with self.subTest(style=style):
                menu = Menu(
                    menu_items=self.menu_items,
                    header=self.header,
                    footer=self.footer,
                    style=style,
                )
                self.assertEqual(menu.menu, expected_output_output)


class TestMenuBasicRendering(unittest.TestCase):

    def setUp(self):
        self.default_menu_items = ["Option 1", "Option 2", "Option 3"]
        self.default_header = "Main Menu"
        self.default_footer = "x) Exit"

    def test_basic_menu(self):
        """[Menu] Test rendering of basic menu without header or footer."""
        menu = Menu(menu_items=self.default_menu_items)
        expected_output = (
            "┌────────┐\n"
            "│Option 1│\n"
            "│Option 2│\n"
            "│Option 3│\n"
            "└────────┘"
        )
        self.assertEqual(menu.menu, expected_output)

    def test_str_method(self):
        """[Menu] Test the __str__ dunder method for basic menu."""
        menu = Menu(menu_items=self.default_menu_items)
        self.assertEqual(str(menu), menu.menu)

    def test_menu_with_header_footer(self):
        """[Menu] Test rendering of menu with header and footer."""
        menu = Menu(
            menu_items=self.default_menu_items,
            header=self.default_header,
            footer=self.default_footer,
        )
        expected_output = (
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
        self.assertEqual(str(menu), expected_output)

    def test_menu_with_empty_items(self):
        """[Menu] Test rendering of menu with empty menu items."""
        with self.assertRaises(ValidationError):
            Menu(menu_items=[])


class TestMenuIndexing(unittest.TestCase):

    def setUp(self):
        self.default_menu_items = ["Option 1", "Option 2"]

    def test_menu_with_letter_index_upper_dot(self):
        """[Menu] Test menu with letter-based numbering (uppercase, dot)."""
        menu = Menu(
            menu_items=self.default_menu_items, index="letter.upper.dot"
        )
        expected_output = (
            "┌───────────┐\n"
            "│A. Option 1│\n"
            "│B. Option 2│\n"
            "└───────────┘"
        )
        self.assertEqual(menu.menu, expected_output)

    def test_menu_with_number_index_dot(self):
        """[Menu] Test menu with number-based numbering (number, dot)."""
        menu = Menu(menu_items=self.default_menu_items, index="number.dot")
        expected_output = (
            "┌───────────┐\n"
            "│1. Option 1│\n"
            "│2. Option 2│\n"
            "└───────────┘"
        )
        self.assertEqual(menu.menu, expected_output)

    def test_invalid_index_type(self):
        """[Menu] Test invalid numbering type."""
        with self.assertRaises(ValidationError):
            Menu(menu_items=self.default_menu_items, index="invalid")


class TestMenuAlignment(unittest.TestCase):

    def setUp(self):
        self.default_menu_items = ["Option 1"]
        self.default_header = "Centered Header"
        self.default_footer = "Centered Footer"
        self.min_width = 21

    def test_center_header_footer(self):
        """[Menu] Test center alignment of header and footer."""
        menu = Menu(
            menu_items=self.default_menu_items,
            header=self.default_header,
            footer=self.default_footer,
            align=("center", "left", "center"),
            min_width=self.min_width,
        )
        expected_output = (
            "┌───────────────────┐\n"
            "│  Centered Header  │\n"
            "├╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤\n"
            "│Option 1           │\n"
            "├───────────────────┤\n"
            "│  Centered Footer  │\n"
            "└───────────────────┘"
        )
        self.assertEqual(menu.menu, expected_output)

    def test_right_header_footer(self):
        """[Menu] Test right alignment of header and footer."""
        menu = Menu(
            menu_items=self.default_menu_items,
            header="Right Header",
            footer="Right Footer",
            align=("right", "left", "right"),
            min_width=self.min_width,
        )
        expected_output = (
            "┌───────────────────┐\n"
            "│       Right Header│\n"
            "├╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤\n"
            "│Option 1           │\n"
            "├───────────────────┤\n"
            "│       Right Footer│\n"
            "└───────────────────┘"
        )
        self.assertEqual(menu.menu, expected_output)


class TestMenuPadding(unittest.TestCase):

    def setUp(self):
        self.default_menu_items = ["Padded Option"]

    def test_padding_on_options(self):
        """[Menu] Test padding on menu options."""
        menu = Menu(
            menu_items=self.default_menu_items,
            padx=((0, 0), (2, 2), (0, 0)),
            style="single",
        )
        expected_output = (
            "┌─────────────────┐\n"
            "│  Padded Option  │\n"
            "└─────────────────┘"
        )
        self.assertEqual(menu.menu, expected_output)

    def test_right_aligned_with_padding(self):
        """[Menu] Test right alignment with padding."""
        menu = Menu(
            menu_items=["Option 1"],
            align=("left", "right", "left"),
            min_width=21,
            padx=((0, 0), (2, 2), (0, 0)),
        )
        expected_output = (
            "┌───────────────────┐\n"
            "│         Option 1  │\n"
            "└───────────────────┘"
        )
        self.assertEqual(menu.menu, expected_output)

    def test_invalid_padx(self):
        """[Menu] Test invalid padding tuple."""
        with self.assertRaises(PaddingError):
            Menu(menu_items=["Option 1"], padx=((1, 1), (1, -1), (0, 0)))


class TestMenuErrorHandling(unittest.TestCase):

    def test_invalid_menu_items(self):
        """[Menu] Test invalid menu_items (non-list)."""
        with self.assertRaises(ValidationError):
            Menu(menu_items="Invalid Items")  # Should be a list of strings

    def test_invalid_index(self):
        """[Menu] Test invalid numbering type."""
        with self.assertRaises(ValidationError):
            Menu(menu_items=["Option 1"], index="invalid")

    def test_center_padx_conflict(self):
        """[Menu] Test center and padx conflict."""
        with self.assertRaises(PaddingError):
            Menu(
                menu_items=["Option 1"],
                align=("center", "left", "left"),
                padx=((1, 1), (0, 0), (0, 0)),
            )


if __name__ == "__main__":
    unittest.main()
