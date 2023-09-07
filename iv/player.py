import json
import os
import numpy as np
import pandas as pd

# from iv.helper import player_decoder

def player_decoder(json_obj):
    return Player(
        **json_obj
    )

class Player:
    def __init__(
        self,
        name,
        pid,
        isBot = False,
        three_big_used=False,

        principality=False,
        state=False,
        empire=False,
        capital=False,

        mines=0,
        factories=0,
        central=0,
        harbor=0,

        hasNavy=False,
        money=0,
        next_player_pid=None,


        ):

        self.name = name
        self.pid = pid
        self.isBot = isBot
        self.three_big_used = three_big_used

        self.principality = principality #
        self.state = state #
        self.empire = empire #
        self.capital = capital #

        self.mines = mines
        self.factories = factories
        self.central = central #
        self.harbor = harbor #

        self.hasNavy = hasNavy
        self.money = money
        self.next_player_pid = next_player_pid

    
    # def set_action(self):
    #     """
    #     Buy
    #     Attack
    #     3 Big
    #     Transfer
    #     """
    #     pass
        
    # def reverse_action(self):
    #     pass

    def buy(self, game, market_id):
        item = game.market[market_id]
        item_name = item["name"]
        item_price = item["price"]
        
        if self.money >= item_price:
            self.money -= item_price
            game.case_money += item_price
            
            game.log_action(
                player = self,
                action = "buy",
                subtype = item_name,
                description = f'Player {self.name} bought {item_name}.',
                cost = item_price,
                target = None
            )
        
            if item_name == "donanma":
                self.hasNavy = True
            
        else:
            raise Exception(f"The player {self.name} does not have enough money.")

    def attack(self, game, target, status):
        if isinstance(target, Player):
            game.log_action(
                player = self,
                action = "attack",
                subtype = status,
                description = f'Player {self.name} attacked to {target.name}. Result of the attack is {status}.',
                cost = None,
                target = target.pid
            )
        elif isinstance(target, str):
            game.log_action(
                player = self,
                action = "attack",
                subtype = status,
                description = f'Player {self.name} attacked to {target}. Result of the attack is {status}.',
                cost = None,
                target = target
            )

    def three_big(self, game, status):
        if self.three_big_used:
            raise Exception("Three big is used. Can not be used.")
        
        else:
            self.three_big_used = True
            game.log_action(
                player = self,
                action = "three_big",
                subtype = status,
                description = f'Player {self.name} used three big and attacked. Result of the attack is {status}.',
                cost = None,
                target = None
            )

    def transfer(self, game, target, amount):
        if self.money >= amount:

            self.money -= amount
            target.money += int(amount * 0.8)
            game.case_money += int(amount * 0.2)

            game.log_action(
                player = self,
                action = "transfer",
                subtype = "To Player",
                description = f'Player {self.name} transferred {amount} to {target.name}.',
                cost = amount,
                target = target.pid
            )
        else:
            raise Exception(f"The player {self.name} does not have enough money.")
    
    def serialize(self):
        # return json.dumps(self.__dict__, default=lambda obj: obj.__dict__, indent=4, ensure_ascii=False)
        return {attr: getattr(self, attr) for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__") and not attr == "game"}