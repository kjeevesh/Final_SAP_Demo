import os
import time
import sched
import threading


class SAP_Scheduler(object):
    _instance = None

    def __new__(cls, *args, **kwargs):

        if cls._instance is None:
            cls._instance = super(SAP_Scheduler, cls).__new__(cls)

            cls.s = sched.scheduler(time.time, time.sleep)
            cls.start = time.time()
            cls.e = threading.Event()
            cls._stop = threading.Event()
        return cls._instance

    def get_scheduler(self):
        return self._instance

    def addControl(self, control):
        """Add a new task to the scheduler."""
        #self.s.enter(delay, 1, task, argument=args, kwargs={'start': self.start})
        #print(control.task)
        self.s.enterabs(control.start_time, 1, control.task, argument=control.argments, kwargs=control.kwargs)
        self.e.set()

    def listAllTasks(self):
        """list all tasks"""
        print(self.s.queue)
        return self.s.queue

    def stop(self):
        """Stop the scheduler."""
        self._stop.set()
        self.e.set()

    def rmTask(self, arg):
        """Remove a task from the scheduler."""
        for event in self.s.queue:
            if event.argument[0] == arg:
                self.s.cancel(event)

    def run(self):
        """Executes the main loop of the scheduler.
        This is to be executed in a new thread."""
        max_wait = None
        while not self._stop.is_set():
            self.e.wait(max_wait)
            self.e.clear()
            max_wait = self.s.run(blocking=False)


class Control(object):

    def __init__(self, start_time, task, args, kwargs):
        self.start_time = start_time
        self.task = task
        self.argments = args
        self.kwargs = kwargs