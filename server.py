from bottle import route, run
from game import *

games = {}

@route('/')
def main():
    player = Player("Chuck", "1")
    player1 = Player("Steve", "1")
    deck = Util.newDeck()
    nid = "abe"
    games[nid] = Game([player, player1],["1"], deck, 1000)
    return nid
    
    
    return str(game.get_current_player())

@route('/<nid>')
def current(nid):
    return str(games[nid].get_current_player())

@route('/<nid>/<playername>/cards')
def cards(nid, playername):
    return str(games[nid].get_player_by_name(playername).cards)

@route('/<nid>/move/<move>')
def move(nid, move):
    game = games[nid]
    player = game.get_current_player()
    return str(Util.Valid_move(player, player.cards[int(move)]))
run(host='localhost', port=8080, reloader=True)

