"""
    threadpool.py
    Author: Garett Roberts

    A basic thread pool
"""
from threading import Thread
from queue     import Queue

class ThreadPool:
    """
        A threadpool class
    """
    def __init__(self,maxthreads):
        """
            Creates a queue and initializes the threadpool.

            @params:
                maxthreads (int) - The max amount of threads we want to run
        """
        self.threads     = []
        self.maxthreads  = maxthreads
        self.currthreads = 0
        self.queue       = Queue()
        self.alive       = True

    def queueWorkers(self,work,param):
        """
            Queues workers and it's parameters
            
            @param:
                work (function) - A function
                param (any)     - Functions paramaters
        """
        self.queue.put([work,param])

    def runPool(self):
        """
            Takes items from the queue and creates a thread, if no
            threads are available checks for live threads
        """
        while self.alive:
            if self.queue.empty() or self.currthreads == self.maxthreads:
                self.checkThreads()
                continue 

            self.currthreads += 1
            popped = self.queue.get()
            thread = Thread(target=popped[0],args=(popped[1],))
            self.threads.append(thread)
            thread.start()

    def checkThreads(self):
        """
            Checks if any thread has died, if so updates the class info
        """
        for thread in self.threads:
            if not thread.isAlive():
                self.currthreads -= 1 
                self.threads.remove(thread)

    def closePool(self):
        """
            Closes the pool by stopping the runPool and clears queue
        """
        self.alive = False

        if self.queue.empty() and len(self.threads) == 0:
            return True

        while not self.queue.empty():
            self.queue.get()

        for i in self.threads:
            i.join()
        
        return True  
