import requests
import json

class YuGiOhMaster:
    def __init__(self, stock=0):
        self.stock=stock
    
    def getStock(self):
        return self.stock
    
    def updateStock(self, s):
        self.stock = s
        return s
    
    # following methods are classmethods so you do not need to create a master object
    # this is because the master's role is only to deal with the API and organizing results
    @classmethod
    def getCardByName(self, n):
        if type(n) == str:
            resp = requests.get('https://db.ygoprodeck.com/api/v5/cardinfo.php?name='+n)
            if resp.status_code != 200: # error occurred
                print("Not valid card")
                return None
            j = json.loads(json.dumps(resp.json()))[0] # resp.json -> str, str -> dictionary
            return j
    @classmethod
    def getCardsByArchetype(self, n):
        if type(n) == str:
            resp = requests.get('https://db.ygoprodeck.com/api/v5/cardinfo.php?archetype='+n)
            if resp.status_code != 200: # error occurred
                print("Not valid archetype")
                return None
            j = json.loads(json.dumps(resp.json())) # resp.json -> str, str -> dictionary
            return j
    @classmethod
    def getByType(self, l, t):
        try:
            res = (card for card in l if t in card["type"])
            return list(res)
        except:
            print("Not valid type")
            return None
    @classmethod
    def printCardNames(self, l):
        for card in l:
            if card["name"] is not None:
                print(card["name"])
    @classmethod
    def getCardPrice(self, c):
        try:
            return c["card_prices"]["ebay_price"]
        except:
            try:
                return c["card_prices"]["tcgplayer_price"]
            except:
                print("Not able to get price")
                return None

class Player:
    # keep deck and transactions as None in order to not reuse [] as arguments
    def __init__(self, name, budget, deck=None, transactions=None):
        self.name = name
        self.budget = float(budget)
        self.deck = deck
        self.transactions = transactions

    # checks type of b, checks that transactions is initialized
    def changeBudget(self, b):
        if type(b) is int:
            print("New budget is {}".format(b))
            self.budget = b
            if self.transactions is None:
                self.transactions = ["Budget changed to {}".format(b)]
            else:
                self.transactions.append("Budget changed to {}".format(b))
            return b
        else:
            print("Not valid budget")
            return None
    
    def getBudget(self):
        return self.budget

    def getName(self):
        return self.name

    def getDeck(self):
        return self.deck

    # checks that deck is initialized
    def printDeckNames(self):
        if self.deck is None:
            print([])
        for i in self.deck:
            print(i["name"])

    # checks price is valid and that budget is sufficient
    def buyCard(self, c):
        card = YuGiOhMaster.getCardByName(c)
        if card:
            price = float(YuGiOhMaster.getCardPrice(card))
            if price is None:
                print("Card not for sale")
                return None
            if self.budget - price < 0:
                print("You do not have enough money!")
                return None

            print("{} costs {}. You will be left with ${}.".format(c, price, self.budget-price))
            self.budget -= price
            self.addToDeck(card)
            print("{} has been added to your deck!".format(c))
            if self.transactions is None:
                self.transactions = ["Bought {} for {}".format(c, price)]
            else:
                self.transactions.append("Bought {} for {}".format(c, price))
            return self.budget
        else:
            print("Not valid card")
            return None
    
    # initialize transactions and append  transaction
    def getTransactions(self):
        if self.transactions is None:
            self.transactions = []
        return self.transactions
    
    # initialize deck and append card
    def addToDeck(self, c):
        if self.deck is None:
            self.deck = []
        self.deck.append(c)
    


        

