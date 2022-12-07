from random import shuffle, choice, randint
import os

suites = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
deck = []
players = {}
class Player:
    def __init__(self, name, score, hand, bet, chips,  state):
        self.name = name
        self.score = score
        self.hand = hand
        self.bet = bet
        self.chips = chips
        self.state = state

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
                players[f'player{i + 1 }'] = Player(name, 0, [], 0, 0, True)
                break 
    players['dealer'] = Player("Dealer", 0, [], None, None, True)
    cash = round(randint(500, 1000), -1)
    for player in players:
        players[player].chips = cash
    print(f"Each player starts with ${cash}.")
    input("Press enter to start!")
    clear_scr()
    shuffle_deck()

def bet(player):
    wager = input("How much do want to bet?>")
    players[player].chips -= wager
    players[player].bet += wager

def deal():
    for i in range(2):
        for player in players:
            card = choice(deck)
            players[player].hand.append(card)
            deck.remove(card)
        for player in players:
            display_hand(player, True)

def display_hand(player, hidden):
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

def end_count(player, dealer_score):
    score = chk_score(player)
    result = 'Null'
    if score < dealer_score:
        result = 'lose'
    elif score > dealer_score:
        result = 'win'
    elif score == dealer_score:
        result = 'tie'

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
    
def shuffle_deck():
    for i in suites:
        for j in range(1, 13):
            card = (j, i)
            deck.append(card)
    shuffle(deck)

init()
deal()

for player in players:
    bet(player)

for player in players:
    if players[player].state == False : continue
    if players[player].name == 'Dealer': continue
    while True:
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
    winner = []
    for player in players:
        if players[player].state == True:
            winner.append(players[player].name)
    print("Winners:")
    for i in winner:
        print(i, end="\t")
for player in players:
    if players[player].state == False: continue
    end_count(player, d_score)