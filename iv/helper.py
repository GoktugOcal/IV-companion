from iv.game import TheGame
from iv.player import Player

def game_decoder(json_obj):
    # return TheGame(
    #     name=json_obj["name"],
    #     players=json_obj["players"],
    #     history=json_obj["history"],
    #     bots=json_obj["bots"],
    #     round=json_obj["round"],
    #     players_file=json_obj["players_file"],
    #     history_file=json_obj["history_file"],
    #     market_file=json_obj["market_file"],
    #     market=json_obj["market"],        
    #     load=True
    # )

    return TheGame(
        load=True,
        **json_obj
    )

def player_decoder(json_obj):
    return Player(
        **json_obj
    )