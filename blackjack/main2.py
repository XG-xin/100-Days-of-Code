import random
cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
user_cards = []
computer_cards = []

def deal_card():
    card = random.choice(cards)
    return card

def calculate_score(cards):
    if len(cards) == 2:
        if 1 in cards and 11 in cards:
            return (0)
        else: 
            return (sum(cards))
    else:
        if 11 in cards:
            if sum(cards) > 21:
                cards.remove(11)
                cards.append(1)
                return (sum(cards))
        else:        
            return (sum(cards))


def compare(user_score, computer_score):
    if user_score == computer_score:
        print("It's a draw.")
    elif computer_score == 0:
        print("You loss.")
    elif user_score == 0:
        print("You win.")
    elif user_score > 21:
        print("You loss.")
    elif computer_score > 21:
        print("You win.")
    else:
        if user_score > computer_score:
            print("You win.")
        else:
            print("You loss.")
        

user_cards = [deal_card(), deal_card()]
computer_cards = [deal_card(), deal_card()]
print(f"user card {user_cards}")
print(f"computer card {computer_cards}")
if calculate_score(user_cards) > 21:
    game_end = True
    compare(calculate_score(user_cards), calculate_score(computer_cards))
elif calculate_score(user_cards) == 0:
    game_end = True
    compare(calculate_score(user_cards), calculate_score(computer_cards))
elif calculate_score(computer_cards) == 0:
    game_end = True
    compare(calculate_score(user_cards), calculate_score(computer_cards))
else:
    continue_game = input("Type 'y' to get another card, type 'n' to pass: ")
    while continue_game == 'y':
        user_cards.append(deal_card())
        calculate_score(user_cards)
        print(f"user card {user_cards}")
        print(calculate_score(user_cards))
        if calculate_score(user_cards) > 21:
            print("You loss.")
            continue_game == 'n'
        else:
            continue_game = input("Type 'y' to get another card, type 'n' to pass: ")
    if continue_game == 'n':
        game_end = True
    while calculate_score(computer_cards) < 17:
        computer_cards.append(deal_card())
        calculate_score(computer_cards)

restart_game = input("Do you want to play game of Blckjack? Type 'y' or 'n': ")