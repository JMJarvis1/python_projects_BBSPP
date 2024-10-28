import os
import sys
import time
import textwrap
from typing import Literal


def clear_scrn() -> None:
    """Clear screen on 'nt' (windows) and posix (macOS, unix)"""
    os.system("cls" if os.name == "nt" else "clear")


def display_message(
    message: list[str] | str,
    txt_width: int = 80,
    msg_just: Literal["ljust", "rjust", "center"] = "ljust",
) -> None:
    """
    Format and display the text of the program.

    :param txt_width: width of the diplayed text, defaults to 80
    :type txt_width: int, optional

    """
    if isinstance(message, list):
        for line in message:
            if len(line) > txt_width:
                _print_long_message(line, txt_width)
            else:
                line = justify_txt(line, msg_just, txt_width)
                print(line)
    elif isinstance(message, str) & (len(message) > txt_width):
        _print_long_message(message, txt_width)
    else:
        print(message)


def exit_game():
    print("Exiting game", end="")

    for i in range(3):
        time.sleep(0.75)
        print(".", end="")
    time.sleep(0.5)
    clear_scrn()
    sys.exit()


def justify_txt(msg: str, msg_just: str, width: int, fillchar: str = " ") -> str:
    match msg_just:
        case "center":
            return msg.center(width, fillchar)
        case "rjust":
            return msg.rjust(width, fillchar)
        case _:
            return msg.ljust(width, fillchar)


def _print_long_message(message: str, txt_width: int = 80) -> None:
    """
    Displays text wrapped to a desired width.

    :param message: String to be displayed
    :type message: str
    :param txt_width: Width tet will be wrapped to.
    :type txt_width: int
    """
    long_msg: list = textwrap.wrap(message, txt_width)
    [print(line) for line in long_msg]


def month_end_date(month: int) -> int:
    """
    Returns the last day of a given month as an integer value.

    :param month: The month that we wish to find last day of.
    :type month: int
    :raises ValueError: Raised if the value of the month provided as an argument is not between 1 and 12 inclusive.
    :return date: The last day of the month.
    :rtype: int

    :Example:

    >>> last_day_of_month(2)  # Find last date in February
        28
    """
    if month not in range(1, 13):
        raise ValueError("An error occurred", "ValueError", f"month = {month}")

    date: int = 30
    match month:
        case 1 | 3 | 5 | 7 | 8 | 10 | 12:  # 31 day months
            date = 31
        case 2:
            date = 28  # February
        case _:
            pass  # Default

    return date


def play_again() -> bool:
    answer: str = ""
    while not answer.startswith(("Y", "N")):
        print("Would you like to play another game? (Y/N)")

        answer = input("> ").upper().strip()

    return True if answer == "Y" else False
