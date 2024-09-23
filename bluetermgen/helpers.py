def calculate_inner_width(
    head: list,
    foot: str = None,
    opt: list = None,
    minimum_width: int = 0,
    padx: tuple = (0, 0),
) -> int:
    """
    Help function to calculate the width of the item based on the longest
        string in the item. Used for 'message' and 'menu'.

    Args:
        header (list):
            The header to calculate the width for.
        footer (str, optional):
            The footer to calculate the width for. Defaults to None.
        options (list, optional):
            The menu options to calculate the width for. Defaults to None.
        min_width (int, optional):
            The minimum width of the item. Defaults to 0.
        padx (tuple, optional):
            Padding to add around the header, footer, and options. Defaults to 0.
            - For message:
            (a, b) = (left, right)


            - For menu:
            (1, 1) = (left, right)
            ((1, 1), (1, 1), (1, 1)) = ((header), (footer), (options))
            1 = (1, 1)

    Returns:
        int: The width of the item.
    """

    if padx:
        # If padx is a list of two integers, apply to all parts
        if len(padx) == 2 and all(isinstance(x, int) for x in padx):
            lpad, rpad = padx

        # If padx has nested tuples with specific
        # paddings for head, opt, and foot
        elif len(padx) == 3 and all(
            len(p) == 2 and all(isinstance(x, int) for x in p) for p in padx
        ):
            (lpad, rpad), (opt_lpad, opt_rpad), (foot_lpad, foot_rpad) = padx

        head = [f"{' ' * lpad}{h}{' ' * rpad}" for h in head] if head else head
        opt = (
            [f"{' ' * opt_lpad}{o}{' ' * opt_rpad}" for o in opt]
            if opt
            else opt
        )
        foot = (
            [f"{' ' * foot_lpad}{f}{' ' * foot_rpad}" for f in foot]
            if foot
            else foot
        )

    max_str_width = max(
        max(len(h) for h in head) if head else 0,
        max(len(f) for f in foot) if foot else 0,
        max(len(o) for o in opt) if opt else 0,
    )

    width = (
        max_str_width if max_str_width > minimum_width else minimum_width - 2
    )

    return width


""" Styles legend:
tl - top left
tr - top right
bl - bottom left
br - bottom right
h - horizontal
v - vertical
c - cross
ml - middle left
mr - middle right
mt - middle top
mb - middle bottom
"""
DOUBLE_STYLE = {
    "tl": "╔",
    "tr": "╗",
    "bl": "╚",
    "br": "╝",
    "h": "═",
    "v": "║",
    "c": "╬",
    "ml": "╠",
    "mr": "╣",
    "mt": "╦",
    "mb": "╩",
}
SINGLE_STYLE = {
    "tl": "┌",
    "tr": "┐",
    "bl": "└",
    "br": "┘",
    "h": "─",
    "v": "│",
    "c": "┼",
    "ml": "├",
    "mr": "┤",
    "mt": "┬",
    "mb": "┴",
}
ASCII_STYLE = {
    "tl": "+",
    "tr": "+",
    "bl": "+",
    "br": "+",
    "h": "-",
    "v": "|",
    "c": "+",
    "ml": "+",
    "mr": "+",
    "mt": "+",
    "mb": "+",
}

STYLES = {
    "double": DOUBLE_STYLE,
    "single": SINGLE_STYLE,
    "ascii": ASCII_STYLE,
}
