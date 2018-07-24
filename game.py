import xml.etree.ElementTree as ET
from random import shuffle

REMEDIES = {"Accident":"Repairs", "Empty_tank":"Gas", "Flat":"Spare"}
SAFETIES = {"Accident":"Ace", "Empty_tank":"ExtraTank", "Flat":"PunctureProof", "RightOfWay":"Stop"}

class Card:
    def __init__(self, name, category, subtype, value):
        self.name = name
        self.category = category
        self.subtype = subtype
        self.value = value

    def __repr__(self):
        return("{0}, Category={1}, Subtype={2}, Value={3} \n".format(self.name, self.category, self.subtype, self.value))

class Player:
    def __init__(self, name, team):
        self.name = name
        self.team = team
        self.round_score = 0
        self.milestones = []
        self.total_score = 0
        self.cards = []
        self.limit = False
        self.go_pile = None
        self.safeties = []
        self.safety_cards = []

    def __repr__(self):
        return("name: {0}, Score: {1}, {2}, Limit = {3}".format(self.name, self.round_score, self.go_pile, self.limit))

        
    def draw(self,deck):
        self.cards.append(deck.pop())

    def play(self, card_index, opponent=None):
        card = self.cards[card_index]
        ret = 0
        if card.category == "Hazard":
            if opponent == None:
                print("Choose an Opponent ")
                ret = opponent.add_to_go_pile(card)
            else:
                ret = opponent.add_to_go_pile(card)
        elif card.category == "Remedy":
            ret = self.add_to_go_pile(card)

        elif card.category == "Safety":
            ret = self.add_safety(card)

        elif card.category == "Distance":
            ret = self.add_milestone(card)
            
        if ret == 1 :
            self.cards.remove(card)

    def add_to_go_pile(self,card):
        if card.category == "Hazard":
            if card.subtype == "Limit":
                self.add_to_limit(card)
                return 1
            if self.go_pile.subtype == "Go":
                self.go_pile = card
                return 1
                
            else:
                return 0
            
        elif card.category == "Remedy":
            if self.go_pile == None and card.subtype == "Go":
                self.go_pile = card
            if self.go_pile.category == "Hazard":
                if REMEDIES[self.go_pile.subtype] == card.subtype:
                    self.go_pile = card
            if self.go_pile.category == "Remedy":
                if card.subtype == "Go":
                    self.go_pile = card
        return 1
                
            

    def add_to_limit(self, card):
        if self.limit == False and card.subtype == "Limit":
            self.limit = True
            return 1
        elif self.limit and card.subtype == "LimitEnd":
            self.limit = False
            return 1
        else:
            return 0

    def add_safety(self, card):
       self.safeties.append(card.name)
       self.safety_cards.append(card)
       return 1
       
    def add_milestone(self, card):
        if self.go_pile != None and card.category == "Distance":
            if self.limit and (not "RightOfWay" in self.safeties):
                if card.value > 50:
                    return 0
                else:
                    self.milestones.append(card)
                    self.round_score += card.value
                    return 1
            else:
                self.milestones.append(card)
                self.round_score += card.value
                return 1
        elif "RightOfWay" in self.safeties and card.category == "Distance":
            self.milestones.append(card)
            self.round_score += card.value
            return 1
        return 0
    

class Game:
    def __init__(self, players, teams, deck):
        self.players = players
        self.teams = teams
        self.deck = deck


class Util:
    def newDeck():
        tree = ET.parse("cards.xml")
        cards = []
        deck = tree.getroot()

        for category in deck:
            for subtype in category:
                value = int(subtype.attrib["value"])
                name = subtype.attrib["name"]
                for i in range(1,int(subtype.attrib["count"])):
                    newCard = Card(name, category.tag, subtype.tag, value)
                    cards.append(newCard)
        return cards

    def Valid_move(player1, card, opponent=None):
        if opponent != None:
            if card.category != "Hazard":
                return False
            else:
                if opponent.go_pile.subtype != "Go":
                    return False
                if SAFTIES[card.subtype] in opponent.safeties:
                    return False
        else:
            if card.category == "Remedy":
                if player1.go_pile == None:
                    if card.subtype == "Go":
                        return True
                    else:
                        return False
                if REMEDIES[player1.go_pile.subtype] == card.subtype:
                    return True
                else:
                    return False
                if card.subtype == "LimitEnd":
                    if player1.limit:
                        return True
                    else:
                        return False
            elif card.category == "Distance":
                if player1.go_pile == None:
                    return False
                if player1.go_pile.subtype != "Go":
                    return False
                if player1.limit:
                    if card.value > 50:
                        return False
                    else:
                        return True
                    
            else:
                return True
        return True
                
                    
                




def main():
    num_players = input("Number of Players? ")
    players = []
    for i in range(0,int(num_players)):
        name = input("Name? ")
        team = input("Team? ")
        players.append(Player(name, team))
    print(players)

    deck = Util.newDeck()
    shuffle(deck)
    #deal out
    for i in players:
        for y in range(6):
            i.cards.append(deck.pop())
        #print(i.cards)

    while True:
        for player in players:
            print(player)
            player.draw(deck)
            print(player.cards)
            line = input("?")
            line = list(line)
            if line[0] == "p":
                if player.cards[int(line[1])].category == "Hazard":
                    opponent = players[int(input("Which Opponent?"))]
                    if Util.Valid_move(player, player.cards[int(line[1])], opponent):
                        player.play(int(line[1]), opponent)
                    else:
                        print("INVALID MOVE")
                else:
                    if Util.Valid_move(player, player.cards[int(line[1])]):
                        player.play(int(line[1]))
                    else:
                        print("INVALID MOVE")
            elif line[0] == "d":
                player.cards.remove(player.cards[int(line[1])])
        
                
                
if __name__ == "__main__":
    main()
        
