"""
    engine.py
    Author: Garett Roberts

    This is the driving force for the program. Gets inputs from the clients
    and adds things to databases
"""
import json, time
from queue            import Queue
from scraperreciever  import ScraperR
from db               import DB
from threadpool       import ThreadPool

class Engine:
    """
        An engine class
    """
    def __init__(self):
        """
            Loads configuration, queue, db, and threadpool
        """
        self.db = DB()

        try:
            with open("../config/server-clients.json") as jsonf:
                self.cinfo = json.load(jsonf) 
                print(self.cinfo)
        except:
            print("Could not find/load server-clients.json config file")
            exit()

        self.clients = self.cinfo["clients"] 
        self.nodenum = len(self.clients)
        self.queue   = Queue()
        self.alive   = True
        self.tp      = ThreadPool(self.nodenum+1)

    def databaseWork(self,dummy=None):
        """
            This adds responses from the clients to the db
            
            @param:
                dummy <None> - This is to conform to threadpool
        """
        while self.alive:
            if self.queue.empty():
                continue 
            
            items = []
            count = 0
            while not self.queue.empty() and count != 6:
                items.append(self.queue.get())
                count += 1
            
            self.db.insertItems(items)
           
            time.sleep(5) 

    def serverWork(self,info):
        """
            This is the work that the server does for each
            client. Connects to those clients and adds items to the queues.
            
            @param:
                info - <list> first element is client info
                        <list> second element is for the divied up work         
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((info[0]['ip'],info[0]['port']))
        s.listen(1)
        
        data = " ".join(str(i) for i in info[1]).encode('utf-8')
        conn.sendall(data)
        self.queue.put(data.decode('utf-8'))

        while self.alive:
            try:
                data = conn.recv(2048)
                #if client done, die
                self.queue.put(json.loads(data))
            except:
                #Client is no longer alive
                return

    def Start(self):
        """
            This starts the engine, adds all the needed work to the threadpool
            and then executes the threadpool. (divies up work)
        """
        self.tp.queueWorkers(self.databaseWork,None) 
        #needs to divy up work
