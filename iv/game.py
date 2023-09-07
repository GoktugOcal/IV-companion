import json
import os
import numpy as np
import pandas as pd
from datetime import datetime
from json import JSONEncoder
from copy import deepcopy

from iv.player import Player, player_decoder

class TheGame:
    def __init__(
        self,
        name=None,
        players=None,
        history=None,
        bots=None,
        coal_gain = None,
        factory_gain = None,
        round=None,
        round_player=None,
        round_player_pid=None,
        final_player_pid=None,
        game_file = None,
        players_file=None,
        history_file=None,
        market_file=None,
        market=None,
        latest_save_time=None,
        load=False
    ):
        
        if load:
            self.name = name
            self.players = {}
            for player in players:
                pl = player_decoder(player)
                self.players[pl.pid] = player_decoder(player)

            self.history = history
            self.bots = {} ##
            for bot in bots:
                b = player_decoder(bot)
                self.bots[b.pid] = player_decoder(bot)
            self.round = round
            if round_player_pid == -1: self.round_player = Player("game", -1)
            else: self.round_player = self.players[round_player_pid]
            self.round_player_pid = round_player_pid
            self.final_player_pid = final_player_pid

            self.coal_gain = coal_gain
            self.factory_gain = factory_gain

            self.game_file = game_file
            self.players_file = players_file
            self.history_file = history_file
            self.market_file = market_file

            self.market = market

            self.latest_save_time = latest_save_time
            
        else:
            if name:
                self.name = name
                self.players = {}
                self.history = []
                self.bots = {}
                self.round = 0
                self.round_player = Player("game", -1)
                self.round_player_pid = -1
                self.final_player_pid = -1
                
                self.game_file = os.path.join(".", "games", self.name, "game.json")
                self.players_file = os.path.join(".", "games", self.name, "players.json")
                self.history_file = os.path.join(".", "games", self.name, "history.json")
                self.market_file = os.path.join(".", "market.json")
                
                self.market = json.loads(pd.read_csv("market.csv",delimiter=";").to_json(orient="records"))

            else:
                raise Exception("Name is not set for this game. Give a name to the game you have created.")

    def set_coal_gain(self, gain):
        self.coal_gain = gain
        self.save()
    
    def set_factory_gain(self, gain):
        self.factory_gain = gain
        self.save()
    
    def add_player(self, name, bot=False):

        player = Player(
            name = name,
            pid = len(self.players.values()) + 1,
#             game = self
        )
        self.players[player.pid] = player
        
        self.log_action(
            player = player,
            action = "system",
            subtype = "Add player",
            description = f'Player {player.name} has been added to the game.',
            cost = None,
            target = None
        )

    def get_player_by_pid(self, pid):
        try:
            return self.players[pid]
        except:
            return None
        # for player in self.players.values():
        #     if player.pid == pid:
        #         return player
        # return None
    
    def get_players_dataframe(self):
        return pd.DataFrame([player.serialize() for player in self.players.values()])
        #[["pid", "name", "money", "three_big_used", "isBot"]]
    
    def show_players(self):
        print(self.get_players_dataframe())

    def add_bot(self, name):
        bot = Player(
            name = name,
            pid = len(self.players.values()) + 1001,
#             game = self,
            isBot = True
        )
        self.bots[bot.pid] = bot
        
        self.log_action(
            player = bot,
            action = "system",
            subtype = "Add bot",
            description = f'Bot {bot.name} has been added to the game.',
            cost = None,
            target = None
        )
    
    def save(self):

        self.latest_save_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        ## Game
        if not os.path.exists(os.path.dirname(self.game_file)):
            os.makedirs(os.path.dirname(self.game_file))
        
        with open(self.game_file, "w") as json_file:
            json.dump(self.serialize(), json_file)
        
        ## Players
        if not os.path.exists(os.path.dirname(self.players_file)):
            os.makedirs(os.path.dirname(self.players_file))
        
        with open(self.players_file, "w") as json_file:
            players_data = [player.serialize() for player in self.players.values()]
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
                    "id" : player.pid,
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
        
        useCorrection = np.all([player.three_big_used for player in self.players.values()])
        
        if useCorrection:
            for player in self.players.values():
                player.three_big_used = False

    def can_game_start(self):
        attributes = vars(self)
        can_start = True
        for attribute_name, attribute_value in attributes.items():
            if attribute_value is None:
                print(attribute_name, "=", attribute_value)
                can_start = False
        return can_start

    def start_game(self):
        player_list = list(self.players.values())
        for idx in range(len(player_list)):
            if idx + 1 >= len(player_list):
                player_list[idx].next_player_pid = player_list[0].pid
                self.final_player_pid = player_list[idx].pid
            else: player_list[idx].next_player_pid = player_list[idx+1].pid
        
        self.round_player_pid = player_list[0].pid
        self.round_player = player_list[0]
        self.round = 1

        self.save()
    
    def go_to_next_player(self):
        curr_pid = self.round_player_pid
        curr_player = self.players[curr_pid]
        self.round_player_pid = curr_player.next_player_pid
        self.round_player = self.players[self.round_player_pid]

        print(f"Round : {self.round} | Player : {self.round_player.name} | Next : {self.round_player.next_player_pid}")
        if curr_pid == self.final_player_pid:
            self.go_to_next_round()
        
        self.three_big_correction()
        self.save()

    def go_to_next_round(self):
        """
        """
        print("Next round!!")
        self.round += 1
        for player in list(self.players.values()):
            player.money += player.mines*self.coal_gain + player.factories*self.factory_gain # Tour reward?

    def serialize(self):
        init_serial = {attr: getattr(self, attr) for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__") and not attr == "game"}
        serialized = deepcopy(init_serial)

        for k,v in serialized.items():
            if isinstance(v, dict):
                players_list = list(v.values())
                for i in range(len(v.values())):
                    if hasattr(players_list[i], "serialize"):
                        # print(players_list[i].serialize())
                        players_list[i] = players_list[i].serialize()

                serialized[k] = players_list
            
            elif isinstance(v, Player):
                serialized[k] = v.serialize()

        return serialized


def game_decoder(json_obj: dict) -> TheGame:
    return TheGame(
        load=True,
        **json_obj
    )