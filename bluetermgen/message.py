from .helpers import calculate_inner_width, STYLES
from typing import Union, List, Tuple


class Message:
    """
    Generates a message with borders with different options.

    Args:
        message (str | list):
            The text for the message. Can be a string or a list of strings
            for multiple lines.

        align (str, optional):
            How to align the text. Defaults to `'left'`.

        min_width (int, optional):
            The minimum width of the frame. Defaults to `0`.

        style (str, optional):
            The frame style to use. Defaults to `'single'`.

        padx (tuple | int, optional):
            Padding to add around the text. Defaults to `(0, 0)`.

            Example:
            (1, 1) = (left, right)
            1 = (1, 1)

    Raises:
        ValueError:
            If the `'message'` property is not a string or a list of strings.

        ValueError:
            If the `'align'` property is not a string from the list:
            "left"
            "center"
            "right"

        ValueError:
            If the `'min_width'` property is not an integer.

        ValueError:
            If the `'style'` property is not a string.

        ValueError:
            If the `'padx'` property is not a tuple of length 2
            containing integers.

        ValueError:
            If the `'padx'` property is not an integer.

        ValueError:
            If the `'padx'` property is set
            while the `'align'` property is `"center"`.

    Example:
        >>> message = Message(["", "Hello World!", ""],
        ...                    style="double", align="center", min_width=20)
    """

    def __init__(
        self,
        message_text: Union[str, List],
        align: str = "left",
        min_width: int = 0,
        style: str = "single",
        padx: Union[Tuple, int] = (0, 0),
    ) -> None:

        self.message_text = message_text
        self.align = align
        self.min_width = min_width
        self.style = style
        self.padx = padx
        self._inner_width = self._calculate_width()
        self._width = 0
        self._height = 0
        self._message = self._generate_message()

    @property
    def message_text(self) -> Union[str, List]:
        return self._message_text

    @message_text.setter
    def message_text(self, value: Union[str, List]):
        if isinstance(value, str):
            self._message_text = value.split("\n")
        elif isinstance(value, list):
            self._message_text = value
        else:
            raise ValueError(
                """
                The 'message_text' property must be a string
                or a list of strings.
                """
            )

    @property
    def align(self) -> str:
        return self.__align

    @align.setter
    def align(self, value: str):
        if isinstance(value, str) and value in ["left", "center", "right"]:
            self.__align = value
        else:
            raise ValueError(
                "The 'align' property must be 'left', 'center', or 'right'"
            )

    @property
    def min_width(self) -> int:
        return self.__min_width

    @min_width.setter
    def min_width(self, value: int):
        if isinstance(value, int) and value >= 0:
            self.__min_width = value
        else:
            raise ValueError(
                "The 'min_width' property must be a non-negative integer."
            )

    @property
    def style(self) -> str:
        return self.__style

    @style.setter
    def style(self, value: str):
        valid_styles = list(STYLES.keys())
        if isinstance(value, str) and value in valid_styles:
            self.__style = STYLES[value]
        else:
            raise ValueError(
                f"The 'style' property must be one of {valid_styles}."
            )

    @property
    def padx(self) -> tuple:
        return self.__padx

    @padx.setter
    def padx(self, value: Union[Tuple, int]):
        if isinstance(value, int) and value >= 0:
            self.__padx = (value, value)
        elif (
            isinstance(value, tuple)
            and len(value) == 2
            and all(isinstance(x, int) and x >= 0 for x in value)
        ):
            self.__padx = value
        else:
            raise ValueError(
                "The 'padx' property must be a tuple of length 2 containing positive integers."
            )

        if (
            self.__align == "center"
            and self.__padx[0] > 0
            and self.__padx[1] > 0
        ):
            raise ValueError(
                "The 'padx' property cannot be used when 'align' is 'center'."
            )

    def get_width(self) -> int:
        """
        Returns:
            int: The entire width of the message including the borders.
        """
        return self._width

    def get_height(self) -> int:
        """
        Returns:
            int: The entire height of the message including the borders.
        """
        return self._height

    def _calculate_width(self) -> int:
        """
        Returns:
            int: The width of the message excluding the borders.
        """
        return calculate_inner_width(
            head=self._message_text,
            minimum_width=self.__min_width,
            padx=self.__padx,
        )

    def _generate_message(self) -> str:
        # Add the top line
        item = [
            f"{self.__style['tl']}"
            f"{self.__style['h'] * (self._inner_width)}"
            f"{self.__style['tr']}\n"
        ]

        # Get the width of the menu
        self._width = len(item[0].strip("\n"))

        # Add message lines
        for line in self._message_text:
            if self.align == "center":
                # Center align the line
                formatted_line = f"{line:^{self._inner_width}}"
            elif self.align == "right":
                # Right align the line with padding
                padding_left = " " * (
                    self._inner_width - len(line) - self.__padx[1]
                )
                padding_right = " " * self.__padx[1]
                formatted_line = f"{padding_left}{line}{padding_right}"
            else:
                # Left align the line with padding
                padding_left = " " * self.__padx[0]
                padding_right = " " * (
                    self._inner_width - len(line) - self.__padx[0]
                )
                formatted_line = f"{padding_left}{line}{padding_right}"

            item.append(
                f"{self.__style['v']}{formatted_line}{self.__style['v']}\n"
            )

        # Add the bottom line
        item.append(
            f"{self.__style['bl']}"
            f"{self.__style['h'] * self._inner_width}"
            f"{self.__style['br']}"
        )

        # Get the height of the menu
        self._height = len(item)

        return "".join(item)

    @property
    def message(self) -> str:
        return self._message

    def __str__(self) -> str:
        return self._message


if __name__ == "__main__":
    pass
