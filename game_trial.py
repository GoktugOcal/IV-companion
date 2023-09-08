from iv.game import TheGame
from iv.player import Player
from iv.market import Market, MarketItem
from iv.helper import *

import pandas as pd
import json

game = TheGame(
    name = "firstGame"
)

game.add_player("goktug")
game.add_player("mete")
game.add_player("uraz")
game.add_bot("kopruculer")

game.players[1].money = 100000
game.players[2].money = 100000

game.show_players()

serialized_game = game.serialize()
gg = game_decoder(serialized_game)

# market_json = json.loads(pd.read_csv(game.market_file, delimiter=";").to_json(orient="records", force_ascii=False))

# market = Market(market_json)

# game.buy(game.players[1], 5)
# game.buy(game.players[1], 17)
# game.buy(game.players[1], 18)
# game.buy(game.players[1], 19)

ids = [4]
item_id = list(game.market.items.values())[ids[0]].id
game.buy(game.players[1], item_id)

# game.buy(game.players[2], 19)

game.show_players()


serialized_game = game.serialize()
print(serialized_game)
gg = game_decoder(serialized_game)


# game.market.items[5].affect(game.players[1])
# game.market.items[18].affect(game.players[1])