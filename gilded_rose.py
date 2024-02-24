# -*- coding: utf-8 -*-


class Item:
    """ DO NOT CHANGE THIS CLASS!!!"""
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

class ItemUpdateStrategy:
    def update(self, item):
        raise NotImplementedError("Update method not implemented")

class NormalItemUpdateStrategy(ItemUpdateStrategy):
    def update(self, item):
        item.sell_in -= 1
        degrade_rate = 2 if item.sell_in < 0 else 1
        item.quality = max(0, item.quality - degrade_rate)

class AgedBrieUpdateStrategy(ItemUpdateStrategy):
    def update(self, item):
        item.sell_in -= 1
        increase_rate = 2 if item.sell_in < 0 else 1
        item.quality = min(50, item.quality + increase_rate)

class SulfurasUpdateStrategy(ItemUpdateStrategy):
    def update(self, item):
        pass  # Sulfuras doesn't change

class BackstagePassesUpdateStrategy(ItemUpdateStrategy):
    def update(self, item):
        item.sell_in -= 1
        if item.sell_in < 0:
            item.quality = 0
        elif item.sell_in < 5:
            item.quality = min(50, item.quality + 3)
        elif item.sell_in < 10:
            item.quality = min(50, item.quality + 2)
        else:
            item.quality = min(50, item.quality + 1)

class ConjuredItemUpdateStrategy(ItemUpdateStrategy):
    def update(self, item):
        item.sell_in -= 1
        degrade_rate = 4 if item.sell_in < 0 else 2  # Conjured items degrade twice as fast
        item.quality = max(0, item.quality - degrade_rate)


class UpdateStrategyFactory:
    @staticmethod
    def get_update_strategy(item):
        if item.name == "Aged Brie":
            return AgedBrieUpdateStrategy()
        elif item.name == "Sulfuras, Hand of Ragnaros":
            return SulfurasUpdateStrategy()
        elif item.name == "Backstage passes to a TAFKAL80ETC concert":
            return BackstagePassesUpdateStrategy()
        elif item.name.startswith("Conjured"):
            return ConjuredItemUpdateStrategy()
        else:
            return NormalItemUpdateStrategy()

class GildedRose(object):

    def __init__(self, items: list[Item]):
        # DO NOT CHANGE THIS ATTRIBUTE!!!
        self.items = items

    def update_quality(self):
        for item in self.items:
            strategy = UpdateStrategyFactory.get_update_strategy(item)
            strategy.update(item)