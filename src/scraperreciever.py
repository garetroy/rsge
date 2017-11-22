"""
    scraperreciever.py
    Author: Garett Roberts

    This program inhearets from scraper.py and will connect to the main server
    recieving info from the server on which items to scrape from the osrs
    ge
""" 
import json,time,socket
from urllib.request import urlopen
from scraper import Scraper

class ScraperR(Scraper):
    """
        The ScraperR class which is a chile of the Scraper class
    """
    
    def __init__(self):
        """
            Initially in this function we open up the config file,
            then get the serverip and port from the config file.
        """
        Scraper.__init__(self)
        
        try:
            with open("../config/server-clients.json") as jsonf:
                self.cinfo = json.load(jsonf) 
        except:
            print("Could not find/load server-clients.json config file")
            exit()

        try:
            self.serverip   = self.cinfo["serverip"]
            self.serverport = self.cinfo["serverport"]
        except:
            print("server-clients config file not properly formatted")
            exit()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host   = socket.gethostname()

    def serverConnection(self):
        #Wait for connection/while connected.
        while True:
            try:
                self.socket.connect(("localhost",9999))
                itemids = json.loads(self.socket.recv(2048))
                print(itemids)
                exit()
                startScraping(itemids)
            except:
                continue

    def startScraping(self,ids): 
        #Get Item ID
        #Send to server
            #if unsucessful, return
        #wait 5 seconds for next scrape
        pass
