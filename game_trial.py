from iv.game import TheGame
from iv.player import Player
from iv.helper import *

import json

game = TheGame(
    name = "firstGame"
)

game.add_player("goktug")
game.add_player("mete")
game.add_player("uraz")
game.add_bot("kopruculer")

serialized_game = game.serialize()
gg = game_decoder(serialized_game)
gg.set_coal_gain(199)
gg.set_factory_gain(300)

gg.start_game()

serialized_game = gg.serialize()
print(json.dumps(serialized_game, indent=2))

gg.go_to_next_player()
gg.go_to_next_player()
gg.go_to_next_player()
gg.go_to_next_player()
gg.go_to_next_player()
gg.go_to_next_player()
gg.go_to_next_player()
gg.go_to_next_player()
