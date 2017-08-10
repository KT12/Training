#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 00:07:00 2017

@author: kt12
"""

''' __iter__ and __next__ needed to make an iterator '''

class CapitalIterable:
    def __init__(self, string):
        self.string = string
    
    def __iter__(self):
        return CapitalIterator(self.string)
    
class CapitalIterator:
    def __init__(self, string):
        self.words = [w.capitalize() for w in string.split()]
        self.index = 0
    
    def __next__(self):
        if self.index == len(self.words):
            raise StopIteration()
        
        word = self.words[self.index]
        self.index += 1
        return word
    
    def __iter__(self):
        return self

iterable = CapitalIterable('the quick brown fox jumps over the lazy \
dog')
iterator = iter(iterable)

while True:
    try:
        print(next(iterator))
    except StopIteration:
        break

# List comp
input_strings = ['1', '5', '28', '131', '3']
output_itegers = [int(n) for n in input_strings]
output_ints = [int(n) for n in input_strings if len(n) < 3]


# List Comps

import sys
filename = sys.argv[1]

with open (filename) as file:
    header = file.readline().strip().split('\t')
    contacts = [
            dict(
                    zip(header, line.strip().split('\t'))
                    ) for line in file
            ]
    
    for contact in contacts:
        print("email: {email} -- {last}, {first}".format(**contact))

# Set and dict comps

from collections import namedtuple

Book = namedtuple("Book", "author title genre")

books = [
        Book('Pratchett', 'Nightwatch', 'fantasy'),
        Book('Pratchett', 'Thief of Time', 'fantasy'),
        Book('Le Guin', 'The Dispossessed', 'scifi'),
        Book('Le Guin', 'A Wizard of Earthsea', 'fantasy'),
        Book('Turner', 'The Thief', 'fantasy'),
        Book('Phillips', 'Preston Diamond', 'western'),
        Book('Phillips', 'Twice Upon A Time', 'scifi'),
        ]

fantasy_authors = {
        b.author for b in books if b.genre == 'fantasy'}

fantasy_titles = {
        b.title: b for b in books if b.genre == 'fantasy'}

# Generator expressions
import sys
inname = sys.argv[1]
outname = sys.argv[2]

with open(inname) as infile:
     with open(outname, 'w') as outfile:
         warnings = (l for l in infile if 'WARNING' in l)
         for l in warnings:
             outfile.write(l)
             
# Generators save memory and should be used wherever possible
# use yield()

import sys
inname, outname = sys.argv[1:3]

def warnings_filter(insequence):
    for l in insequence:
        if 'WARNING' in l:
            yield l.replace('\tWARNING', '')

with open(inname) as infile:
    with open(outname, 'w') as outfile:
        filter = warnings_filter(infile)
        for l in filter:
            outfile.write(l)

# Yield items from another iterable

import sys
inname, outname = sys.argv[1]

def warnings_filter(infilename):
    with open(infilename) as infile:
        yield from (
                l.replace('\tWARNING', '')
                for l in infile
                if 'WARNING' in l
                )

filter = warnings_filter(inname)
with open(outname, 'w') as outfile:
    for l in filter:
        outfile.write(l)

# Use yield to walk a file tree

class File:
    def __init__(self, name):
        self.name = name

class Folder(File):
    def __init__(self, name):
        super().__init__(name)
        self.children = []

root = Folder('')
etc = Folder('etc')
root.children.append(etc)
etc.children.append(File('passwd'))
etc.children.append(File('groups'))
httpd = Folder('httpd')
etc.children.append(httpd)
httpd.children.append(File('http.conf'))
var = Folder('var')
root.children.append(var)
log = Folder('log')
var.children.append(log)
log.children.append(File('messages'))
log.children.append(File('kernel'))


def walk(file):
    if isinstance(file, Folder):
        yield file.name + '/'
        for f in file.children:
            yield from walk(f)
    else:
        yield file.name

for filename in walk(root):
    print(filename)
    
# Coroutines

""" Generator only produces values
    Coroutines can also consume them """
    
# next(i) is the same as i.send(None)

def tally():
    score = 0
    while True:
        increment = yield score
        score += increment

white_sox = tally()
blue_jays = tally()

next(white_sox)
next(blue_jays)

white_sox.send(3)
blue_jays.send(2)
white_sox.send(2)
blue_jays.send(4)

# Log parsing using regex and coroutines

import re

def match_regex(filename, regex):
    with open(filename) as file:
        lines = file.readlines()
    for line in reversed(lines):
        match = re.match(regex, line)
        if match:
            regex = yield match.groups()[0]

def get_serials(filename):
    ERROR_RE = 'XFS ERROR (\[sd[a-z]\])'
    matcher = match_regex(filename, ERROR_RE)
    device = next(matcher)
    while True:
        bus = matcher.send(
                '(sd \S+) {}.*'.format(re.escape(device)))
        serial = matcher.send('{} \(SERIAL=([^)]*)\)'.format(bus))
        yield serial
        device = matcher.send(ERROR_RE)

for serial_number in get_serials('EXAMPLE_LOG.log'):
    print(serial_number)



