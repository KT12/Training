#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 20:46:59 2017

@author: kt12
"""

import datetime
import time

class TimedEvent:
    def __init__(self, endtime, callback):
        self.endtime = endtime
        self.callback = callback
        
    def ready(self):
        return self.endtime <= datetime.datetime.now()

class Timer:
    def __init__(self):
        self.events = []
        
    def call_after(self, delay, callback):
        end_time = datetime.datetime.now() + \
            datetime.timedelta(seconds=delay)
        
        self.events.append(TimedEvent(end_time, callback))
        
    def run(self):
        while True:
            ready_events = (e for e in self.events if e.ready())
            for event in ready_events:
                event.callback(self)
                self.events.remove(event)
            time.sleep(0.5)
