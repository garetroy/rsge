"""
    db.py
    Author: Garett Roberts

    This program is for modifying the database within the osrsge program.
    Uses mongodb to store,query, and remove data.
"""
from pymongo import MongoClient, errors

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
        self.client     = MongoClient(ip,port)

        try:
            self.client.server_info() 
            print("Connected to db successfully")
        except errors.ConnectionFailure:
            raise Exception(\
                "Could not connect to mongodb at address: {} port: {}"\
                .format(ip,port))
            
        self.database   = self.client.osrsge 
        self.items      = self.database.items

    def insertItem(self,itemdict={}):
        """
            Takes an itemdict and inserts it into the items collection.

            @param:
                itemdict <dict> - A dictionary representing a runescape item

            @returns:
                <int> - returns -1 if failed to insert item
                                 0 on success

            Ex of itemdict:
                {"id":<int>, "name":<string>, "members":<bool>,
                    "today":<string>, "date":<string> FMT:"00/00/000"}
        """
        if itemdict == {}:
            print("itemdict in insertItem was empty")
            return -1

        item = {
                "_id"     : itemdict["id"],
                "name"    : itemdict["name"],
                "members" : itemdict["members"],
                "today"   : itemdict["today"],
                "dateacc" : itemdict["date"]
        }

        try:
            self.items.insert_one(item)
        except(errors.WriteError, errors.WriteConcernError) as e:
            print("Write error in insertItem: {}".format(e))
            print("catalogueitem = {}".format(item))
            return -1

        return 0
        
    def insertItems(self, itemdicts):
        """
            Inserts multiple catalogue entries.

            @param:
                itemdicts <list<dict>> - A list of dictionary items 
                    representing rs items

            @returns
                <int> - returns -1 on failure
                                 0 on sucess
        """
        if len(itemdicts) == 0:
            print("itemdicts in insertItems was empty")
            return -1

        #make threaded
        for i in itemdicts:
            if(self.insertItem(i) == -1):
                print("insertItems failed")
                return -1
        return 0



    def removeItem(self,queryitem):
        """
            Removes the given queryitem from catalogue collection
    
            @param:
                queryitem <dict> - Some info to query our database with
            
            @returns:
                <int> - returns -1 on failure, 
                                 0 on success,
        """
        try:
            self.items.remove(queryitem)
        except:
            print("Could not remove queryitem {} in removeItem"\
                .format(queryitem))
            return -1

        return 0
    
    def removeItems(self, queryitems):
        """
            Removes the given rs items from the item collection 

            @param:
                queryitems <list<dict>> - List of items represented as dicts

            @returns:
                <int> - returns -1 on failure,
                                 0 on success,
        """
        if len(queryitems) == 0:
            print("queryitems in removeItems was empty")
            return -1        

        #needs threading
        for i in queryitems:
            if(self.removeItem(i) == -1):
                print("removeItems failed")
                return -1
        return 0

    def itemQuery(self,queryitem):
        """
            Returns a list of items that match the queryitem in the item 
            collection

            @param:
                queryitem <dict> - Some info to query our database with

            @returns:
                <list> - [] on failure (or not found), 
                        else a populated dictionary
        """
        try:
            query = self.items.find(queryitem)
        except:
            print("Query faild for {} in itemQuery".format(queryitem))
            return []

        if query.count() == 0:
            return []
        else:
            return [item for item in query]

    def gatherAllItemsByDate(self,datestring):
        """
            Queryies all items that were updated on the given date

            @params:
                datestring <string> - A datestring represented as MM/DD/YYYY
            
            @returns:
                <list<dict>> A list of items represented as dicts 
                            [] on failure (or could not find)
        """
        try:
            query = self.items.find({"dateacc":datestring}) 
        except:
            print("Query failed for {} in gatherAllItemsByDate"\
                    .format(datestring))
            return []
    
        if query.count() == 0:
            return []
        else:
            return [item for item in query]

    def getItemColSize(self):
        """
            Returns the size of the Items collection

            @returns:
                <int>
                -1 if error
                size of collection otherwise
        """
        try:
            return self.items.count()
        except:
            print("Error getting collection size in getItemColSize")
            return -1

    def clearItems(self):
        """
            Drops items from table

            @returns 
                True - if successfully drops collection
                False - if unsucessful (collection dosen't exist)
        """
        try:
            self.items.drop()
            return True
        except:
            print("clearItems failed!")
            return False
