class market:
    def __init__(self):
        pass

    def bring(self, player, item_id):
        pass


class marketItem:
    def __init__(
        self
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
        if getattr(player, self.requirement):
            return True
        else: return False

    def affect(self, player):
        setattr(player, self.effect, True) ###########

