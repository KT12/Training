#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 23:01:34 2017

@author: kt12
"""
# Reversed

""" If there is no __reversed__ function, Python will call __len__ and
    __getitem__ which are used to define a sequence 
"""

normal_list = [1,2,3,4,5]

class CustomSequence():
    def __len__(self):
        return 5
    
    def __getitem__(self, index):
        return "x{0}".format(index)

class FunkyBackwards():
    def __reversed__(self):
        return "BACKWARDS!"

for seq in normal_list, CustomSequence(), FunkyBackwards():
    print("\n{}: ".format(seq.__class__.__name__), end="")
    for item in reversed(seq):
        print(item, end=", ")

# Enumerate

import sys
filename = sys.argv[1]

with open(filename) as file:
    for index, line in enumerate(file):
        print("{0}: {1}".format(index+1, line), end='')
        

# Context manager
""" __enter__ and __exit__ turn file object into a context manager
"""

class StringJoiner(list):
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, tb):
        self.result = ''.join(self)
        
import random, string

with StringJoiner() as joiner:
    for i in range(15):
        joiner.append(random.choice(string.ascii_letters))
    
    
print(joiner.result)

# Default arguments

""" Default arguments are evaluated when the function is first interpreted,
    not when it is called"""
    
number = 5
def funky_function(number=number):
    print(number)
    
number = 6
funky_function(8)
funky_function()
print(number)

""" Default arguments are tricky with empty containers such as lists etc """

def hello(b=[]):
    b.append('a')
    print(b)

# Variable argument lists

def get_pages(*links):
    for link in links:
        # download the link with urllib
        print(link)
        
# kwargs are frequently used in configuration setups

class Options:
    default_options = {
            'port': 21,
            'host': 'localhost',
            'username': None,
            'password': None,
            'debug': False,
            }
    
    def __init__(self, **kwargs):
        self.options = dict(Options.default_options)
        self.options.update(kwargs)
    
    def __getitem__(self, key):
        return self.options[key]

options = Options(username='dusty', pasword='drowssap', debug=True)

options['debug']
options['port']
options['username']


import shutil
import os.path
def augmented_move(target_folder, *filenames,
                   verbose=False, **specific):
    """Move all filenames into the target_folder, allowing
    specific treatment of certain files."""
    
    def print_verbose(message, filename):
        """print the mesage only if verbose is enabled"""
        if verbose:
            print(message.fomat(filename))
    
    for filename in filenames:
        target_path = os.path.join(target_folder, filename)
        if filename in specific:
            if specific[filename] == 'ignore':
                print_verbose("Ignoring {0}", filename)
            elif specific[filename] == 'copy':
                print_verbose("Copying {0}", filename)
                shutil.copyfile(filename, target_path)
        else:
            print_verbose("Moving {0}", filename)
            shutil.move(filename, target_path)
    

# Unpacking arguments

def show_args(arg1, arg2, arg3="THREE"):
    print(arg1, arg2, arg3)

some_args = range(3)

more_args = {
        "arg1": "ONE",
        "arg2": "TWO"}

print("Unpacking a sequence:", end=" ")
show_args(*some_args)

print("Unpacking a dict:", end=" ")
show_args(**more_args)



# Functions are objects too

def my_function():
    print("The Function Was Called")
my_function.description = 'A silly function'

def second_function():
    print("The second was called")
second_function.description = "A sillier function."

def another_function(function):
    print("The description:", end=" ")
    print(function.description)
    print("The name:", end=" ")
    print(function.__name__)
    print("The class:", end=" ")
    print(function.__class__)
    print("Now I'll call the function passed in")
    function()
    
another_function(my_function)
another_function(second_function)


# Event driven timer

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

# Set of callbacks to test the timer

# Need to be in the correct directory to use timer.py

from timer import Timer
import datetime

def format_time(message, *args):
    now = datetime.datetime.now().strftime("%I:%M:%S")
    print(message.format(*args, now=now))

def one(timer):
    format_time("{now}: Called One")

def two(timer):
    format_time("{now}: Called Two")

def three(timer):
    format_time("{now}: Called Three")

class Repeater:
    def __init__(self):
        self.count = 0
        
    def repeater(self, timer):
        format_time("{now}: repeat {0}", self.count)
        self.count += 1
        timer.call_after(5, self.repeater)
        

timer = Timer()
timer.call_after(1, one)
timer.call_after(2, one)
timer.call_after(2, two)
timer.call_after(4, two)
timer.call_after(3, three)
timer.call_after(6, three)
repeater = Repeater()
timer.call_after(5, repeater.repeater)
format_time("{now}: Starting")
timer.run()

# Using functions as attributes

# Make Repeater callable

""" Only implement the __call__ function on an object if the object is 
    meant to be treated like a function """
    
class Repeater:
    def __init__(self):
        self.count = 0
    
    def __call__(self, timer):
        format_time("{now}: repeat {0}", self.count)
        self.count += 1
        
        timer.call_after(5, self)

timer = Timer()
timer.call_after(5, Repeater())
format_time("{now}: Starting")
timer.run()

# Mailing list manager

import smtplib
from email.mime.text import MIMEText

def send_email(subject, message, from_addr, *to_addrs,
        host='localhost', port=1025, headers=None):
    
    headers = {} if headers is None else headers
    email = MIMEText(message)
    email['Subject'] = subject
    email['From'] = from_addr
    for header, value in headers.items():
        email[header] = value
    
    sender = smtplib.SMTP(host, port)
    for addr in to_addrs:
        del email['To']
        email['To'] = addr
        sender.sendmail(from_addr, addr, email.as_string())
    sender.quit()

send_email("A model subject", "The message contents",
"from@example.com", "to1@example.com", "to2@example.com")

# Email gropu mgmt system
# Store email addresses in a set container

from collections import defaultdict

class MailingList:
    '''Manage groups of email addresses for sending emails'''
    def __init__(self, data_file):
        self.email_map = defaultdict(set)
        self.data_file = data_file
        
    def add_to_group(self, email, group):
        self.email_map[email].add(group)
    
    def emails_in_group(self, *groups):
        groups = set(groups)
        emails = set()
        for e, g in self.email_map.items():
            if g & groups: # short for g.intersection(groups)
                emalis.add(e)
        return emails

    def send_mailing(self, subject, message, from_addr,
                     *groups, headers=None):
        emails = self.emails_in_group(*groups)
        send_email(subject, message, from_addr,
                   *emails, headers=headers)
        
    # Save emails to data
    def save(self):
        with open(self.data_file, 'w') as file:
            for email, groups in self.email_map.items():
                file.write(
                        '{} {}\n'.format(email, ','.join(groups))
                        )
    
    def load(self):
        self.email_map = defaultdict(set)
        try:
            with open(self.data_file) as file:
                for line in file:
                    email, groups = line.strip().split(' ')
                    groups = set(groups.split(','))
                    self.email_map[email] = groups
        except IOError:
            pass
    
    # Support context manager
    def __enter__(self):
        self.load()
        return self
    
    def __exit__(self):
        self.save()