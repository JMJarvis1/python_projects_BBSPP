import os
import textwrap


def clear_scrn() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def display_message(message: list[str] | str, txt_width: int = 80) -> None:
    """
    Format and display the introductory text of the program.

    :param txt_width: width of the diplayed text, defaults to 80
    :type txt_width: int, optional

    """
    if isinstance(message, list):
        for line in message:
            if len(line) > txt_width:
                _print_long_message(line, txt_width)
            else:
                print(line)
    elif isinstance(message, str) & (len(message) > txt_width):
        _print_long_message(message, txt_width)
    else:
        print(message)


def _print_long_message(message, txt_width) -> None:
    long_msg: list[str] = textwrap.wrap(message, txt_width)
    [print(line) for line in long_msg]


def last_day_of_month(month: int) -> int:
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
