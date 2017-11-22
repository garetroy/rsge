"""
    scraper.py

    This program is for scraping the osrs api.  
"""
import json,time,os.path,math
from urllib.request import urlopen
from datetime       import date
from os             import remove
    
class Scraper:
    """
        A scraper class for the program
    """
        
    def __init__(self):
        """
            Creates the links we need for scraping
        """
        #For grabbing an item from an item id
        self.itemdetail  = "http://services.runescape.com/m=itemdb_rs/api/"+\
            "catalogue/detail.json?item="
 
    def getItem(self,idnum):
        """
            Grabs the items from the given idnum

            @param:
                idnum (int) - idnum of the item we want

            @returns:
                (dict) - A dictionary representing a json request
                        Empty if failed
        """

        if type(idnum) != int:
            print("idnum must be of type int in getItem")
            return {}

        try:
            url  = self.itemdetail + str(idnum)
            resp = urlopen(url) #add to parallelizer
            cont = json.loads(resp.read())
            return cont['item']
        except:
            print("Could not find id {} in getItem".format(idnum))
            return {}
