# -*- coding: utf-8 -*-
import re

MIN_ITEM_QUALITY = 0
MAX_ITEM_QUALITY = 50
MIN_ITEM_SELL_IN = 0

class GildedRose(object):
    def __init__(self, items):
        self.items = items
        self.updater = NameBasedQualityUpdater([
            ('^Aged Brie$', SellInQualityUpdater(IncreasingQualityUpdater(), DecreasingSellInUpdater())),
            ('^Sulfuras, Hand of Ragnaros$', None),
            ('^Backstage passes to a TAFKAL80ETC concert$', SellInQualityUpdater(BackstagePassQualityUpdater(), DecreasingSellInUpdater())),
            ('^Conjured.*$', SellInQualityUpdater(DecreasingBySellInQualityUpdater(before_sell_in=2, after_sell_in=4), DecreasingSellInUpdater())),
            ('^.*$', SellInQualityUpdater(DecreasingBySellInQualityUpdater(before_sell_in=1, after_sell_in=2), DecreasingSellInUpdater()))
        ])

    def update_quality(self):
        for item in self.items:
            self.updater.update_quality(item)

class QualityUpdater(object):
    def update_quality(self, item):
        pass
    
class SellInUpdater(object):
    def update_sell_in(self, item):
        pass

class DecreasingSellInUpdater(SellInUpdater):
    def update_sell_in(self, item):
        item.sell_in -= 1

class SellInQualityUpdater(QualityUpdater):
    def __init__(self, quality_updater, sell_in_updater):
        self.quality_updater = quality_updater
        self.sell_in_updater = sell_in_updater

    def update_quality(self, item):
        if self.sell_in_updater:
            self.sell_in_updater.update_sell_in(item)

        if self.quality_updater:
            self.quality_updater.update_quality(item)

class DecreasingBySellInQualityUpdater(QualityUpdater):
    def __init__(self, before_sell_in, after_sell_in):
        self.before_sell_in = before_sell_in
        self.after_sell_in = after_sell_in

    def update_quality(self, item):
        item.quality = max(MIN_ITEM_QUALITY, item.quality - (self.before_sell_in if item.sell_in >= MIN_ITEM_SELL_IN else self.after_sell_in))

class IncreasingQualityUpdater(QualityUpdater):
    def update_quality(self, item):
        item.quality = min(MAX_ITEM_QUALITY, item.quality + 1)

class BackstagePassQualityUpdater(QualityUpdater):
    def update_quality(self, item):
        item.quality = MIN_ITEM_QUALITY if item.sell_in < MIN_ITEM_SELL_IN else min(MAX_ITEM_QUALITY, item.quality + 1 
                                                                                                      + (1 if item.sell_in < 11 else 0)
                                                                                                      + (1 if item.sell_in < 6 else 0))

class NameBasedQualityUpdater(QualityUpdater):
    def __init__(self, rules):
        self.rules = rules

    def update_quality(self, item):
        for pattern, updater in self.rules:
            if re.match(pattern, item.name):
                if updater:
                    updater.update_quality(item)
                break

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
