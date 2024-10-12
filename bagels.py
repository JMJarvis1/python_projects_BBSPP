"""Bagels - A deductive reasoning game where the player is asked to guess a number of a set length using the clues provided following each incorrect guess. The player wins if they guess correctly before running out of guesses"""

import sys
import random
import logging
import os


MAX_GUESSES: int = 10  # Number of guesses available to the player
NUM_DIGITS: int = 3  # Length of the secret number


def main() -> None:
    while True:  # Main game loop.
        # Print title and game instructions
        print_intro()

        # Get secret number
        secret_nums: list = get_secret_num()

        # Get player guess
        guess_count: int = 1

        while guess_count <= MAX_GUESSES:
            print(f"Guess #{guess_count}")

            guess: str = input("> ")  # Player input

            if not validate_guess(guess):
                continue

            guess_count += 1

            if guess == "".join(secret_nums):
                print("You got it!")  # Player wins
                break

            # Generate and display clue
            clue: str = get_clue(guess, secret_nums)
            print(clue)

        clr_scrn()
        print("\nYou have run out of guesses.\n")
        # Ask if player wants to play again
        keep_playing: bool = play_new_game()

        if not keep_playing:
            break

    clr_scrn()
    sys.exit()


def print_intro() -> None:
    clr_scrn()

    title_msg: str = "Bagels"

    instruction_msg: str = f"""
        Instructions:
          
            I have created a secret number that is comprised of {NUM_DIGITS}
            unique digits. 
            
            You will have {MAX_GUESSES} chances to guess this number
            correctly. 
            
            After each incorrect guess, you will be presented with 
            a series of clues indicating:
                1. Whether one or more digits from your guess matches
                   a digit from the secret number. 
                2. Whether one or more of your matching digits is in the
                   correct place.
                   
            There are three possible clues:
                Fermi:  You have a correct digit in the correct place.
                Pico:   You have a correct digit in an incorrect place.
                Bagels: You do not have any correct digits. 
            
            For Example: 
                If you guess 123 and the secret number is 413, then the
                clue you will receive could be either "Pico Fermi" or 
                "Fermi Pico".  
          """

    print(title_msg.center(79), "\n", instruction_msg)


def clr_scrn() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def get_secret_num() -> list[str]:
    nums: list[int] = [num for num in range(10)]

    random.shuffle(nums)
    try:
        sampled_nums: list[int] = random.sample(nums, NUM_DIGITS)
    except ValueError as e:
        logging.exception(f"\nA ValueError occurred: {e}")
        sys.exit()

    return [str(num) for num in sampled_nums]


def validate_guess(guess) -> bool:
    "Check if player's guess meets game requirements."
    try:
        int(guess)
        if len(set(guess)) == NUM_DIGITS:  # Check for length and unique digits
            return True
    except ValueError as e:  # Handle non-integer exceptions
        logging.exception(f"A ValueError has occurred: {e}")

    return False


def get_clue(guess, secret_num) -> str:
    clues: list[str] = []

    for i in range(NUM_DIGITS):
        if guess[i] == secret_num[i]:
            clues.append("Fermi")
        elif guess[i] in secret_num:
            clues.append("Pico")

    if len(clues) == 0:
        return "Bagels"
    else:
        return " ".join(clues)


def play_new_game() -> bool:
    response: str = input("Would you like to play again? (y/n)\n> ")

    return True if response.lower().startswith("y") else False


if __name__ == "__main__":
    main()
