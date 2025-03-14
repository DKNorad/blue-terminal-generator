import unittest
from bluetermgen.table import Table
from bluetermgen.exceptions import ValidationError


class TestTable(unittest.TestCase):

    # Test table with default left alignment
    def test_default_left_aligned_table(self):
        data = [["Header 1", "Header 2"], [1, 123456], [300, 4]]
        table = Table(data)
        expected = (
            "┌────────┬────────┐\n"
            "│Header 1│Header 2│\n"
            "├╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌┤\n"
            "│1       │123456  │\n"
            "│300     │4       │\n"
            "└────────┴────────┘"
        )
        self.assertEqual(str(table), expected)

    # Test table with center alignment for both header and data
    def test_center_aligned_table(self):
        data = [["Header 1", "Header 2"], [1, 123456], [300, 4]]
        table = Table(data, align=("center", "center"))
        expected = (
            "┌────────┬────────┐\n"
            "│Header 1│Header 2│\n"
            "├╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌┤\n"
            "│   1    │ 123456 │\n"
            "│  300   │   4    │\n"
            "└────────┴────────┘"
        )
        self.assertEqual(str(table), expected)

    # Test table with separate header and data alignment
    def test_header_left_data_right_aligned_table(self):
        data = [["Header 1", "Header 2"], [1, 123456], [300, 4]]
        table = Table(data, align=("left", "right"))
        expected = (
            "┌────────┬────────┐\n"
            "│Header 1│Header 2│\n"
            "├╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌┤\n"
            "│       1│  123456│\n"
            "│     300│       4│\n"
            "└────────┴────────┘"
        )
        self.assertEqual(str(table), expected)

    # Test table with mixed alignment (header center, data right)
    def test_header_center_data_right_aligned_table(self):
        data = [["Header 1", "Header 2"], [1, 123456], [300, 4]]
        table = Table(data, align=("center", "right"))
        expected = (
            "┌────────┬────────┐\n"
            "│Header 1│Header 2│\n"
            "├╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌┤\n"
            "│       1│  123456│\n"
            "│     300│       4│\n"
            "└────────┴────────┘"
        )
        self.assertEqual(str(table), expected)

    # Test table with padding and alignment
    def test_table_with_padding_and_alignment(self):
        data = [["Header 1", "Header 2"], [1, 1234567890], [300, 4]]
        table = Table(data, align=("center", "right"), padx=((0, 0), (0, 2)))
        expected = (
            "┌────────┬────────────┐\n"
            "│Header 1│  Header 2  │\n"
            "├╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌┤\n"
            "│     1  │1234567890  │\n"
            "│   300  │         4  │\n"
            "└────────┴────────────┘"
        )
        self.assertEqual(str(table), expected)

    # Test table with row separator and mixed alignments
    def test_table_with_row_separator_and_mixed_alignment(self):
        data = [["Header 1", "Header 2"], [1, 123456], [300, 4]]
        table = Table(data, align=("left", "right"), row_sep=True)
        expected = (
            "┌────────┬────────┐\n"
            "│Header 1│Header 2│\n"
            "├╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌┤\n"
            "│       1│  123456│\n"
            "├────────┼────────┤\n"
            "│     300│       4│\n"
            "└────────┴────────┘"
        )
        self.assertEqual(str(table), expected)

    # Test table with complex data (list of dictionaries)
    def test_table_list_of_dicts(self):
        data = [
            {"Name": "Alice", "Age": 30},
            {"Name": "Bob", "Age": 25},
            {"Name": "Charlie", "Age": 35},
        ]
        table = Table(data, align=("left", "right"))
        expected = (
            "┌───────┬───┐\n"
            "│Name   │Age│\n"
            "├╌╌╌╌╌╌╌┼╌╌╌┤\n"
            "│  Alice│ 30│\n"
            "│    Bob│ 25│\n"
            "│Charlie│ 35│\n"
            "└───────┴───┘"
        )
        self.assertEqual(str(table), expected)

    # Test table with variable width
    def test_variable_width_table(self):
        data = [["Header 1", "Header 2"], ["Short", "Very very long text"]]
        table = Table(data)
        expected = (
            "┌────────┬───────────────────┐\n"
            "│Header 1│Header 2           │\n"
            "├╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤\n"
            "│Short   │Very very long text│\n"
            "└────────┴───────────────────┘"
        )
        self.assertEqual(str(table), expected)

    # Test table with custom alignment (right-aligned)
    def test_right_aligned_table(self):
        data = [["Header 1", "Header 2"], [1, 123456], [300, 4]]
        table = Table(data, align=("right", "right"))
        expected = (
            "┌────────┬────────┐\n"
            "│Header 1│Header 2│\n"
            "├╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌┤\n"
            "│       1│  123456│\n"
            "│     300│       4│\n"
            "└────────┴────────┘"
        )
        self.assertEqual(str(table), expected)

    # Test table with mixed data types
    def test_mixed_data_types(self):
        data = [["Header 1", "Header 2"], [123, None], ["Text", 456.789]]
        table = Table(data)
        expected = (
            "┌────────┬────────┐\n"
            "│Header 1│Header 2│\n"
            "├╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌┤\n"
            "│123     │None    │\n"
            "│Text    │456.789 │\n"
            "└────────┴────────┘"
        )
        self.assertEqual(str(table), expected)

    # Test table with single border style
    def test_table_with_single_style(self):
        data = [["Header 1", "Header 2"], ["Cell 1", "Cell 2"]]
        table = Table(data, style="single")
        expected = (
            "┌────────┬────────┐\n"
            "│Header 1│Header 2│\n"
            "├╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌┤\n"
            "│Cell 1  │Cell 2  │\n"
            "└────────┴────────┘"
        )
        self.assertEqual(str(table), expected)

    # Test table with double border style
    def test_table_with_double_style(self):
        data = [["Header 1", "Header 2"], ["Cell 1", "Cell 2"]]
        table = Table(data, style="double")
        expected = (
            "╔════════╦════════╗\n"
            "║Header 1║Header 2║\n"
            "╠════════╬════════╣\n"
            "║Cell 1  ║Cell 2  ║\n"
            "╚════════╩════════╝"
        )
        self.assertEqual(str(table), expected)

    # Test table with ASCII border style
    def test_table_with_simple_style(self):
        data = [["Header 1", "Header 2"], ["Cell 1", "Cell 2"]]
        table = Table(data, style="simple")
        expected = (
            "+--------+--------+\n"
            "|Header 1|Header 2|\n"
            "|========+========|\n"
            "|Cell 1  |Cell 2  |\n"
            "+--------+--------+"
        )
        self.assertEqual(str(table), expected)

    # Test table with empty rows
    def test_empty_rows(self):
        data = [["Header 1", "Header 2"], ["", ""]]
        table = Table(data)
        expected = (
            "┌────────┬────────┐\n"
            "│Header 1│Header 2│\n"
            "├╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌┤\n"
            "│        │        │\n"
            "└────────┴────────┘"
        )
        self.assertEqual(str(table), expected)

    # Test invalid table data (non-list input)
    def test_invalid_data(self):
        with self.assertRaises(ValidationError):
            Table("Invalid Data")  # Should be a list of lists or dicts

    # Test table with very long header
    def test_long_header(self):
        data = [
            ["Short", "A very long header"],
            ["123", "A long cell content"],
        ]
        table = Table(data)
        expected = (
            "┌─────┬───────────────────┐\n"
            "│Short│A very long header │\n"
            "├╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤\n"
            "│123  │A long cell content│\n"
            "└─────┴───────────────────┘"
        )
        self.assertEqual(str(table), expected)

    # Test table with very long cell content
    def test_long_cell_content(self):
        data = [["Header 1", "Header 2"], ["Short", "A" * 100]]
        table = Table(data)
        expected = (
            "┌────────┬────────────────────────────────────────────────────────────────────────────────────────────────────┐\n"
            "│Header 1│Header 2                                                                                            │\n"
            "├╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤\n"
            "│Short   │AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA│\n"
            "└────────┴────────────────────────────────────────────────────────────────────────────────────────────────────┘"
        )
        self.assertEqual(str(table), expected)

    # Test large table with many rows (performance)
    def test_large_table(self):
        data = [["Header 1", "Header 2"]] + [
            [f"Row {i} Col 1", f"Row {i} Col 2"] for i in range(1000)
        ]
        table = Table(data)
        output = str(table)
        self.assertTrue(len(output) > 1000)

    # Test get_dimensions function for basic width data
    def test_get_width_basic(self):
        data = [["Header 1", "Header 2"], ["Cell 1", "Cell 2"]]
        table = Table(data)
        expected_width = 19
        width, _ = table.get_dimensions()
        self.assertEqual(width, expected_width)

    # Test get_dimensions function with longer data
    def test_get_width_long_data(self):
        data = [
            ["Short", "A very long header"],
            ["123", "A long cell content"],
        ]
        table = Table(data)
        expected_width = 27
        width, _ = table.get_dimensions()
        self.assertEqual(width, expected_width)

    # Test get_dimensions function for basic height data
    def test_get_height_basic(self):
        data = [["Header 1", "Header 2"], ["Cell 1", "Cell 2"]]
        table = Table(data)
        expected_height = 5
        _, height = table.get_dimensions()
        self.assertEqual(height, expected_height)

    # Test get_dimensions function with multi-line cells
    def test_get_height_multiline(self):
        data = [
            ["Header 1", "Header 2"],
            ["Cell 1", "Line 1\nLine 2\nLine 3"],
            ["Row 3", "Cell 2"],
        ]
        table = Table(data)
        expected_height = 8
        _, height = table.get_dimensions()
        self.assertEqual(height, expected_height)

    # Test get_dimensions with padding applied
    def test_get_width_with_padding(self):
        data = [["Header 1", "Header 2"], ["Cell 1", "Cell 2"]]
        table = Table(data, padx=((2, 2), (3, 1)))  # Custom padding
        expected_width_col1 = (
            max(len("Header 1"), len("Cell 1")) + 2 + 2
        )  # padding 2 on each side
        expected_width_col2 = (
            max(len("Header 2"), len("Cell 2")) + 3 + 1
        )  # padding 3 left, 1 right
        expected_width = (
            expected_width_col1 + expected_width_col2 + 3
        )  # add separator spaces
        width, _ = table.get_dimensions()
        self.assertEqual(width, expected_width)


if __name__ == "__main__":
    unittest.main()
