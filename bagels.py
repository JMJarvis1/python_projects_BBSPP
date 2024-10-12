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
    while True:  # Main game loop.
        # Get secret number
        secret_nums: list = get_secret_num()

        # Get player guess
        guess_count: int = 1

        while guess_count <= MAX_GUESSES:
            print(f"Guess #{guess_count}")

            guess: str = input("> ")

            guess_count += 1

            if guess == "".join(str(secret_nums)):
                print("You got it!")  # Player wins
                break

            # Generate and display clue
            clue: str = get_clue(guess, secret_nums)
            print(clue)

        # TODO Ask if player wants to play again
        keep_playing: bool = play_new_game()

        if not keep_playing:
            break


def get_secret_num() -> list[int]:
    nums: list[int] = [num for num in range(10)]

    random.shuffle(nums)
    try:
        sampled_nums: list[int] = random.sample(nums, NUM_DIGITS)
    except ValueError as e:
        logging.exception(f"\nA ValueError occurred: {e}")
        sys.exit()

    return [str(num) for num in sampled_nums]


def get_clue(guess, secret_num) -> str:
    clues: list[str] = []

    for i in NUM_DIGITS:
        if guess[i] == secret_num[i]:
            clues.append("Fermi")
        elif guess[i] in secret_num:
            clues.append("Pico")

    if len(clues) == 0:
        return "Bagels"
    else:
        return " ".join(clues)


def play_new_game() -> bool:
    response = input("Would you like to play again? (y/n)\n> ")

    return True if response.startswith("y") else False


if __name__ == "__main__":
    main()
