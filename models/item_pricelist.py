class ItemPricelist:
    def __init__(self, name, qty, price_min, price_steam=None, liquidity=None):
        self.name = name
        self.qty = qty
        self.price_min = price_min
        self.price_steam = price_steam
        self.liquidity = liquidity

    def __repr__(self):
        """Make it print()able"""
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"