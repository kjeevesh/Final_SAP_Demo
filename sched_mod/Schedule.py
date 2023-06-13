from sched_mod.SAP_Scheduler import *
import threading
import time
from threading import Thread

class Schedule(object):

    def __init__(self, start_time, interval, sapcontrols):
        self.start_time = start_time
        self.interval = interval
        self.sapcontrols = sapcontrols
        self.scheduler = SAP_Scheduler()

    def run(self):

        scheduled_interval_abs_time = self.start_time
        loop_thread = threading.Thread(target=self.scheduler.run)
        loop_thread.daemon = True
        loop_thread.setDaemon(True)
        loop_thread.start()

        while True:
            print("********************************")
            #print(self.sapcontrols)
            for control in self.sapcontrols:
                self.scheduler.addControl(Control(scheduled_interval_abs_time, control.func, control.argset, control.controldict))
            
            print("********************************")
            scheduled_interval_abs_time += self.interval

            # sleeptime should always be leass than the interval
            time.sleep(5)

        loop_thread.join()



class SapControl(object):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.argset = args
        self.controldict = kwargs


