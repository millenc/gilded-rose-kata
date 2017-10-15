# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose

class GildedRoseTest(unittest.TestCase):
    def _update_item(self, item):
        GildedRose([item]).update_quality()

        return item
    
    def test_quality_degrades(self):
        self.assertEquals(self._update_item(Item("Elixir of the Mongoose", 10, 50)).quality, 49)

    def test_conjured_quality_degrades(self):
        self.assertEquals(self._update_item(Item("Conjured Elixir of the Mongoose", 10, 50)).quality, 48)

    def test_sell_in_decrements(self):
        self.assertEquals(self._update_item(Item("Elixir of the Mongoose", 10, 50)).sell_in, 9)

    def test_quality_degrades_twice_as_fast_when_sell_in_passed(self):
        self.assertEquals(self._update_item(Item("Elixir of the Mongoose", 0, 50)).quality, 48)

    def test_conjured_quality_degrades_twice_as_fast_when_sell_in_passed(self):
        self.assertEquals(self._update_item(Item("Conjured Elixir of the Mongoose", 0, 50)).quality, 46)

    def test_quality_higher_or_equal_zero(self):
        self.assertEquals(self._update_item(Item("Elixir of the Mongoose", 0, 0)).quality, 0)

    def test_quality_less_or_equal_fifty(self):
        self.assertEquals(self._update_item(Item("Aged Brie", 10, 50)).quality, 50)

    def test_aged_brie_quality_increases(self):
        self.assertEquals(self._update_item(Item("Aged Brie", 10, 40)).quality, 41)

    def test_sulfuras_inmutable(self):
        sulfuras = Item("Sulfuras, Hand of Ragnaros", 10, 80)

        self.assertEquals(self._update_item(sulfuras).quality, 80)
        self.assertEquals(self._update_item(sulfuras).sell_in, 10)

    def test_backstage_passes_quality_increases(self):
        self.assertEquals(self._update_item(Item("Backstage passes to a TAFKAL80ETC concert", 15, 40)).quality, 41)

    def test_backstage_passes_quality_increases_when_sell_in_ten_days_or_less(self):
        self.assertEquals(self._update_item(Item("Backstage passes to a TAFKAL80ETC concert", 10, 40)).quality, 42)

    def test_backstage_passes_quality_increases_when_sell_in_five_days_or_less(self):
        self.assertEquals(self._update_item(Item("Backstage passes to a TAFKAL80ETC concert", 5, 40)).quality, 43)

    def test_backstage_passes_quality_drops_to_zero_when_sell_in_passed(self):
        self.assertEquals(self._update_item(Item("Backstage passes to a TAFKAL80ETC concert", 0, 40)).quality, 0)

if __name__ == '__main__':
    unittest.main()
