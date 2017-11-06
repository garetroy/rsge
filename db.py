"""
    db.py
    Author: Garett Roberts

    This program is for modifying the database within the osrsge program.
    Uses mongodb to store,query, and remove data.
"""
from pymongo import MongoClient

class DB:
    """
        A database class for our program.
    """

    def __init__(self,ip="localhost",port=27017):
        """
            Connects to database and prepares collections
    
            @param:
                ip <string> - The ip address of the mongodb 
                port <int>  - The port number of the mongodb
        """
        #need error checking here
        self.client     = MongoClient(ip,port)
        self.database   = self.client.osrsge 
        self.catalogue  = self.database.catalogue
        self.items      = self.database.items

    def insertCatalogueItem(self,catalogueitem):
        """
            This method takes a catalouge item and inserts it into
            the catalogues collection.

            @param:
                catalogueitem <dict> - A dictonary representing a catelog item

            @returns:
                <int> - returns -1 if failed to insert item
                                 0 on success
                                 1 on already existing

            Ex of catalogueitem:
                The catalouge item must look similar to this format
                {"pagenum":<int>,catalogue:{
                    "types":[],"alpha":[{"letter":<char>,"items":<int>}]
                }}
        """
        if catalogueitem == {}:
            #insert print statement
            return -1 
        

        alpha = temp["catalogue"]["alpha"]
        for itemidx in range(len(alpha)):
            item = {
                    "_id"      : itemidx,
                    "pagenum"  : temp["pagenum"],
                    "letter"   : alpha[itemidx]["letter"],
                    "numitems" : alpha[itemidx]["items"]
            }

            #error checking
            self.catalogue.insert_one(item)

        return 0

    def insertCatalogueItems(self):
        pass
    
    def insertItem(self,itemdict):
        """
            Takes an itemdict and inserts it into the items collection.

            @param:
                itemdict <dict> - A dictionary representing a runescape item

            @returns:
                <int> - returns -1 if failed to insert item
                                 0 on success
                                 1 on already existing

            Ex of itemdict:
                {"id":<int>, "name":<string>, "members":<bool>,
                    "today":<string>, "date":<string> FMT:"00/00/000"}
        """

        if itemdict == {}:
        #insert print statment
            return -1

        item = {
                "_id"     : itemdict["id"],
                "name"    : itemdict["name"],
                "members" : itemdict["members"],
                "today"   : itemdict["today"],
                "dateacc" : itemdict["date"]
        }

        #error checking
        self.items.insert_one(item)

        return 0
        
    def insertItems(self):
        pass

    def removeCatalogueItem(self,queryitem):
        """
            Removes the given queryitem from catalogue collection
    
            @param:
                queryitem <dict> - Some info to query our database with
            
            @returns:
                <int> - returns -1 on failure, 
                                 0 on success,
                                 1 on non-existant/could'nt find item
                                 2 on finding more than one entry
        """
        #error check
        self.catalogue.remove(queryitem) 
        return 0

    def removeCatalogueItems(self):
        pass
    
    def removeItem(self,queryitem):
        """
            Removes the given queryitem from catalogue collection
    
            @param:
                queryitem <dict> - Some info to query our database with
            
            @returns:
                <int> - returns -1 on failure, 
                                 0 on success,
                                 1 on non-existant/could'nt find item
                                 2 on finding more than one entry
        """
        #error check
        self.items.remove(queryitem)
        return 0
    
    def removeItems(self):
        pass

    def catalogueQuery(self,queryitem):
        """
            This function returns a list of items that match items in 
            the catalogue

            @param:
                queryitem <dict> - Some info to query our database with
            
            @returns:
                <list> - [] on failure, else a populated dictonary
        """        
        #error check
        query = self.catalogue.find(queryitem)

        if query.count() == 0:
            return []
        else:
            return [item for item in query]
            
    def itemQuery(self,queryitem):
        """
            Returns a list of items that match the queryitem in the item 
            collection

            @param:
                queryitem <dict> - Some info to query our database with

            @returns:
                <list> - [] on failure, else a populated dictionary
        """
        #error check
        query = self.items.find(queryitem)

        if query.count() == 0:
            return []
        else:
            return [item for item in query]

    def gatherAllItemsByDate(self):
        pass

    def clearCatalogue(self):
        """
            Drops catalogue from table
        """
        #needs error checking.. (already gone, sucessful?)
        self.catalogue.drop()
    
    def clearItems(self):
        """
            Drops items from table
        """
        #error checking
        self.items.drop()

if __name__ == '__main__':
    temp = {"pagenum":0, "catalogue":{"types":[],"alpha":[{"letter":"#",
            "items":0},{"letter":"a","items":6},{"letter":"b","items":8},
            {"letter":"c","items":1},{"letter":"d","items":3}]}}

    db = DB()
    db.clearCatalogue()
    db.insertCatalogueItem(temp)
    print(db.catalogueQuery({"letter":"d"}))
    db.removeCatalogueItem({"letter":"c"})  
    db.clearItems()
    db.insertItem({"id":1,"name":"dog","members":True,"today":"1","date":"00/00/0000"})
    db.insertItem({"id":3,"name":"dog","members":True,"today":"1","date":"00/00/0020"})
    db.insertItem({"id":2,"name":"dog","members":False,"today":"1","date":"00/00/0020"})
    db.removeItem({"_id":1})
