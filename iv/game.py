import json
import os
import numpy as np
import pandas as pd
from json import JSONEncoder

from iv.player import Player

class TheGame:
    def __init__(
        self,
        name=None,
        players=None,
        history=None,
        bots=None,
        round=None,
        players_file=None,
        history_file=None,
        market_file=None,
        market=None,        
        load=False
    ):
        
        if load:
            self.name = name
            self.players = players ##
            self.history = history
            self.bots = bots ##
            self.round = round

            self.players_file = players_file
            self.history_file = history_file
            self.market_file = market_file

            self.market = market
            
        else:
            if name:
                self.name = name
                self.players = []
                self.history = []
                self.bots = []
                self.round = 0
                
                self.players_file = os.path.join(".", self.name, "players.json")
                self.history_file = os.path.join(".", self.name, "history.json")
                self.market_file = os.path.join(".", "market.json")
                
                self.market = json.loads(pd.read_csv("market.csv",delimiter=";").set_index("id").to_json(orient="index"))

            else:
                raise Exception("Name is not set for this game. Give a name to the game you have created.")
    
    def add_player(self, name, bot=False):
        player = Player(
            name = name,
            pid = len(self.players) + 1,
#             game = self
        )
        self.players.append(player)
        
        self.log_action(
            player = player,
            action = "system",
            subtype = "Add player",
            description = f'Player {player.name} has been added to the game.',
            cost = None,
            target = None
        )
    
    def show_players(self):
        
        print(pd.DataFrame([player.serialize() for player in self.players]))

    def add_bot(self, name):
        bot = Player(
            name = name,
            pid = len(self.players) + 1001,
#             game = self,
            isBot = True
        )
        self.bots.append(bot)
        
        self.log_action(
            player = bot,
            action = "system",
            subtype = "Add bot",
            description = f'Bot {bot.name} has been added to the game.',
            cost = None,
            target = None
        )
    
    def save(self):
        
        ## Players
        if not os.path.exists(os.path.dirname(self.players_file)):
            os.makedirs(os.path.dirname(self.players_file))
        
        with open(self.players_file, "w") as json_file:
            players_data = [player.serialize() for player in self.players]
            json.dump(players_data, json_file)
            
        
        ## History
        if not os.path.exists(os.path.dirname(self.history_file)):
            os.makedirs(os.path.dirname(self.history_file))
        
        with open(self.history_file, "w") as json_file:
            json.dump(self.history, json_file)
        

    def log_action(self, player, action, subtype, description, cost, target):
        
        if action not in ["buy", "attack", "three_big", "transfer", "system"]:
            print("The action is invalid. Make a valid action.")
        
        else:
            self.history.append(
                {
                    "id" : player.id,
                    "player_name" : player.name,
                    "type" : action,
                    "subtype" : subtype,
                    "description" : description,
                    "cost" : cost,
                    "target" : target,
                    "round" : self.round
                }
            )
            
        self.save()
    
    def three_big_correction(self):
        
        useCorrection = np.all([player.three_big_used for player in self.players])
        
        if useCorrection:
            for player in self.players:
                player.three_big_used = False
    
    def serialize(self):
        init_serial = {attr: getattr(self, attr) for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__") and not attr == "game"}
        for k,v in init_serial.items():
            if isinstance(v, list):
                for i in range(len(v)):
                    if hasattr(v[i], "serialize"):
                        v[i] = v[i].serialize()
        # json.dumps(self.__dict__, default=lambda obj: obj.__dict__, indent=4, ensure_ascii=False)
        return init_serial