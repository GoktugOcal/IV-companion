from iv.game import TheGame
from iv.player import Player
from iv.helper import *

game = TheGame(
    name = "firstGame"
)

game.add_player("goktug")
game.add_player("mete")
game.add_bot("köprücüler")

serialized_game = game.serialize()
print(serialized_game)

print(game_decoder(serialized_game))