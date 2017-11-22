from db import DB

class ThreadedDB(DB):

    def __init__(self,ip="localhost",port=27017):
        DB.__init__(self,ip,port) 

    def insertItems(self, itemdicts):
        pass

    def removeItems(self, queryitems):
        pass
