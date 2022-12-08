from random import shuffle, choice, randint
from sys import exit
import webbrowser
import os

suites = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
deck = []
players = {}
class Player:
    def __init__(self, name, score, hand, bet, chips, state, result):
        self.name = name
        self.score = score
        self.hand = hand
        self.bet = bet
        self.chips = chips
        self.state = state
        self.result = result

def main():
    deal()
    for player in players:
        if players[player].name == 'Dealer': continue
        bet(player)
    clear_scr()
    for player in players:
        display_hand(player, True)
    for player in players:
        if players[player].state == False : continue
        if players[player].name == 'Dealer': continue
        while players[player].state:
            choice = input(players[player].name + "[H]it/[S]tand>")
            if choice.lower() == 's':
                break
            elif choice.lower() == 'h':
                hit(player)
                continue
            else:
                print("Not a valid option.")
                continue
    reveal('dealer')
    while True:
        if chk_score('dealer') < 17:
            hit('dealer')
        else:
            break
    d_score = chk_score('dealer')
    if d_score > 21:
        print("Dealer bust!")
        players['dealer'].state = False
    for player in players:
        if players[player].state == False and players[player].name != 'Dealer': continue
        end_count(player, d_score)

    for player in players:
        if players[player].name == 'Dealer': continue
        if players[player].result == 'lose' or not players[player].state: 
            print(players[player].name + " lost their bet.")
            players['dealer'].chips += players[player].bet
            players[player].bet = 0
            continue
        if players[player].result == 'win':
            prize = players[player].bet * 2
            print(f"{players[player].name} beat the dealer. They won ${prize}.")
            players[player].bet = 0
            players[player].chips += prize
            continue
        if players[player].result == 'tie':
            players[player].chips += players[player].bet
            players[player].bet = 0
            print(f"It's a tie! {players[player].name} got their bet back. (${players[player].bet})")
            continue
    input("Press enter to continue...")
    for player in players:
        summary(players)
    left = []
    for player in players:
        if players[player].name == 'Dealer':
            continue
        while True:
            ng = input(f"{players[player].name}, would you like to go again? [N]ew round/[L]eave/E[X]it/[C]redits\n>")
            if ng.upper() == 'N':
                break
            elif ng.upper() == 'L':
                left.append(player)
                break
            elif ng.upper() == 'X':
                exit()
            elif ng.upper() == 'C':
                webbrowser.open("https://github.com/Krizsan0596/PyJack", 2, True)
                continue
            else:
                print("Invalid input. Try again.")
    for item in left:
        del players[item]
    if len(players) != 0:
        main()

def clear_scr():
    os.system('cls' if os.name == 'nt' else 'clear')

def init():
    p_count = int(input("How many players?\n>"))
    for i in range(p_count):
        while True:
                name = input(f"Player {i + 1} name> ")
                if name == 'Dealer':
                    print("You are not the dealer.")
                    continue
                players[f'player{i + 1 }'] = Player(name, 0, [], 0, 0, True, None)
                break 
    players['dealer'] = Player("Dealer", 0, [], None, 0, True, None)
    cash = round(randint(500, 1000), -1)
    for player in players:
        players[player].chips = cash
    print(f"Each player starts with ${cash}.")
    input("Press enter to start!")
    clear_scr()
    shuffle_deck()
    main()

def bet(player):
    wager = input(f"{players[player].name}, how much do want to bet? (Num/[A]ll in)>")
    wager = players[player].chips if wager.lower() == 'a' else int(wager)
    players[player].chips -= wager
    players[player].bet += wager

def deal():
    for i in range(2):
        for player in players:
            card = choice(deck)
            players[player].hand.append(card)
            deck.remove(card)
    for player in players:
        if chk_score(player) == 21:
            if players[player].name == 'Dealer':
                for p in players:
                    if chk_score(p) != 21:
                        players[p].result = 'lose'
                    elif chk_score(p) == 21:
                        players[p].result = 'tie'
            else:
                if players['dealer'].score != 21:
                    prize = players[player].bet *1.5
                    print(players[player].name + f" hit a blackjack! They won ${prize}.")
                    players[player].chips += prize
                    players[player].bet = 0
                    players[player].result = 'blackjack'
                    players[player].state = False
    for player in players:
        display_hand(player, True)

def display_hand(player, hidden:bool):
    hand = []
    if player != 'dealer' or not hidden:
        for i in players[player].hand:
            hand.append(str('Ace' if i[0] == 1 else ('King' if i[0] == 13 else ('Queen' if i[0] == 12 else ('Jack' if i[0] == 11 else i[0])))) + " of " + i[1])
    else:
        d_hand = players[player].hand[:-1]
        for i in d_hand:
            hand.append(str('Ace' if i[0] == 1 else ('King' if i[0] == 13 else ('Queen' if i[0] == 12 else ('Jack' if i[0] == 11 else i[0])))) + " of " + i[1])
            hand.append("??? of ???")
    print((str(players[player].name) + ' - ' +  ' and '.join(hand)) + (("  =  " + str(chk_score(player))) if players[player].name != 'Dealer' or not hidden else "  =  " + str(sum([players[player].hand[i][0] for i in range(len(players[player].hand) - 1)]))))           
        
def hit(player):
    card = choice(deck)
    deck.remove(card)
    players[player].hand.append(card)
    chk_score(player)
    display_hand(player, True)

def reveal(dealer):
    display_hand(dealer, False)

def end_count(player, dealer_score:int):
    score = chk_score(player)
    result = 'Null'
    if score < dealer_score:
        result = 'lose'
    elif score > dealer_score:
        result = 'win'
    elif score == dealer_score:
        result = 'tie'
    players[player].result = result

def chk_score(player):
    score = 0
    hand = []
    for i in players[player].hand:
        hand.append(10 if i[0] > 10 else (i[0] if i[0] != 1 else 11))
    score = sum(hand)
    players[player].score = score
    if score > 21:
        try:
            hand.remove(11)
            hand.append(1)
        except ValueError:
            players[player].status = False
            if players[player].name != 'Dealer': 
                print(f"{players[player].name} busted!")
    return score

def summary(players):
    clear_scr()
    for player in players:
        if players[player].name == 'Dealer': continue
        if not players[player].state and players[player].result != 'blackjack':
            print(f"{players[player].name} busted! They have ${players[player].chips} left.")
        elif players[player].result == 'tie':
            print(f"{players[player].name} tied with the dealer and won nothing. They have ${players[player].chips} left.")
        elif players[player].result == 'win':
            print(f"{players[player].name} beat the dealer. They now have ${players[player].chips}.")
        elif players[player].result == 'blackjack':
            print(f"{players[player].name} got a natural and now has ${players[player].chips}")

def shuffle_deck():
    for i in suites:
        for j in range(1, 13):
            card = (j, i)
            deck.append(card)
    shuffle(deck)

    
init()