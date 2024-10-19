import random
import datetime as dt
import os
import sys

sys.path.append(os.getcwd() + "/..")

from common_functions import clear_scrn, display_message, last_day_of_month


def main() -> None:
    # Settings
    rng_grp_size: range = range(2, 101)  # Number of people in grp (2-100)
    txt_width = 80  # Maximum width in chracters of displayed text.
    num_sims = 100_000  # Number of simulations to run

    intro_msg: list[str] = [
        "The Birthday Paradox".center(txt_width),
        f"{"-"*30}".center(txt_width),
        "",
        "The Birthday Paradox is a common name given to the surprisingly high probability of any two people in an N sized group sharing the same birthday. In fact, the size of the group required for there to be a very high probability that any two people will share matching birthdays is much smaller than most people typically assume.",
        "",
        "For more information go to: https://en.wikipedia.org/wiki/Birthday_problem",
    ]
    input_msg: str = f"\nEnter the size of the group that you wish to generate birthdays for: ({rng_grp_size.start}-{rng_grp_size.stop - 1}):"

    clear_scrn()
    display_message(intro_msg, txt_width)

    # Loops until user inputs valid group sise to generate birthdays for.
    grp_size: int = get_group_size(rng_grp_size, txt_width, input_msg)

    # Generate and display the birthdays
    birthdays: list[str] = generate_birthdays(grp_size)
    display_birthdays(birthdays)

    # Determine if two birthdays match
    match: str | None = get_match(birthdays)
    match_msg: str = ""
    if match is not None:
        match_msg += f"There is at least one pair of people in this simulation sharing a birthday on {match}.\n"
    else:
        match_msg += "There were no matches in this simulation.\n"

    display_message(match_msg, txt_width)

    # Run through 100_000 simulations
    sim_message = f"\nNow the program will run {num_sims:,} simulations on a group of {grp_size} people:\n"
    display_message(sim_message)

    sim_matches: int = run_simulations(num_sims, grp_size)

    sim_ratio = sim_matches * 100 / num_sims

    # Display simulation results
    sim_results_msg = f"\nOut of {num_sims:,} simulations of {grp_size} people run, {sim_matches:,} simulations resulted in at least two person sharing the same birthday. That is a ratio of {round(sim_ratio)}%!\n"
    display_message(sim_results_msg)

    sys.exit()


def get_message(msg_name):
    messages = {}


def run_simulations(num_sims: int, grp_size: int) -> int:
    """
    Runs multiple iterations of the birthday paradox simulation.

    :param num_sims: The number of iterations to run.
    :type num_sims: int
    :param grp_size: Group size to generate birthdays for.
    :type grp_size: int
    :return sim_matches: Number of total matches from all simulations
    :rtype: int
    """
    # Initialize count of sims with matching birthdays.
    sim_matches: int = 0
    for sim_count in range(num_sims):
        birthdays = generate_birthdays(grp_size)
        match = get_match(birthdays)

        if match is not None:
            sim_matches += 1

        sim_count += 1

        if sim_count % 10_000 == 0:
            print(f"{sim_count:,} simulations run...")

        if sim_count == num_sims:
            print("\nAll simulations successfully run.")
    return sim_matches


def get_group_size(rng_grp_size: range, txt_width: int, input_msg: str) -> int:
    """
    _summary_

    :param rng_grp_size: Allowed size range for group.
    :type rng_grp_size: range
    :param txt_width: Width of text in characters to display.
    :type txt_width: int
    :param input_msg: User imput prompt for group size.
    :type input_msg: str
    :raises ValueError: Raise for invalid user input
    :return grp_size: Number of people in group
    :rtype: int
    """
    while True:
        try:
            display_message(input_msg, txt_width)
            grp_size = int(input("> "))
            if grp_size not in rng_grp_size:
                raise ValueError
            else:
                break
        except ValueError:
            print(
                f"\nError: Please type a numbers that is between {rng_grp_size.start} and {rng_grp_size.stop - 1} inclusive."
            )

    return grp_size


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


def display_birthdays(birthdays: list[str]) -> None:
    """
    Formats and displays birthdays.

    :param birthdays: List of generated birthdays in the format of 'Nov 01'.
    :type birthdays: list[str]
    """

    print(f"\nHere are the generated birthdays for a group of {len(birthdays)} people:")

    for i in range(len(birthdays) // 6 + 1):  # Print N rows of 6 dates
        index = i * 6
        print()
        ([print(f"{date}", end="    ") for date in birthdays[index : index + 6]])

    if len(birthdays) % 6 == 0:
        print()
    else:
        print("\n")


def get_match(birthdays: list[str]) -> str | None:
    """
    Returns a datetime object for a birthday that occurs more than once.

    :param birthdays: List of generated birthdays in the format of 'Nov 01'.
    :type birthdays: list[str]
    :return: Date (i.e. 'Nov 1') of first birthday with a match or None
    :rtype: str | None
    """

    if len(birthdays) != len(set(birthdays)):
        for i, first_date in enumerate(birthdays):
            for second_date in birthdays[i + 1 :]:
                if first_date == second_date:
                    match = first_date
                    return match
    return None


if __name__ == "__main__":
    main()
