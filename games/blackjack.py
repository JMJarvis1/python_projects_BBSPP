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

import json
import random
import time
from typing import Literal
import game_functions

# Constants
HEARTS: str = chr(9829)  # Character 9829 is '♥'
SPADES: str = chr(9824)  # Character 9824 is '♠'
CLUBS: str = chr(9827)  # Character 9824 is '♣'
DIAMONDS: str = chr(9830)  # Character 9830 is '♦'
MONEY: int = 5000


def main() -> None:
    money: int = MONEY

    start_game()

    while True:  # Main game loop.
        player_move: str = ""
        # Create card deck
        deck: list[tuple[str, str]] = get_deck()

        # Get player wager
        wager: int = get_wager(money)

        # Deal hands
        player_hand: list = [deck.pop() for i in range(2)]
        dealer_hand: list = [deck.pop() for i in range(2)]

        # Display Hands
        print()
        display_hands(money, wager, player_hand, dealer_hand)
        print()

        # Handle player actions
        print("----------\n" + "Your turn:\n" + "----------\n")
        while player_move not in ["S", "D"]:
            player_move = get_player_move(player_hand)

            match player_move:
                case "Q":
                    game_functions.exit_game()
                case "H" | "D":
                    player_value, message = take_card(deck, player_hand, "player")
                    if player_move == "D":
                        wager = get_wager(money, wager)
                    print(" ".join(message))

            display_hands(money, wager, player_hand, dealer_hand)

            if player_value > 21:
                break

        # Handle dealer actions
        if player_value < 21:
            print("\n--------------\n" + "Dealer's turn:\n" + "--------------")
            while get_hand_value(dealer_hand) < 17:  # Calculate hand value
                dealer_value, message = take_card(deck, dealer_hand, "dealer")
                print(" ".join(message))
                display_hands(money, wager, player_hand, dealer_hand)
                time.sleep(2)

        # Decide winner of hand
        display_hands(money, wager, player_hand, dealer_hand, hide_dealer=False)
        outcome: str = get_outcome(player_hand, dealer_hand)
        money = payout(outcome, money, wager)

        print(f"\nYou {outcome}", end="")
        print(f" {wager}!\n") if outcome != "tie" else print("!\n")

        if money <= 0:
            print("You're broke! It's a good thing this wasn't real money!\n")
            print("Game over...\n")
            new_game: bool = game_functions.play_again()

            if new_game:
                money = MONEY
                start_game()
                continue
            else:
                game_functions.exit_game()
        else:
            continue

        while input("Press Enter to continue...") != "":
            continue


def start_game() -> None:
    game_functions.clear_scrn()

    # Load program text from JSON file.
    try:
        game_txt: dict = load_json_txt(path="text.json", key="blackjack.py")
    except FileNotFoundError:  # For lauch.json debugging
        game_txt = load_json_txt(path="games/text.json", key="blackjack.py")

    # Display Introduction
    title_txt: list = game_txt["title"]
    game_functions.display_message(title_txt, msg_just="center")

    # Display rules
    rules_intro: list = game_txt["rules"]
    game_functions.display_message(rules_intro)
    print()


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
        print(f"MONEY: ${money-wager}")
        print("How much would you like to wager?")
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


def get_deck() -> list[tuple[str, str]]:
    # deck: list[tuple[str, str]] = []
    ranks: list = [str(num) for num in range(2, 11)] + ["J", "Q", "K", "A"]
    suits: list[str] = [HEARTS, SPADES, CLUBS, DIAMONDS]

    deck: list[tuple[str, str]] = [(rank, suit) for rank in ranks for suit in suits]

    random.shuffle(deck)
    return deck


def get_hand_value(hand: list[tuple]) -> int:
    value: int = 0
    num_aces: int = 0

    for card in hand:
        if card[0] in ["K", "Q", "J"]:
            value += 10
        elif card[0] == "A":
            value += 1
            num_aces += 1
        else:
            value += int(card[0])

    for i in range(1, num_aces + 1):
        while value + 10 <= 21:
            value += 10

    return value


def display_hands(
    money: int, wager: int, plr_hand: list, dlr_hand: list, hide_dealer: bool = True
) -> None:
    dealer_value: int = get_hand_value(dlr_hand)
    player_value: int = get_hand_value(plr_hand)

    # Dealer
    if hide_dealer:
        print("DEALER: ??")
    else:
        print(f"DEALER: {dealer_value}")
    print("Dealer busts!") if dealer_value > 21 else None
    draw_hand(dlr_hand, hide_dealer)

    # Player
    print(f"PLAYER: {player_value}")
    print("Player busts!") if player_value > 21 else None
    draw_hand(plr_hand, hide_dealer=False)
    print(f"Money: ${money-wager} Wager: ${wager}")


def draw_hand(hand: list[tuple[str, str]], hide_dealer: bool) -> None:
    rows = ["", "", "", "", ""]

    for card in hand:
        rows[0] += " ___  "
        if (hide_dealer) & (card is hand[0]):
            rows[1] += "|## | "
            rows[2] += "|###| "
            rows[3] += "|_##| "
        else:
            rows[1] += f"|{card[0]:<2} | "
            rows[2] += f"| {card[1]} | "
            rows[3] += f"|_{card[0]:_>2}| "

    [print(row) for row in rows]


def get_player_move(player_hand: list) -> str:
    prompts: list = ["(H)it", "(S)tand"]
    valid_moves: list = ["H", "S", "Q"]
    player_move: str = ""

    if len(player_hand) == 2:
        prompts.append("(D)ouble down")
        valid_moves.append("D")

    prompts.append("or (Q) to quit.\n> ")

    prompt: str = ", ".join(prompts)

    while player_move not in valid_moves:
        player_move = input(prompt).upper()

    return player_move


def take_card(deck: list, hand: list, owner: Literal["player", "dealer"]) -> tuple:
    hand.append(deck.pop())
    rank, suit = hand[-1]

    message = ["", f"a {rank} of {suit} from the deck.\n"]

    if owner == "player":
        message[0] = "\nYou take"
    elif owner == "dealer":
        message[0] = "\nThe dealer takes"

    return get_hand_value(hand), message


def get_outcome(plr_hand: list, dlr_hand: list) -> str:
    dealer_value: int = get_hand_value(dlr_hand)
    player_value: int = get_hand_value(plr_hand)
    # Player wins hand
    if (player_value > dealer_value) | dealer_value > 21:
        return "win"
    # Player loses hand
    elif player_value > 21 | (player_value < dealer_value):
        return "lose"
    # Hand is tied
    else:
        return "tie"


def payout(outcome: str, money: int, wager: int) -> int:
    match outcome:
        case "win":
            money += wager
        case "lose":
            money -= wager
    return money


if __name__ == "__main__":
    main()
