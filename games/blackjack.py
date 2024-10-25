"""Blackjack.py -- John Michael Jarvis JMJarvis1@icloud.com

In this game, also known as 21, the player wagers a certain amount of money
on each hand and attempts to get the value of their hand as close to 21 as
possible without going over that value. There are three moves available to
the player on each hand. They can (H)it - take another card, (S)tand - end
their play for the hand, or (D)ouble down - double the value of their wager.
However, the play can only (D)ouble down if it is their first play on that
hand and they must take at least one more card before standing. The player is
awarded the value of their wager if they win, and lose that value if they
themselves lose. The wagered money is returned to the player in the event of
a tie.

The possible outcomes are of each hand:

    Player Hand   Dealer Hand         Result
    -----------   -----------   --------------------
        > 21          Any       Player Loses (Busts)
        < 21       < Player     Player Wins
        < 21         > 21       Dealer Busts
         Tie         Tie        Tie

    Other rules:
        1. Facecards (K, Q, J) are each worth 10.
        2. Aces are worth either 1 or 11.
        3. All other cards are worth their face value.
        4. This version of the game does not allow for splitting,
           surrendering, or buying insurance.
        5. The dealer stands at 17 or higher.

More information can be found at: https://en.wikipedia.org/wiki/blackjack

"""

import sys
import os
import json
import random


sys.path.append(os.getcwd() + "/..")

from common_functions import clear_scrn, display_message

# Constants
HEARTS = chr(9829)  # Character 9829 is '♥'
SPADES = chr(9824)  # Character 9824 is '♠'
CLUBS = chr(9827)  # Character 9824 is '♣'
DIAMONDS = chr(9830)  # Character 9830 is '♦'
BACKSIDE = "backside"


def main() -> None:
    money: int = 5000

    clear_scrn()

    # Load program text from JSON file.
    try:
        game_txt: dict = load_json_txt(path="text.json", key="blackjack.py")
    except FileNotFoundError:  # For lauch.json debugging
        game_txt = load_json_txt(path="games/text.json", key="blackjack.py")

    while True:  # Main game loop.
        # Display Introduction
        title_txt: list = game_txt["title"]
        display_message(title_txt, msg_just="center")

        rules_intro: list = game_txt["rules"]
        display_message(rules_intro)
        print()

        # Create card deck
        deck: list[tuple[str, str]] = get_deck()

        # Get player wager
        while True:
            print(f"MONEY: {money}")
            print("How much would you like to wager?")
            try:
                wager: int = int(input("> "))
            except ValueError:
                print("\nPlease only enter a number value.\n")
                continue
            if wager <= money:
                break
        # Deal hands
        player_hand: list = [deck.pop() for i in range(2)]
        dealer_hand: list = [deck.pop() for i in range(2)]
        print(player_hand, dealer_hand)

        # TODO Display Hands

        while True:
            # TODO get player moves

            # TODO Update player_hand display
            break

        while True:
            # TODO get dealer moves

            # TODO Update dealer_hand display
            break

        # TODO Decide winner of hand

        # TODO Adjust player money

        # TODO Determine if palyer can or wants to continue.

        break

    sys.exit()


def load_json_txt(path: str, key: str) -> dict:
    with open(file=path, mode="r", encoding="UTF-8") as read_file:
        all_txt = json.load(read_file)
        selected_txt: dict = all_txt.get(key)

    return selected_txt


def get_deck() -> list[tuple[str, str]]:
    deck: list[tuple[str, str]] = []

    for rank in range(2, 11):
        for suit in [HEARTS, SPADES, CLUBS, DIAMONDS]:
            card = (str(rank), suit)
            deck.append(card)

    for face in ["A", "K", "Q", "J"]:
        for suit in [HEARTS, SPADES, CLUBS, DIAMONDS]:
            card = (face, suit)
            deck.append(card)
    random.shuffle(deck)
    return deck


if __name__ == "__main__":
    main()
