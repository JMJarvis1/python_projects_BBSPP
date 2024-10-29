"""Blackjack.py -- John Michael Jarvis JMJarvis1@icloud.com

In this game, also known as 21, the player wagers a certain amount of money
on each hand and attempts to get the value of their hand as close to 21 as
possible without going over that value. There are three moves available to
the player on each hand. They can (H)it - take another card, (S)tand - end
their play for the hand, or (D)ouble down - increase the value of their wager.
However, the player can only (D)ouble down if it is their first play on that
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
import logging
import random
import time
import game_functions
from typing import Literal


# Constants
HEARTS: str = chr(9829)  # Character 9829 is '♥'
SPADES: str = chr(9824)  # Character 9824 is '♠'
CLUBS: str = chr(9827)  # Character 9824 is '♣'
DIAMONDS: str = chr(9830)  # Character 9830 is '♦'
MONEY: int = 5000


def main() -> None:
    current_hand, money = start_new_game()
    display_info()

    while True:  # Main game loop.
        player_move: str = ""
        # Create card deck
        deck: list[tuple[str, str]] = build_deck()

        # Get player wager
        wager: int = get_wager(money)

        # Deal hands
        player_hand: list = [deck.pop() for i in range(2)]
        dealer_hand: list = [deck.pop() for i in range(2)]

        # Display Hands
        print()
        describe_hands(current_hand, player_hand, dealer_hand)
        print()

        # Handle player actions
        print("----------\n" + "Your turn:\n" + "----------\n")
        while player_move not in ["S", "D"]:  # Player action loop
            player_move = get_player_move(player_hand, money, wager)

            match player_move:
                case "Q":  # Quits.
                    game_functions.exit_game()
                case "H" | "D":  # (H)its or (D)oubles down
                    # Handle player takes card
                    message = take_card(deck, player_hand, "player")
                    if player_move == "D":
                        wager = get_wager(money, wager)
                    print(" ".join(message))

            describe_hands(current_hand, player_hand, dealer_hand)

            player_busts = True if sum_hand_value(player_hand) > 21 else False

            if player_busts:  # Break loop
                break

        # Handle dealer actions
        if not player_busts:
            print("\n--------------\n" + "Dealer's turn:\n" + "--------------")
            while sum_hand_value(dealer_hand) < 17:  # Dealer loop
                message = take_card(deck, dealer_hand, "dealer")
                print(" ".join(message))
                describe_hands(current_hand, player_hand, dealer_hand)
                time.sleep(2)  # Delay between moves

        # Decide winner
        describe_hands(current_hand, player_hand, dealer_hand, hide_dealer=False)
        outcome: str = get_outcome(player_hand, dealer_hand)
        money = payout(outcome, money, wager)

        print(f"\nYou {outcome}", end="")  # 'win', 'lose', or 'tie'
        print(f" {wager}!\n") if outcome != "tie" else print("!\n")

        if money <= 0:  # Player is broke
            print("You're broke! It's a good thing this wasn't real money!\n")
            print("Game over...\n")
            new_game: bool = game_functions.play_again()

            if new_game:
                review_rules: str = " "
                current_hand, money = start_new_game()
                while review_rules[0] not in ["Y", "N"]:
                    review_rules = (
                        input("Do you want to see the rules again? (Y/N)\n> ")
                        .strip()
                        .upper()
                    )
                display_info() if review_rules == "Y" else display_info(rules=False)

                continue  # Restart game loop with money reset to start value
            else:
                game_functions.exit_game()
        else:
            continue  # Restart loop with current state intact

        while input("Press Enter to continue...") != "":
            current_hand += 1
            continue


def start_new_game() -> tuple[int, int]:
    """
    Initialize a new game with money set its starting value.
    """
    game_functions.clear_scrn()
    current_hand: int = 1
    money = MONEY

    return current_hand, money


def display_info(title=True, rules=True) -> None:
    """
    Load the Title and Rules texts from a json file and display them on the screen.

    :param title: Include title text, defaults to True
    :type intro: bool, optional
    :param rules: Include rules text, defaults to True
    :type rules: bool, optional
    """
    game_functions.clear_scrn()

    # Load program text from JSON file.
    sys.path.append(os.getcwd() + "../")  # Make sure file is in path
    try:
        game_txt: dict = load_json_txt(
            path="/workspaces/python_games/games/text.json", key="blackjack.py"
        )
    except FileNotFoundError:
        logging.error(" A fatal error occurred when attempting to load 'text.json.'")
        game_functions.exit_game()

    # Display Introduction
    if title:
        title_txt: list = game_txt["title"]
        game_functions.display_message(title_txt, msg_just="center")

    # Display rules
    if rules:
        rules_intro: list = game_txt["rules"]
        game_functions.display_message(rules_intro)
    print()


def build_deck() -> list[tuple[str, str]]:
    """
    Create and return a shuffled deck of cards.

    :return: A shuffled deck of cards
    :rtype: list[tuple[str, str]]
    """
    # deck: list[tuple[str, str]] = []
    ranks: list = [str(num) for num in range(2, 11)] + ["J", "Q", "K", "A"]
    suits: list[str] = [HEARTS, SPADES, CLUBS, DIAMONDS]

    deck: list[tuple[str, str]] = [(rank, suit) for rank in ranks for suit in suits]

    random.shuffle(deck)
    return deck


def get_wager(money: int, wager: int = 0) -> int:
    """
    Receive and validate player's wager.

    :param money: Current money held by player
    :type money: int
    :param wager: Amount already wagered, defaults to 0
    :type wager: int, optional
    :return: The new or updated value for the wager
    :rtype: int
    """
    while True:
        amount: int = 0
        game_functions.display_message(
            f"You currently have ${money-wager} available. How much would you like to wager?"
        )

        try:
            amount += int(input("> $"))
        except ValueError:
            print("\nPlease only enter a number value.\n")
            continue
        if money < amount:
            print(f"\nError: You dont have ${amount:,} to bet! Try again...\n")
            continue
        else:
            wager += amount
        return wager


def describe_hands(
    curr_hand: int,
    plr_hand: list,
    dlr_hand: list,
    hide_dealer: bool = True,
) -> None:
    """
    Displays the text and art associated with the current state of play.

    :param money: Current amount of money available to the player.
    :type money: int
    :param wager: Current amount wagered by player.
    :type wager: int
    :param plr_hand: The player's hand.
    :type plr_hand: list
    :param dlr_hand: The dealer's hand.
    :type dlr_hand: list
    :param hide_dealer: Hide first card if 'True', defaults to True
    :type hide_dealer: bool, optional
    """
    # Calculate value of each hand
    dealer_value: int = sum_hand_value(dlr_hand)
    player_value: int = sum_hand_value(plr_hand)

    print(f"Hand #{curr_hand}\n")
    # Dealer
    if hide_dealer:
        print("DEALER: ??")  # Hide dealer's score
    else:
        print(f"DEALER: {dealer_value}")
        print("Dealer busts!") if dealer_value > 21 else None
    draw_hand(dlr_hand, hide_dealer)  # Draw hand

    # Player
    print(f"PLAYER: {player_value}")
    print("Player busts!") if player_value > 21 else None
    draw_hand(plr_hand, hide_dealer=False)  # Draw hand


def load_json_txt(path: str, key: str) -> dict:
    """
    Loads the game's text from a json file.

    :param path: Path to file
    :type path: str
    :param key: The name of the game 'blackjack.py' we want the text for.
    :type key: str
    :return: The text from the file specific to this game.
    :rtype: dict
    """
    with open(file=path, mode="r", encoding="UTF-8") as read_file:
        all_txt = json.load(read_file)
        selected_txt: dict = all_txt.get(key)

    return selected_txt


def sum_hand_value(hand: list[tuple[str, str]]) -> int:
    """
    Calculates the current value of all card currently held in accordance with the rules
    of blackjack.

    :param hand: The hand to be evaluated
    :type hand: list[tuple[str,str]]
    :return: The sum value of all cards
    :rtype: int
    """
    value: int = 0
    num_aces: int = 0

    for card in hand:
        if card[0] in ["K", "Q", "J"]:
            value += 10
        elif card[0] == "A":  # Add 1 for each Ace
            value += 1
            num_aces += 1
        else:
            value += int(card[0])

    for i in range(1, num_aces + 1):
        while value + 10 <= 21:
            value += 10  # Add an additional 10 for each ace if possible

    return value


def draw_hand(hand: list[tuple[str, str]], hide_dealer: bool) -> None:
    """
    Draws a visual represntation of the cards in a hand.

    :param hand: The hand being drawn as art.
    :type hand: list[tuple[str, str]]
    :param hide_dealer: Hides the first card in the hand.
    :type hide_dealer: bool
    """
    rows = ["", "", "", "", ""]

    for card in hand:
        rows[0] += " ___  "  # Top edge of card
        if (hide_dealer) & (card is hand[0]):  # Hide first card
            rows[1] += "|## | "
            rows[2] += "|###| "
            rows[3] += "|_##| "
        else:
            rows[1] += f"|{card[0]:<2} | "  # Rank to 2 digits
            rows[2] += f"| {card[1]} | "  # Suit
            rows[3] += f"|_{card[0]:_>2}| "  # Rank to 2 digits and bottom edge

    [print(row) for row in rows]  # Draws card to screen


def get_player_move(player_hand: list, money, wager) -> str:
    """
    Gets player choice of move from the folowing options:
    (H)it, (S)tand, (D)ouble down, (Q)uit.

    :param player_hand: Current cards held by player
    :type player_hand: list
    :return: Player's chosen move.
    :rtype: str
    """
    prompts: list = ["(H)it", "(S)tand"]
    valid_moves: list = ["H", "S", "Q"]
    player_move: str = ""

    if len(player_hand) == 2:
        prompts.append("(D)ouble down")
        valid_moves.append("D")

    prompts.append(f"or (Q) to quit. Money: ${money-wager} Wager: ${wager}\n> ")

    prompt: str = ", ".join(prompts)

    while player_move not in valid_moves:
        player_move = input(prompt)[0].upper()

    return player_move


def take_card(
    deck: list, hand: list[tuple[str, str]], owner: Literal["player", "dealer"]
) -> list:
    """
    Draw a card from the deck and add it to the hand provide, print details regarding the card drawn, and return updated hand.

    :param deck: The deck of cards being drawn from.
    :type deck: list
    :param hand: The hand (player or dealer) receiving the new card.
    :type hand: list[tuple[str, str]]
    :param owner: Ownership of hand.
    :type owner: Literal["player", "dealer"]
    :return: Updated hand.
    :rtype: list
    """
    hand.append(deck.pop())
    rank, suit = hand[-1]

    message = ["", f"a {rank} of {suit} from the deck.\n"]

    if owner == "player":
        message[0] = "\nYou take"
    elif owner == "dealer":
        message[0] = "\nThe dealer takes"

    return message


def get_outcome(plr_hand: list, dlr_hand: list) -> str:
    """
    Determine if player wins, loses, ot ties.

    :param plr_hand: Player's cards at end of hand
    :type plr_hand: list
    :param dlr_hand: Dealers's cards at end of hand
    :type dlr_hand: list
    :return: Player rusult. ('win', 'lose', 'tie')
    :rtype: str
    """
    dealer_value: int = sum_hand_value(dlr_hand)
    player_value: int = sum_hand_value(plr_hand)

    if not player_value > 21:
        if player_value > dealer_value or dealer_value > 21:
            return "win"
        elif player_value < dealer_value:
            return "lose"
        elif player_value == dealer_value:
            return "tie"
    return "lose"


def payout(outcome: str, money: int, wager: int) -> int:
    """
    Updates player money based upon outcome of most recent hand.

    :param outcome: Whether player won, lost, or tied.
    :type outcome: str
    :param money: Amount of money held by player.
    :type money: int
    :param wager: Amount wagered by player during hand.
    :type wager: int
    :return: Updated value for money. (money +/- wager)
    :rtype: int
    """
    match outcome:
        case "win":
            money += wager
        case "lose":
            money -= wager
    return money


if __name__ == "__main__":
    main()
