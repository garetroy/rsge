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
        
        self.socket = self.createSocket()

    def createSocket(self):
        """
            Creates the client sockets

            @returns:
                (socket.socket) - A socket we create
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error as err:
            print("Sockets couldn't be created {}".format(err)) 

        return s

    def serverConnection(self):
        """
            Forever waits for a servers conenctions, then its message
            containing a string with corresponding id numbers for items
            
            Msg Example: 
                b'2 6'
        """
        while True:
            try:
                self.socket = self.createSocket()
                self.socket.connect((self.serverip,self.serverport))
                self.startScraping(self.socket.recv(2048).decode("utf-8"))
                #needs to send a done signal
                self.socket.close()
            except socket.error as err:
                print("Socket exception caught {}".format(err))
                time.sleep(1)
                continue

    def startScraping(self,ids): 
        """
            Recieves a string with corresponding item ids then scrapes
            one by one for them, then sends the items to the server
            
            @params:
                ids (int) - A integer spaced string containing item ids
        """
        idlist = ids.split(" ")
        for itemid in idlist:
            item = self.getItem(int(itemid))
            self.socket.sendall(json.dumps(item).encode("utf-8"))
            time.sleep(5)
