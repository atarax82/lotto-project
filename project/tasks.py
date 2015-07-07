'''
This module defines task using sched module that should be done repeatedly.
'''
import time
import sched
import threading
from project.apps.lotto.utils import tickets as tickets_util


def check_tickets():
    s = sched.scheduler(time.time, time.sleep)
    check_delay = 60*60 # every hour
        
    def perform_check_tickets():
        # using try to prevent thread from stopping
        try:
            tickets_util.check_tickets()
        except:
            # ideally, we should log our exception here
            pass
        
        s.enter(check_delay, 1, perform_check_tickets, ())
        
    s.enter(check_delay, 1, perform_check_tickets, ())
    s.run()

def run():
    # we use separate thread to run our task
    threading.Thread(target=check_tickets).start()
    
