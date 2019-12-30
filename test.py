import unittest
from main import Player, YuGiOhMaster

class YuGiOhMasterTest(unittest.TestCase):
    def test_initial_stock(self):
        master = YuGiOhMaster()
        self.assertEqual(master.getStock(), 0)
    
    def test_updated_stock(self):
        master = YuGiOhMaster()
        master.updateStock(100)
        self.assertEqual(master.getStock(), 100)

    def test_get_card_by_name(self):
        self.assertEqual(type(YuGiOhMaster.getCardByName("Blue-Eyes White Dragon")), dict)
        self.assertIsNone(YuGiOhMaster.getCardByName("__invalid__"))

    def test_get_cards_by_archetype(self):
        self.assertEqual(type(YuGiOhMaster.getCardsByArchetype("Blue-Eyes")), list)
        self.assertIsNone(YuGiOhMaster.getCardsByArchetype("__invalid__"))

    def test_get_by_type(self):
        cards = YuGiOhMaster.getCardsByArchetype("Blue-Eyes")
        self.assertEqual(type(YuGiOhMaster.getByType(cards, "Monster")), list)

        self.assertEqual(type(YuGiOhMaster.getByType(cards, "__invalid__")), list)
        self.assertEqual(len(YuGiOhMaster.getByType(cards, "__invalid__")), 0)
        self.assertEqual(type(YuGiOhMaster.getByType([], "__invalid__")), list)
        self.assertEqual(len(YuGiOhMaster.getByType(cards, "__invalid__")), 0)
        self.assertIsNone(YuGiOhMaster.getByType("__invalid__", "__invalid__"))


    def test_get_card_price(self):
        card = YuGiOhMaster.getCardByName("Blue-Eyes White Dragon")
        self.assertEqual(YuGiOhMaster.getCardPrice(card), card["card_prices"]["ebay_price"])
        self.assertIsNone(YuGiOhMaster.getCardPrice("__invalid__"))

class PlayerTest(unittest.TestCase):
    def test_initial_transactions(self):
        p = Player("Name", 300)
        self.assertEqual(p.getTransactions(), [])

    def test_buget(self):
        p = Player("Name", 100)
        self.assertEqual(p.getBudget(), 100)
        p.changeBudget(200)
        self.assertEqual(p.getBudget(), 200)
        self.assertIsNone(p.changeBudget("__invalid__"))
    
    def test_name(self):
        p = Player("Name", 100)
        self.assertEqual(p.getName(), "Name")

    def test_initial_deck(self):
        p = Player("Name", 100)
        self.assertIsNone(p.getDeck()) 

    def test_buy_card_invalid(self):
        p = Player("Name", 0)
        self.assertIsNone(p.buyCard("Blue-Eyes White Dragon"))
        self.assertIsNone(p.buyCard("__invalid__"))
    
    def test_buy_card_valid(self):
        player = Player("Name", 100)
        initialBudget = player.getBudget()
        card = YuGiOhMaster.getCardByName("Blue-Eyes White Dragon")
        player.buyCard("Blue-Eyes White Dragon")
        self.assertEqual(player.getBudget(), float(initialBudget) - float(card["card_prices"]["ebay_price"]))
        self.assertEqual(len(player.getDeck()), 1)
        self.assertEqual(len(player.getTransactions()), 1)

    def test_add_to_deck_single(self):
        card = YuGiOhMaster.getCardByName("Blue-Eyes White Dragon")
        player = Player("Name", 100)
        player.addToDeck(card)
        self.assertEqual(len(player.getDeck()), 1)


if __name__ == '__main__':
    unittest.main()