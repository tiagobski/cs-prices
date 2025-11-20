class Item:
    def __init__(self, site, id, name, float, price, tradable, tradelock_expires_at, url):
        self.site = site
        self.id = id
        self.name = name
        self.float = float
        self.price = price
        self.tradable = tradable
        self.tradelock_expires_at = tradelock_expires_at
        self.url = url

    def __repr__(self):
        """Make it print()able"""
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"