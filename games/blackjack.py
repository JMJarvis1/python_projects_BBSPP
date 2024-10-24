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

sys.path.append(os.getcwd() + "/..")

from common_functions import clear_scrn


def main():
    money = 5000

    clear_scrn()

    while True:  # Main game loop.
        # TODO Display Introduction

        # TODO Create card deck

        # TODO Get player bet

        # TODO Deal hands

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


if __name__ == "__main__":
    main()
