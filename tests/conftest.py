import pytest


@pytest.fixture
def default_message():
    """Basic message text fixture."""
    return "Hello World"


@pytest.fixture
def multi_line_message():
    """Multi-line message fixture."""
    return ["Line 1", "Line 2", "Line 3"]


@pytest.fixture
def message_styles(default_message):
    """Dictionary of expected message outputs for different styles."""
    return {
        "single": f"┌───────────┐\n│{default_message}│\n└───────────┘",
        "double": f"╔═══════════╗\n║{default_message}║\n╚═══════════╝",
        "simple": f"+-----------+\n|{default_message}|\n+-----------+",
        "bold": f"┏━━━━━━━━━━━┓\n┃{default_message}┃\n┗━━━━━━━━━━━┛",
    }


@pytest.fixture
def min_width():
    """Default minimum width for tests."""
    return 20


@pytest.fixture
def default_menu_items():
    """Basic menu items fixture."""
    return ["Option 1", "Option 2", "Option 3"]


@pytest.fixture
def menu_header():
    """Default menu header fixture."""
    return "Main Menu"


@pytest.fixture
def menu_footer():
    """Default menu footer fixture."""
    return "x) Exit"


@pytest.fixture
def menu_styles(menu_header, menu_footer, default_menu_items):
    """Dictionary of expected menu outputs for different styles."""
    return {
        "single": (
            "┌─────────┐\n"
            f"│{menu_header}│\n"
            "├╌╌╌╌╌╌╌╌╌┤\n"
            f"│{default_menu_items[0]} │\n"
            f"│{default_menu_items[1]} │\n"
            f"│{default_menu_items[2]} │\n"
            "├─────────┤\n"
            f"│{menu_footer}  │\n"
            "└─────────┘"
        ),
        "double": (
            "╔═════════╗\n"
            f"║{menu_header}║\n"
            "╠═════════╣\n"
            f"║{default_menu_items[0]} ║\n"
            f"║{default_menu_items[1]} ║\n"
            f"║{default_menu_items[2]} ║\n"
            "╠═════════╣\n"
            f"║{menu_footer}  ║\n"
            "╚═════════╝"
        ),
        "simple": (
            "+---------+\n"
            f"|{menu_header}|\n"
            "|=========|\n"
            f"|{default_menu_items[0]} |\n"
            f"|{default_menu_items[1]} |\n"
            f"|{default_menu_items[2]} |\n"
            "|---------|\n"
            f"|{menu_footer}  |\n"
            "+---------+"
        ),
        "bold": (
            "┏━━━━━━━━━┓\n"
            f"┃{menu_header}┃\n"
            "┣╍╍╍╍╍╍╍╍╍┫\n"
            f"┃{default_menu_items[0]} ┃\n"
            f"┃{default_menu_items[1]} ┃\n"
            f"┃{default_menu_items[2]} ┃\n"
            "┣━━━━━━━━━┫\n"
            f"┃{menu_footer}  ┃\n"
            "┗━━━━━━━━━┛"
        ),
    }
