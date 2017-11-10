import json,time,os.path,math
from urllib.request import urlopen
from datetime       import date
from rsitem         import RSItem
from os             import remove

    
def Scraper:
        
    def __init__(self):
        self.categoryurl = "http://services.runescape.com/m=itemdb_oldschool"+\
            "/api/catalogue/category.json?category=" 
        self.itemgraburl = "http://services.runescape.com/m=itemdb_oldschool"+\
            "/api/catalogue/items.json?category="
        self.itemdetail  = "http://services.runescape.com/m=itemdb_rs/api/"+\
            "catalogue/detail.json?item="
 
    def getCategory(self,catID):
        if type(catID) != int:
            print("catID must be of type int in getCategory")
            return {}

        try:
            url  = self.categoryurl + str(catID)
            resp = urlopen(url) #add to parallelizer
            cont = json.loads(resp.read())
            return cont
        except:
            print("Couldn't find category {} in getCategory".format(catID))
            return {} #Couldn't find page
        
    def getAllCategories(self):
        #needs error checking
        categories = []
        
        #For threading here... Might be a good idea to 
        #push each url request to the parallelizer so it can
        #handle wait times

        for catID in range(1,38):
            time.sleep(5) #Temporary, will be done by parallelizer
            try:
                url  = self.categoryurl+str(catID)
                resp = urlopen(url) #goes to parallelizer, add categories
                cont = json.loads(resp.read())

                categories.append(cont) 
            except: #Found the end of the categories
                return categories

    def getItem(self,idnum):
        if type(idnum) != int:
            print("idnum must be of type int in getItem")
            return {}

        try:
            url  = self.itemdetail + str(idnum)
            resp = urlopen(url) #add to parallelizer
            cont = json.loads(resp.read())
            return cont
        except:
            print("Could not find id {} in getItem".format(idnum))
            return {}

    def getItems(self):
        pass

