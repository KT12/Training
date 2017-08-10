#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 23:59:38 2017

@author: kt12
"""

import datetime
from collections import namedtuple

stock = 'FB', 75.00, 75.03, 74.90


def middle(stock, date):
    symbol, current, high, low = stock
    return(((high + low) / 2), date)

mid_value, date = middle(stock, datetime.date(2014, 10, 31))

'''
So, what do we do when we want to group values together, but know we're frequently
going to need to access them individually?
Named Tuple
'''


Stock = namedtuple("Stock", "symbol current high low")
stock = Stock("FB", 75.00, high=75.03, low=74.90)
stock.high
stock.current

# Dicts

stocks = {"GOOG": (613.30, 625.86, 610.50),
          "MSFT": (30.25, 30.70, 30.19)}

stocks["GOOG"]
stocks['RIM']
stocks.get('RIM')
stocks.get('RIM', "NOT FOUND")

stocks.setdefault("GOOG", "INVALID")
stocks.setdefault("BBRY", (10.50, 10.62, 10.39))
stocks['BBRY']

for stock, values in stocks.items():
    print("{} last value is {}".format(stock, values[0]))
    
# Default Dicts

# Counting number of times letter occurs in sentence

def letter_frequency(sentence):
    frequencies = {}
    for letter in sentence:
        frequency = frequencies.setdefault(letter, 0)
        frequencies[letter] = frequency + 1
    return frequencies

# Implement same with defaultdict
from collections import defaultdict

def letter_frequency(sentence):
    frequencies = defaultdict(int)
    for letter in sentence:
        frequencies[letter] += 1
    return frequencies

from collections import Counter

def letter_frequency(sentence):
    return Counter(sentence)

responses = [
"vanilla",
"chocolate",
"vanilla",
"vanilla",
"caramel",
"strawberry",
"vanilla"
]

print(
          "The children voted for {} ice cream".format(
                  Counter(responses).most_common(1)[0][0]))

# Sorting Lists

class WeirdSortee:
    def __init__(self, string, number, sort_num):
        self.string = string
        self.number = number
        self.sort_num = sort_num
        
    def __lt__(self, object):
        if self.sort_num:
            return self.number < object.number
        return self.string < object.string

    def __repr__(self):
        return"{}:{}".format(self.string, self.number)

a = WeirdSortee('a', 4, True)
b = WeirdSortee('b', 3, True)
c = WeirdSortee('c', 2, True)
d = WeirdSortee('d', 1, True)

l = [a,b,c,d]
l
l.sort()
l

for i in l:
    i.sort_num = False
    
l
l.sort()
l

""" If you implement __lt__ and __eq__ then apply @total_ordering,
    can get all the rich comparison methods
    Need __eq__ and one other operator"""

from functools import total_ordering
    
@total_ordering
class WeirdSortee:
    def __init__(self, string, number, sort_num):
        self.string = string
        self.number = number
        self.sort_num = sort_num
        
    def __lt__(self, object):
        if self.sort_num:
            return self.number < object.number
        return self.string < object.string

    def __repr__(self):
        return"{}:{}".format(self.string, self.number)
    
    def __eq__(self, object):
        return all((
                self.string == object.string,
                self.number == object.number,
                self.sort_num == object.number
                ))

l = ["hello", "HELP", "Helo"]
l.sort()
l.sort(key=str.lower)

# itemgetter helps sort list by something other than first item
from operator import itemgetter
l = [('h', 4), ('n', 6), ('o', 5), ('p', 1), ('t', 3), ('y', 2)]
l.sort(key=itemgetter(1))
l.sort()

# Sets

""" Uniqueness is primary feature, but purpose or sets is to  compare
    sets mathematically"""
    
song_library = [("Phantom Of The Opera", "Sarah Brightman"),
("Knocking On Heaven's Door", "Guns N' Roses"),
("Captain Nemo", "Sarah Brightman"),
("Patterns In The Ivy", "Opeth"),
("November Rain", "Guns N' Roses"),
("Beautiful", "Sarah Brightman"),
("Mal's Song", "Vixy and Tony")]

artists = set()

for song, artist in song_library:
    artists.add(artist)

'Opeth' in artists

for artist in artists:
    print("{} plays good music.".format(artist))
    
alphabetical = list(artists)
alphabetical.sort()

my_artists = {"Sarah Brightman", "Guns N' Roses",
"Opeth", "Vixy and Tony"}
auburns_artists = {"Nickelback", "Guns N' Roses",
"Savage Garden"}

print("All: {}".format(my_artists.union(auburns_artists)))
print("Both: {}".format(auburns_artists.intersection(my_artists)))
print("Either but not both: {}".format(
        my_artists.symmetric_difference(auburns_artists)))

# Supersets, subsets, difference

my_artists = {"Sarah Brightman", "Guns N' Roses",
"Opeth", "Vixy and Tony"}
bands = {"Guns N' Roses", "Opeth"}

print("my_artists is to bands:")
print("issuperset: {}".format(my_artists.issuperset(bands)))
print("is subset: {}".format(my_artists.issubset(bands)))
print("difference: {}".format(my_artists.difference(bands)))
print('*'*20)
print('bands is to my_artists')
print("issuperset: {}".format(bands.issuperset(my_artists)))
print("issubset: {}".format(bands.issubset(my_artists)))
print("difference: {}".format(bands.difference(my_artists)))

# Extending Built-ins

class SillyInt(int):
    def __add__(self, num):
        return 0
    
# Constructing our own sorted dict

from collections import KeysView, ItemsView, ValuesView
class DictSorted(dict):
    def __new__(*args, **kwargs):
        new_dict = dict.__new__(*args, **kwargs)
        new_dict.ordered_keys = []
        return new_dict
    
    def __setitem__(self, key, value):
        """self[key] = value syntax"""
        if key not in self.ordered_keys:
            self.ordered_keys.append(key)
        super().__setitem__(key, value)
        
    def __setdefault__(self, key, value):
        if key not in self.ordered_keys:
            self.ordered_keys.append(key)
        return super().setdefault(key, value)
    
    def keys(self):
        return KeysView(self)
    
    def values(self):
        return ValuesView(self)
    
    def items(self):
        return ItemsView(self)
    
    def __iter__(self):
        """for x in self syntax"""
        return self.ordered_keys.__iter__()

ds = DictSorted()
d = {}
ds['a'] = 1
ds['b'] = 2
ds.setdefault('c', 3)

d['a'] = 1
d['b'] = 2
d.setdefault('c', 3)

for k,v in ds.items():
    print(k,v)
    
for k,v in d.items():
    print(k,v)
    
# Queues
"""Queues more for threads to communicate using messages
    Not intended as data structure.
    Deque is more for container use"""
    
# LIFO queues

# Priority queues

