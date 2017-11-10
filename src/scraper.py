import json,time,os.path,math
from urllib.request import urlopen
from datetime       import date
from rsitem         import RSItem
from os             import remove

    
def Scraper:
        
    def __init__(self):
        self.categoryurl  ="http://services.runescape.com/m=itemdb_oldschool" + \
            "/api/catalogue/category.json?category=" 
        self.itemgraburl = "http://services.runescape.com/m=itemdb_oldschool" + \
            "/api/catalogue/items.json?category="
        self.itemdetail  = "http://services.runescape.com/m=itemdb_oldschool" + \
            "/api/catalogue/detail.json?item="
        self.quantityurl = "http://api.rsbuddy.com/grandExchange?a=guidePric" + \
            "e&i="
 
    def createItemUrl(self,category,letter,page):
        pass

    def getCategory(self):
        pass

    def getCategories(self):
        pass 

    def getItems(self):
        pass

    def getItem(self):
        pass
