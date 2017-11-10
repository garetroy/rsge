from db import DB

temp = {"pagenum":0, "catalogue":{"types":[],"alpha":[{"letter":"#",
            "items":0},{"letter":"a","items":6},{"letter":"b","items":8},
            {"letter":"c","items":1},{"letter":"d","items":3}]}}

temp2 = {"pagenum":1, "catalogue":{"types":[],"alpha":[{"letter":"#",
            "items":0},{"letter":"a","items":6},{"letter":"b","items":8},
            {"letter":"c","items":1},{"letter":"d","items":3}]}}

temp3 = {"pagenum":2, "catalogue":{"types":[],"alpha":[{"letter":"#",
            "items":0},{"letter":"a","items":6},{"letter":"b","items":8},
            {"letter":"c","items":1},{"letter":"d","items":3}]}}

try:
    db = DB()
except:
    print("Could not create db")
    exit()

assert (db.clearCatalogue() == True),"Collection didn't exist!"
assert (db.insertCatalogueItems([temp2,temp3,temp]) == 0),\
         "Couldn't insert item in catalogue"

assert (db.catalogueQuery({"pagenum":0, "letter":"d"}) ==\
        [{'_id': 15, 'pagenum': 0, 'letter': 'd', 'numitems': 3}]),\
        "Couldn't find correct item in catalogueQuery"

assert (db.removeCatalogueItems([{"letter":"c"}]) == 0), "Wrongful remove from" \
            + " Catalogue"

assert (db.getCatalogueColSize() == 12), "Catalogue size is incorrect"

assert (db.clearItems() == True),"Collection didn't exist!"

item  = {"id":1,"name":"dog","members":True,"today":"1","date":"00/00/0000"}
item2 = {"id":3,"name":"dog","members":True,"today":"1","date":"00/00/0020"}
item3 = {"id":2,"name":"dog","members":False,"today":"1","date":"00/00/0020"}

assert (db.insertItems([item,item2,item3]) == 0),\
        "Couldn't insert item into items collection"

assert (db.itemQuery({"members":False}) == 
    [{'_id': 2, 'name': 'dog', 'members': False, 'today': '1', 'dateacc':\
     '00/00/0020'}]), "Bad item query"

desiredresult = [{'_id': 3, 'name': 'dog', 'members': True, 'today': '1',\
     'dateacc': '00/00/0020'}, {'_id': 2, 'name': 'dog', 'members': False,\
     'today': '1', 'dateacc': '00/00/0020'}]

assert (db.gatherAllItemsByDate("00/00/0020")  == desiredresult), "Bad gather"

assert (db.removeItems([{"name":"dog"}]) == 0), "Wrongful remove from"\
            + " Items collection"

assert (db.getItemColSize() == 0), "Item collection size is incorrect"

print("DB Testing is correctly working")
