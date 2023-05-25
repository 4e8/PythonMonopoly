from array import array
from cgi import print_exception
from enum import Enum
import random
from typing import List

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style


# Essentionals
#region
colorama_init()
class Color(Enum):
    WHITE =     f"{Fore.WHITE}- white-{Style.RESET_ALL}"
    RED =       f"{Fore.RED}-  red  -{Style.RESET_ALL}"
    ORANGE =    f"{Fore.LIGHTRED_EX } -orange-{Style.RESET_ALL}"
    YELLOW =    f"{Fore.YELLOW }-yellow-{Style.RESET_ALL}"
    GREEN =     f"{Fore.GREEN }- green-{Style.RESET_ALL}"
    TEAL =      f"{Fore.LIGHTCYAN_EX }- teal -{Style.RESET_ALL}"
    BLUE =      f"{Fore.LIGHTBLUE_EX }- blue -{Style.RESET_ALL}"
    VIOLET =    f"{Fore.MAGENTA }-violet-{Style.RESET_ALL}"
    ROSE =      f"{Fore.LIGHTMAGENTA_EX }- rose -{Style.RESET_ALL}"


class Cardinal(Enum):
    EMPTY = "empty"
    NORTH = "North"
    EAST = "East"
    SOUTH = "South"
    WEST = "West"

def UserIntInput(text):
    print(f"{Fore.LIGHTYELLOW_EX }")
    inp = input(text)
    #print(f"{Style.RESET_ALL}")
    try:
        inp = int(inp)
    except:
        print("Input incorrect!")
        return UserIntInput(text)
    else:
        return int(inp)

def UserIntInputFrom(text,ar:array):
    print(f"{Fore.LIGHTYELLOW_EX }")
    inp = input(text)
    print(f"{Style.RESET_ALL}")
    try:
        if int(inp) in ar:
            inp = int(inp)
        else:
            raise Exception
    except:
        print("Input incorrect!")
        return UserIntInputFrom(text,ar)
    else:
        return int(inp)

#endregion

# PLayer
class Player:

    def __init__(self, isBank, playerNumber):
        self.tileNumber = 0
        if isBank == False : tiles[self.tileNumber].guests.append(self)
        self.playerNumber = playerNumber
        self.money = 1500
        self.cardsOwned = []
        self.inJail = False
        self.housesTotal = 0
        self.hotelsTotal = 0

    def __str__(self):
        return "Player (" + str(self.playerNumber) + ")"

    def ShowInfo(self):
        print("--------")
        s = "None"
        if len(self.cardsOwned) > 0: 
            s = ""
            for c in self.cardsOwned: 
                s += str(c) + "  "
        print("You're on tile [" + str(self.tileNumber) + "]. Cash:" + str(self.money) + ". Cards: " + s)

    def TransferMoneyTo(self, amount , reciever):
        self.money -= amount
        reciever.money += amount
        print(str(self) + " gives to " + str(reciever) + " " + str(amount))

    def Move(self, n):
        self.MoveIgnoreActivation(n)
        tiles[self.tileNumber].ActivateCard(self)

    def MoveIgnoreActivation(self, n):
        tiles[self.tileNumber].RemoveGuest(self)
        self.tileNumber += n
        if (self.tileNumber >= 40 or self.tileNumber == 0):
            self.tileNumber -= 40
            self.money += 200
        tiles[self.tileNumber].AddGuest(self)

    def MoveTo(self, n):
        tiles[self.tileNumber].RemoveGuest(self)
        self.tileNumber = n
        tiles[self.tileNumber].AddGuest(self)
        if (self.tileNumber == 0):
            self.money += 200
        tiles[self.tileNumber].ActivateCard(self)

    def AddCard(self,n):
        self.cardsOwned.append(n)

    def RemoveCard(self,n):
        self.cardsOwned.remove(n)

Bank = Player(True, 0)

# Card
class Card:
    name = "Card"
    guests:List[Player] = []
    
    def __init__(self, newName):
        self.name = newName
        self.guests:List[Player] = []
        
    def ActivateCard(self,player:Player):
        pass
    
    def ShowCard(self):
        print("------")
        print(self.name)
        print("------")

    def AddGuest(self,p):
        self.guests.append(p)
    def RemoveGuest(self, p):
        self.guests.remove(p)

# ObtainableCard
class ObtainableCard(Card):
    owner = Bank
    price = 0
    mortaged = False
    mortageValue = 0

    def __init__(self, newName):
        self.name = newName
        self.owner = Bank

    def SellCardTo(self, newOwner:Player, customPrice):
        if (newOwner.money >= customPrice):
            newOwner.TransferMoneyTo(customPrice,Bank)
            if tiles.index(self) in self.owner.cardsOwned: self.owner.RemoveCard(tiles.index(self))
            self.owner = newOwner
            self.owner.AddCard(tiles.index(self))
        else: print_exception()

    def ActivateCard(self, player: Player):
        if (self.owner == Bank):
            if player.money >= self.price :
                self.ShowCard()
                userInput = UserIntInputFrom("Do you want to buy this Card for " + str(self.price) + "?\n1. Yes; 2.No (starts Auction)\n", [1,2])
                if userInput == 1: 
                    self.SellCardTo(player,self.price)
                    return
                elif userInput == 2: pass
            self.Auction(player)
        else:
            self.SubActivateCard(player)

    def SubActivateCard(self,player:Player):
        pass

    def Auction(self,player):
        topPrice = [self.price,Bank]
        index = players.index(player) + 1
        aucPlayers:List[Player] = []
        print("Auction participants:")
        for p in players:
            if p != player: 
                aucPlayers.append(p)
                print(p)
        if len(aucPlayers) == 1:
            userInput = UserIntInputFrom(str(aucPlayers[0]) + ", do you want to buy this Card for " + str(self.price) + "?\n1. Yes; 2.No\n", [1,2])
            if userInput == 1: self.SellCardTo(player,self.price)
            elif userInput == 2: return
        while len(aucPlayers) > 1:
            for p in aucPlayers:
                offer = UserIntInputFrom(str(p) + ", your balance is: " + p.money + ". Set your price (lower is pass): \n", [1,2])
                if offer > p.money or offer < topPrice[0]:
                    print(str(p) + "Passed!")
                    aucPlayers.remove()
                else:
                    print(str(p) + "'s offer is " + str(offer))
                    topPrice = [offer, players[index]]
        self.SellCardTo(topPrice[1],topPrice[0])
        print("Card goes to " + str(p) + "!")

    def MortageCard(self):
        self.mortaged = True
        self.owner.money += self.mortageValue

    def UnMortageCard(self):
        self.mortaged = False
        self.owner.money -= self.mortageValue
        self.owner.money -= int(str(self.mortageValue)[:-1])

# ColorCard
class ColorCard(ObtainableCard):

    def __init__(self, colorCode, rent0, rent1, rent2, rent3, rent4, rent5, priceHouse, mortageValue):
        self.colorCode = colorCode
        self.rent = [rent0, rent1, rent2, rent3, rent4, rent5]
        self.priceHotel = self.priceHouse = priceHouse
        self.mortageValue = mortageValue
        self.price = mortageValue + mortageValue
        self.housesBuilt = 0
        self.guests:List[Player] = []

    def SubActivateCard(self, player:Player):
        if (self.owner != player and self.mortaged == False):
            player.TransferMoneyTo(self.rent[self.housesBuilt],self.owner)
            if ColorMonopolized(self.colorCode):
                player.TransferMoneyTo(self.rent[self.housesBuilt],self.owner)

    def ShowCard(self):
        print("------")
        print(self.name)
        print(self.colorCode.value)
        print("Rent : " + str(self.rent[0]))
        print("Rent 1h : " + str(self.rent[1]))
        print("Rent 2h : " + str(self.rent[2]))
        print("Rent 3h : " + str(self.rent[3]))
        print("Rent 4h : " + str(self.rent[4]))
        print("Rent H : " + str(self.rent[5]))
        print("Price h : " + str(self.priceHouse))
        print("Mortage : " + str(self.mortageValue))
        print("Owner is " + str(self.owner))
        print("------")

    #Buy houses\hotels funcs
    #region
    def BuyHouse(self):
        if (self.housesBuilt < 5): 
            self.housesBuilt += 1
            self.owner.money -= self.priceHouse
            self.owner.housesTotal += 1
        elif (self.housesBuilt == 5): 
            self.housesBuilt += 1
            self.owner.money -= self.priceHouse
            self.owner.housesTotal -= 4
            self.owner.hotelsTotal += 1 
        else: print_exception()
    
    def SellHouse(self):
        if ( 0 < self.housesBuilt < 5): 
            self.houseBuilt -= 1
            self.owner.money += self.priceHouse
            self.owner.housesTotal -= 1
        elif (self.housesBuilt == 5):
            self.houseBuilt -= 5
            self.owner.money += self.priceHouse
            self.owner.hotelsTotal -= 1

        else: print_exception()
    #endregion

# StationCard 
class StationCard(ObtainableCard):
    rent = [25,50,100,200]
    def __init__(self, cardinal:Cardinal):
        self.cardinalDir = cardinal
        self.name = cardinal.value + " Station"
        self.mortageValue = 100
        self.price = self.mortageValue + self.mortageValue
        self.guests:List[Player] = []

    def SubActivateCard(self, player:Player):
        if (self.owner != player and self.mortaged == False):
            stationsOwned = 0
            for card in self.owner.cardsOwned:
                if card in [5,15,25,35]: stationsOwned += 1
            player.TransferMoneyTo(self.rent[stationsOwned - 1],self.owner)


    def ShowCard(self):
        print("------")
        print(self.name)
        print("Rent 1 St: " + str(self.rent[0]))
        print("Rent 2 St: " + str(self.rent[1]))
        print("Rent 3 St : " + str(self.rent[2]))
        print("Rent 4 St : " + str(self.rent[3]))
        print("Mortage : " + str(self.mortageValue))
        print("Owner is " + str(self.owner))
        print("------")

# CompanyCard
class CompanyCard(ObtainableCard):
    def __init__(self, name):
        self.name = name 
        self.rent = 0
        self.mortageValue = 75
        self.guests:List[Player] = []

    # FUN ACHIEVMENT : DO GAME WITHOUT MULTIPLYING
    def SubActivateCard(self, player:Player):
        if (self.owner != player and self.mortaged == False):
            rolledNum = Roll6x2()[0]
            if tiles[12].owner == tiles[28].owner:
                self.rent = rolledNum + rolledNum + rolledNum + rolledNum + rolledNum + rolledNum + rolledNum + rolledNum + rolledNum + rolledNum
            else: 
                self.rent = rolledNum + rolledNum + rolledNum + rolledNum 
            player.TransferMoneyTo(self.rent,self.owner)

    def ShowCard(self):
        print("------")
        print(self.name)
        print("Rent: Roll x4, x10 if owner has 2 Stations")
        print("Mortage : " + str(self.mortageValue))
        print("Owner is " + str(self.owner))
        print("------")

# TaxCard, ADD?? can go 10% of capitalization(money+cardprice+houses)
class TaxCard(Card):
    def __init__(self, tax):
        self.tax = tax
        self.name = "Tax " + str(tax)

    def ActivateCard(self, player):
        player.money -= self.tax
        print(str(player) + " paid a tax, -" + str(self.tax))
 
# GoJailCard
class GoJailCard(Card):
    def __init__(self,newName):
        self.name = newName
    def ActivateCard(self,player):
        tiles[player.tileNumber].RemoveGuest(player)
        tiles[10].AddGuest(player)
        player.tileNumber = 10
        if(-1 in player.cardsOwned):
            player.inJail = False
            player.RemoveCard(-1)
            print(str(player) + " used a card to get from Jail")
        else:
            player.inJail = True
            print(str(player) + " welcome to JAIL LOL")

# CommunityChestCard
class CommunityChestCard(Card):
    def ActivateCard(self, player):
        print("---- Community Chest!")
        n = random.randrange(16)
        match n:
            case 0:
                for p in players:
                    p.TransferMoneyTo(50,player)
            case 1:
                player.money += 25
            case 2:
                player.MoveTo(0)
            case 3:
                player.money -= 100
            case 4:
                player.money -= 50
            case 5:
                player.AddCard(-1) # free escape from jail
            case 6:
                player.money += 45
            case 7:
                player.money += 100
            case 8:
                ###field[25].Activate(player)
                player.MoveTo(25)
            case 9:
                player.money += 100
            case 10:
                player.money += 10
            case 11:
                player.money += 100
            case 12:
                player.money -= (player.housesTotal * 40) + (player.hotelsTotal * 115)
            case 13:
                player.money += 100
            case 14:
                player.money -= 20
            case 15:
                player.money -= 150

# ChanceCard
class ChanceCard(Card):
    def ActivateCard(self, player):
        print("---- Chance!")
        n = random.randrange(16)
        match n:
            case 0:
                for p in players:
                    player.TransferMoneyTo(50, p)
            case 1:
                player.money += 150
                player.AddCard(-1) # free escape from jail
            case 2:
                player.money -= 15
            case 3:
                player.MoveTo(0)
                player.money += 50
            case 4:
                player.Move(-3)
            case 5:
                if (player.tileNumber == 7):
                    player.MoveTo(5)
                    player.MoveTo(5)
                if (player.tileNumber == 22):
                    player.MoveTo(25)
                    player.MoveTo(25)
                if (player.tileNumber == 36):
                    player.MoveTo(35)
                    player.MoveTo(35)
            case 6:
                if (player.tileNumber == 7):
                    player.MoveTo(5)
                    player.MoveTo(5)
                if (player.tileNumber == 22):
                    player.MoveTo(25)
                    player.MoveTo(25)
                if (player.tileNumber == 36):
                    player.MoveTo(35)
                    player.MoveTo(35)
            case 7:
                player.MoveTo(10)
            case 8:
                player.money += 150
            case 9:
                player.money += 50
            case 10:
                if player.tileNumber > 5:
                    player.money += 200
                player.MoveTo(5)
            case 11:
                if player.tileNumber > 11:
                    player.money += 200
                player.MoveTo(11)
            case 12:
                player.MoveTo(39)
            case 13:
                player.MoveTo(24)
            case 14:
                if tiles[player.tileNumber + 1].owner != Bank and tiles[player.tileNumber + 1].owner != player :
                    player.MoveIgnoreActivation(1)
                    player.TransferMoneyTo(Roll6x2()[0],tiles[player.tileNumber + 1].owner)
            case 15:
                # player.money -= (player.housesTotal * 40) + (player.hotelsTotal * 115)
                for i in range(player.housesTotal):
                    player.money -= 25
                for i in range(player.hotelsTotal):
                    player.money -=  100

# Game Field with cards
global tiles
tiles:List[Card] = [
    Card("StartTile"),
    ColorCard(Color.RED,     2,  10,  30,  90, 160, 250,  50,  30),
    CommunityChestCard("CommunityChestCard"),
    ColorCard(Color.RED,     4,  20,  60, 180, 320, 450,  50,  30),
    TaxCard(200),
        
    StationCard(Cardinal.SOUTH),
    ColorCard(Color.ORANGE,  6,  30,  90, 270, 400, 550,  50,  50),
    ChanceCard("ChanceCard"),
    ColorCard(Color.ORANGE,  6,  30,  90, 270, 400, 550,  50,  50),
    ColorCard(Color.ORANGE,  8,  40, 100, 300, 450, 600,  50,  60),
        
    Card("Jail"),
    ColorCard(Color.YELLOW, 10,  50, 150, 450, 625, 750, 100,  70),
    CompanyCard("CompanyCard"),
    ColorCard(Color.YELLOW, 10,  50, 150, 450, 625, 750, 100,  70),
    ColorCard(Color.YELLOW, 12,  60, 180, 500, 700, 900, 100,  80),
        
    StationCard(Cardinal.WEST),
    ColorCard(Color.GREEN,  14,  70, 220, 550, 750, 950, 100,  90),
    CommunityChestCard("CommunityChestCard"),
    ColorCard(Color.GREEN,  14,  70, 220, 550, 750, 950, 100,  90),
    ColorCard(Color.GREEN,  16,  80, 220, 600, 800,1000, 100, 100),
        
    Card("FreeTile"),
    ColorCard(Color.TEAL,   18,  90, 250, 700, 875,1050, 150, 110),
    ChanceCard("ChanceCard"),
    ColorCard(Color.TEAL,   18,  90, 250, 700, 875,1050, 150, 110),
    ColorCard(Color.TEAL,   20, 100, 300, 750, 925,1100, 150, 120),
        
    StationCard(Cardinal.NORTH),         
    ColorCard(Color.BLUE,   22, 110, 330, 800, 975,1150, 150, 130),
    ColorCard(Color.BLUE,   22, 110, 330, 800, 975,1150, 150, 130),
    CompanyCard("CompanyCard"),
    ColorCard(Color.BLUE,   24, 120, 360, 850,1025,1200, 150, 140),
        
    GoJailCard("GoJail"),
    ColorCard(Color.VIOLET, 26, 130, 390, 900,1100,1275, 200, 150),
    ColorCard(Color.VIOLET, 26, 130, 390, 900,1100,1275, 200, 150),
    CommunityChestCard("CommunityChestCard"),
    ColorCard(Color.VIOLET, 28, 150, 450,1000,1200,1400, 200, 160),
        
    StationCard(Cardinal.EAST),         
    ChanceCard("ChanceCard"),
    ColorCard(Color.ROSE,   35, 175, 500,1100,1300,1500, 200, 175),
    TaxCard(200),
    ColorCard(Color.ROSE,   50, 200, 600,1400,1700,2000, 200, 200),
    ]

# color monopolized check
def ColorMonopolized(color:Color):
    res = []
    for tile in tiles:
        if type(tile) is ColorCard and tile.colorCode == color:
            res.append(tile)
    owner = res[0].owner
    for t in res:
        if owner != t.owner or t.housesBuilt > 0:
            return False
    return True

# ROLLS 
global cheat
cheat = 0

def Roll6x2():
    a = random.randrange(1,7)
    b = random.randrange(1,7)
    print("Rolled " + str(a) + " + " + str(b))
    return a+b,a==b, a, b

global rol # for company rolls
rol = []
def Rolls(p):
    ct = cheat
    r = rol 
    rolledNum = 0
    for i in range(5):
        r = Roll6x2()
        rolledNum += r[0]
        if r[1]:
            if p.inJail:
                p.inJail = False
            else:
                ct += 1
        else: 
            print(rolledNum)
            return rolledNum
    return 10

# UpdateOutput
def UpdateOutput():
    for t in tiles:
        match t:
            case ColorCard() :
                print("[" + str(tiles.index(t)) + "] " + t.name, t.colorCode.value, str(t.owner))
            case StationCard() :
                print("[" + str(tiles.index(t)) + "] " + t.name, str(t.owner))
            case _:
                print("[" + str(tiles.index(t)) + "] " + t.name)
        if len(t.guests) > 0: 
            s = ""
            for g in t.guests: 
                s += str(g) + ", "
            print("^" + s)

# Bankrupt
def Bankrupt(p:Player):
    print(str(p) + "bankrupt! LOST! DAMOI!")
    players.remove(p)
    tiles[p.tileNumber].RemoveGuest(p)
    for ci in p.cardsOwned:
        if ci > 0: tiles[ci].owner = Bank

# Dialogue
def RunDialogueActions(p:Player):
    p.ShowInfo()
    print("""    ---
    1. End turn
    2. Build a house/hotel
    3. Sell a house/hotel
    4. Mortage
    5. Unmortage
    6. Show Card
    7. Trade Card

    0. Surrender
    ---""")
    userInput = UserIntInputFrom("Type a number from options: \n",[0,1,2,3,4,5,6,7]) # turm
    match userInput:
        case 1: # End turn 
            return
        case 2: # Build a house/hotel
            print("Remember! Every 5 house counts as ONE hotel, and deletes rest houses from card!")
            avilCards = []
            for c in p.cardsOwned:
                if (c > 0 and type(tiles[c]) is ColorCard and tiles[c].housesBuilt < 5 and tiles[c].mortaged == False and ColorMonopolized(tiles[c].colorCode)): avilCards.append(c) 
            if len(avilCards) > 0:
                userInput = UserIntInputFrom("Choose a card to BUILD a house. Avaliable Cards: " + str(avilCards) + "\n", avilCards)
                if p.money >= tiles[userInput].priceHouse:
                    tiles[userInput].BuyHouse()
                    print("House built, -" + str(tiles[userInput].priceHouse))
                else: 
                    print("Not enough money!")
            else: print("No aviliable cards!")
        case 3: # Sell a house/hotel
            print("Remember! Every 5 house counts as ONE hotel, and deletes rest houses from card!")
            avilCards = []
            for c in p.cardsOwned:
                if (c > 0 and type(tiles[c]) is ColorCard and tiles[c].housesBuilt > 0 and ColorMonopolized(tiles[c].colorCode)): avilCards.append(c)
            if len(avilCards) > 0:
                userInput = UserIntInputFrom("Choose a card to SELL a house. Avaliable Cards: " + str(avilCards) + "\n", avilCards)
                tiles[userInput].SellHouse()
                print("House sold for" + str(tiles[userInput].priceHouse))
            else: print("No aviliable cards!")
        case 4: # Mortage            
            print("Remember! If there no cards that you want to mortage - try to sell all houses from it first")
            avilCards = []
            for c in p.cardsOwned:
                if (c > 0 and ((type(tiles[c]) is ColorCard and tiles[c].housesBuilt == 0) or type(tiles[c]) is StationCard) and tiles[c].mortaged == False): avilCards.append(c) 
            if len(avilCards) > 0:
                userInput = UserIntInputFrom("Choose a card to MORTAGE a card. Avaliable Cards: " + str(avilCards) + "\n", avilCards)
                tiles[userInput].MortageCard()
                print("Card mortaged for " + str(tiles[userInput].mortageValue))
            else: print("No aviliable cards!")
        case 5: # Unmortage              
            print("Remember! If there no cards that you want to mortage - try to sell all houses from it first")
            avilCards = []
            for c in p.cardsOwned:
                if (c > 0 and ((type(tiles[c]) is ColorCard and tiles[c].housesBuilt == 0) or type(tiles[c]) is StationCard) and tiles[c].mortaged == True): avilCards.append(c) 
            if len(avilCards) > 0:
                userInput = UserIntInputFrom("Choose a card to MORTAGE a card. Avaliable Cards: " + str(avilCards) + "\n", avilCards)
                tiles[userInput].UnMortageCard()
                print("Card unmortaged for " + str(tiles[userInput].mortageValue) + " + " + str(tiles[userInput].mortageValue)[:-1])
            else: print("No aviliable cards!")
        case 6: # Show Card
            userInput = UserIntInputFrom("Number of tile to show? (0 is Start)\n", list(range(0,40)))
            tiles[userInput].ShowCard()
        case 7: # Trade
            avilCards = []
            for c in p.cardsOwned:
                if (c > 0 and ((type(tiles[c]) is ColorCard and tiles[c].housesBuilt == 0) or type(tiles[c]) is StationCard) and tiles[c].mortaged == False): avilCards.append(c) 
            if len(avilCards) > 0:
                userInput = UserIntInputFrom("Choose a card to TRADE a card. Avaliable Cards: " + str(avilCards) + "\n", avilCards)
                price = UserIntInput("...For price: ")
                plrs = []
                for plyr in players: plrs.append(plyr.playerNumber)
                targetPlayer = UserIntInputFrom("...To Player:", plrs)
                targetInput = UserIntInputFrom("Player (" + str(targetPlayer) + ") do you want to buy Card [" + str(userInput) + "] for " + str(price) + "?\n1. Yes, 2. No: " , [1,2])
                if targetInput == 1: 
                    tiles[userInput].SellCardTo(players[targetPlayer - 1], price)
                    print("Trade Done")
                else:
                    print("Trade Canceled")
            else: print("No aviliable cards!")
        case 0: 
            Bankrupt(p)
            return
        case _:
            print("Input incorrect!")
    RunDialogueActions(p)
# Turn
def Turn(p:Player):
    UpdateOutput()

    print("----------")
    print("TURN OF " + str(p))

    # roll dices
    ###Rolls(p)

    # check tile & run tile func
    p.ShowInfo()
    p.Move(Rolls(p))
    

    # suggest player to do smth

    if p.inJail == False:
        RunDialogueActions(p)
    else:
        return
    # end of turn
    if p.money <= 0: Bankrupt(p)

# game init
global players  
players:List[Player] = []
global winner
winner = None
def GoGame():
    playersCount = UserIntInputFrom("Type number of Players:\n",list(range(2,11)))
    for i in range(playersCount):
        players.append(Player(False, i+1))
        print(players[i])
    while len(players) > 1:
        for p in players:
            Turn(p)
    print("************************************************")
    print(str(players[0]) + " WINNER!!!")
    print("************************************************")
GoGame()