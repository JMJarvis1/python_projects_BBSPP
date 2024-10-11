"""Bagels - A deductive reasoning game where the player is asked to guess a number of a set length using the clues provided following each incorrect guess. The player wins if they guess correctly before running out of guesses"""

import sys
import random
import logging

MAX_GUESSES: int = 10  # Number of guesses available to the player
NUM_DIGITS: int = 3  # Length of the 'secret number'


def main() -> None:
    # Print Instructions to the player
    print(f"""
        I have created a secret number that is comprised of {NUM_DIGITS}
        non-repeating digits. You will have {MAX_GUESSES} chances to guess
        the number correctely. After each incorrect guess, you 
        will be presented with a series of clues indicating how 
        close your previous guess was to the secret number. 

        These clues are:
            Fermi:  You have a correct digit in the correct place.
            Pico:   You have a correct digit in an incorrect place.
            Bagels: You do not have any correct digits. 

        For Example: 
            If you guess 123 and the secret number is 413 then the
            clue you will receive will be "Pico Fermi". 
          """)

    # TODO Get secret number
    secret_num: str = get_secret_num()
    print("Hello, world?")
    # TODO Get player guess

    # TODO Get Clues

    # TODO Display clues or victor message

    # TODO Ask if player wants to play again


def get_secret_num() -> str:
    secret_num: str = ""

    nums: list[int] = [num for num in range(10)]

    random.shuffle(nums)
    try:
        sampled_nums: list[int] = random.sample(nums, NUM_DIGITS)
    except ValueError as e:
        logging.exception(f"\nA ValueError occurred: {e}")
        sys.exit()

    sampled_nums = [str(num) for num in sampled_nums]

    secret_num = "".join(sampled_nums)

    return secret_num


if __name__ == "__main__":
    main()
