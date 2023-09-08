from copy import deepcopy

class Market:
    def __init__(self, items, load=False):
        self.items = {}
        for item in items:
            self.items[item["id"]] = MarketItem(**item)

    def purchase(self, game, player, item_id):
        item = self.items[item_id]
        enough_money, adequate = item.buyable(player)

        if enough_money and adequate:
            player.money -= item.price
            game.case_money += item.price

            item.affect(player)
            
            game.log_action(
                player = player,
                action = "buy",
                subtype = item.name,
                description = f'Player {player.name} bought {item.name}.',
                cost = item.price,
                target = None
            )
        
        return enough_money, adequate



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
            
            # elif isinstance(v, MarketItem):
            #     serialized[k] = v.serialize()

        return serialized
        
def market_decoder(json_obj: dict) -> Market:
    return Market(
        load=True,
        **json_obj
    )
    
class MarketItem:
    def __init__(
        self,
        id,
        name,
        price,
        requirement = None,
        effect = None
        ):
        self.id = id
        self.name = name
        self.price = price

        self.requirement = requirement
        self.effect = effect
    
    def buyable(self, player):
        if player.money >= self.price:
            if self.requirement == None:
                return True, True
            if getattr(player, self.requirement):
                return True, True
            else:
                return True, False
        else:
            return False, False

    def affect(self, player):
        val = getattr(player, self.effect)
        if isinstance(val, bool):
            if self.effect == "three_big_used": setattr(player, self.effect, False)
            else: setattr(player, self.effect, True)
        elif isinstance(val, int):
            setattr(player, self.effect, val + 1)

    def serialize(self):
        # return json.dumps(self.__dict__, default=lambda obj: obj.__dict__, indent=4, ensure_ascii=False)
        return {attr: getattr(self, attr) for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")}

def item_decoder(json_obj: dict) -> MarketItem:
    return MarketItem(
        **json_obj
    )