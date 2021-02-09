from game import *


def main():
    player1 = Player("chuck", 1)
    player2 = Player("steve", 2)
    newdeck = Util.newDeck()
    g = Game([player1, player2], [1,2], newdeck, 1000)


    while True:
        currentPlayer = g.get_current_player()
        print(currentPlayer)
        print(currentPlayer.cards)
        uIn = input()
        opp = None
        while not Util.Valid_move(currentPlayer, currentPlayer.cards[int(uIn)], opp):
            print("invalid move")
            uIn = input()
            print(currentPlayer.cards[int(uIn)].category)
        if(currentPlayer.cards[int(uIn)].category == "Hazard"):
            print("choose an opponent")
            print(g.players)
            opp = int(input())
            currentPlayer.play(int(uIn), g.players[opp])
            g.advance_turn()
            continue
        currentPlayer.play(int(uIn))
        g.advance_turn()



if __name__ == "__main__":
    main()