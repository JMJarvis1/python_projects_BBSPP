import random
import datetime as dt
import os
import sys

sys.path.append(os.getcwd() + "/..")

from common_functions import clr_scrn, display_message, last_day_of_month


def main() -> None:
    # Min/max group size that can go to generator
    RNG_BIRTHDAYS: range = range(2, 101)
    TXT_WIDTH = 80

    intro_msg: list[str] = [
        "The Birthday Paradox".center(TXT_WIDTH),
        f"{"-"*30}".center(TXT_WIDTH),
        "",
        "The Birthday Paradox is a common name given to the surprisingly high probability of any two persons in an N sized group sharing the same birthday. In fact, the size of the group required for there to be a very high probability that any two people will share matching birthdays is much smaller than most people typically assume.",
        "",
        "For more information go to: https://en.wikipedia.org/wiki/Birthday_problem",
    ]
    clr_scrn()
    display_message(intro_msg, TXT_WIDTH)

    # Get user to input number of birthdays to generate
    # Loops until user inputs valid information.

    group_size: str = ""
    num_birthdays = 0
    while (not group_size.isdecimal()) | (num_birthdays not in RNG_BIRTHDAYS):
        group_size = input(
            "\nEnter the size of the group that you wish to generate birthdays for.\n> "
        )
        try:
            num_birthdays = int(group_size)

        except ValueError:
            continue

    # Generate and display the birthdays
    birthdays: list[str] = generate_birthdays(num_birthdays)
    display_birthdays(birthdays, num_birthdays)

    # Determine if two birthdays match
    match: str | None = get_match(birthdays)
    match_msg: str = ""
    if match is not None:
        match_msg += f"There is at least one pair of people in this simulation sharing a birthday on {match}.\n"
    else:
        match_msg += "There were no matches in this simulation.\n"

    display_message(match_msg, TXT_WIDTH)

    # TODO Run through 100_000 simulations

    # TODO Display simulation results


def generate_birthdays(numBirthdays: int) -> list[str]:
    """
    Generates and returns a list of birthdays of a specified length.

    :param numBirthdays: The number of birthdays to be generated
    :type numBirthdays: int
    :return: A list of birthdays of the following format: 'Nov 1'
    :rtype: list[str]

    :example:
    >>> birthdays: list[str] = generate_birthdays(42)
        print(birthdays)


    """
    birthdays: list[str] = []

    for i in range(numBirthdays):
        month: int = random.randint(1, 12)
        last_day: int = last_day_of_month(month)

        day: int = random.randint(1, last_day)
        birthday: dt.datetime = dt.datetime(year=1900, month=month, day=day)

        birthdays.append(birthday.strftime("%b %d"))
    return birthdays


def display_birthdays(birthdays: list[str], num_birthdays) -> None:
    "Formats and displays birthdays."

    print(f"\nHere are the generated birthdays for a group of {num_birthdays} people:")

    for i in range(len(birthdays) // 6 + 1):  # Print N rows of 6 dates
        index = i * 6
        print()
        ([print(f"{date}", end="    ") for date in birthdays[index : index + 6]])

    if len(birthdays) % 6 == 0:
        print()
    else:
        print("\n")


def get_match(birthdays: list[str]) -> str | None:
    """Returns a datetime object for a birthday that occurs more than once."""

    if len(birthdays) == len(set(birthdays)):
        pass
    else:
        for i, date in enumerate(birthdays):
            for candidate in birthdays[i + 1 :]:
                if date == candidate:
                    match = date
                    return match
    return None


if __name__ == "__main__":
    main()
