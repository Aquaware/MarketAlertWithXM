import datetime
import threading
import time as pyTime


def today():
    return datetime.datetime.today()

def yesterday():
    return today() - datetime.timedelta(days= 1)

def tomorrow():
    return today() + datetime.timedelta(days= 1)

class Scheduler():

    def __init__(self, interval_sec):
        self.interval_sec = interval_sec
        self.is_active = False
        self.limit = 500
        
        
    def debug(self, callback, debug_callback):
        self.debug_callback = debug_callback
        self.run(callback)
        
    def run(self, callback):
        if self.is_active:
            return
        self.callback = callback
        self.is_active = True
        self.counter = 0
        t = threading.Timer(self.interval_sec, self.worker)
        t.start()
        pass

    def isActive(self):
        now = today()
        t1 = datetime.datetime(now.year, now.month, now.day, 5, 31)
        t2 = datetime.datetime(now.year, now.month, now.day, 8, 00)
        if now >= t1 and now <= t2:
            return False

        t3 = datetime.datetime(now.year, now.month, now.day, 15, 16)
        t4 = datetime.datetime(now.year, now.month, now.day, 16, 00)
        if now >= t3 and now <= t4:
            return False
        return True

    def worker(self):
        self.counter += 1
        if self.counter > self.limit:
            self.is_active = False
            print('<<<< Debug End >>>>')
            self.debug_callback()
            
        if self.is_active:
            self.callback()
            t = threading.Timer(self.interval_sec, self.worker)
            t.start()
        return
    
    def stop(self):
        self.is_active = False
        
        