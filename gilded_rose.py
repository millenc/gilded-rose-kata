# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if item.name == "Aged Brie":
                self.update_aged_brie_item_quality(item)
            elif item.name == "Sulfuras, Hand of Ragnaros":
                self.update_sulfuras_item_quality(item)
            elif item.name == "Backstage passes to a TAFKAL80ETC concert":
                self.update_backstage_pass_item_quality(item)
            else:
                self.update_item_quality(item)

    def update_item_sell_in(self, item):
        item.sell_in -= 1
    
    def update_item_quality(self, item):
        self.update_item_sell_in(item)
        item.quality = max(0, item.quality - (1 if item.sell_in >= 0 else 2) * (2 if item.name.startswith("Conjured") else 1))

    def update_aged_brie_item_quality(self, item):
        self.update_item_sell_in(item)
        item.quality = min(50, item.quality + 1)

    def update_sulfuras_item_quality(self, item):
        pass

    def update_backstage_pass_item_quality(self, item):
        self.update_item_sell_in(item)
        item.quality = 0 if item.sell_in < 0 else min(50, item.quality + 1 + (1 if item.sell_in < 11 else 0)
                                                                           + (1 if item.sell_in < 6 else 0))

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
