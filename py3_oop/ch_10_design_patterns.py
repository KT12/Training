#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 16:06:17 2017

@author: kt12
"""

import socket

def respond(client):
    response = input("Enter a value: ")
    client.send(bytes(response, 'utf8'))
    client.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 2401))
server.listen(1)
try:
    while True:
        client, addr = server.accept()
        respond(client)
finally:
    server.close()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 2401))
print('Received: {0}'.format(client.recv(1024)))
client.close()

# Do with decorator instead

class LogSocket:
    def __init__(self, socket):
        self.socket = socket
    
    def send(self, data):
        print("Sending {0} to {1}".format(
                data, self.socket.getpeername()[0]))
        self.socket.send(data)
    
    def close(self):
        self.socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 2401))
server.listen(1)
try:
    while True:
        client, addr = server.accept()
        respond(LogSocket(client))
finally:
    server.close()

import gzip
from io import BytesIO

class GzipSocket:
    def __init__(self, socket):
        self.socket = socket
    
    def send(self, data):
        buf = BytesIO()
        zipfile = gzip.GzipFile(fileobj=buj, mode='w')
        zipfile.write(data)
        zipfile.close()
        self.socket.send(buf.getvalue())
    
    def close(self):
        self.socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('',2401))
server.listen(1)
try:
    while True:
        client, addr = server.accept()
        respond(GzipSocket(client))
finally:
    server.close()

# Decorators in Python

import time

def log_calls(func):
    def wrapper(*args, **kwargs):
        now = time.time()
        print("Calling {0} with {1} and {2}".format(
                func.__name__, args, kwargs))
        return_value = func(*args, **kwargs)
        print("Executed {0} in {1}ms".format(
                func.__name__, time.time() - now))
        return return_value
    return wrapper

def test1(a,b,c):
    print("\ttest1 called")

def test2(a,b):
    print("\ttest2 called")
    
def test3(a,b):
    print("\ttest3 called")
    time.sleep(1)

test1 = log_calls(test1)
test2 = log_calls(test2)
test3 = log_calls(test3)

test1(1,2,3)
test2(4, b=5)
test3(6,7)

@log_calls
def test4(a,b,c):
    print("\ttest4 called")
    
test4(1,3,c=5)

# Observer Patterns

class Inventory:
    def __init__(self):
        self.observers = []
        self._product = None
        self._quantity = 0
    
    def attach(self, observer):
        self.observers.append(observer)
    
    @property
    def product(self):
        return self._product
    
    @product.setter
    def product(self, value):
        self._product = value
        self._update_observers()
    
    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, value):
        self._quantity = value
        self._update_observers()
    
    def _update_observers(self):
        for observer in self.observers:
            observer()

class ConsoleObserver:
    def __init__(self, inventory):
        self.inventory = inventory
    
    def __call__(self):
        print(self.inventory.product)
        print(self.inventory.quantity)

i = Inventory()
c = ConsoleObserver(i)
i.attach(c)
i.product = 'Widget'
i.quantity = 5

i = Inventory()
c1 = ConsoleObserver(i)
c2 = ConsoleObserver(i)
i.attach(c1)
i.attach(c2)
i.product = "Gadget"

# Strategy pattern

from PIL import Image

class TiledStrategy:
    def make_background(self, img_file, desktop_size):
        in_img = Image.open(img_file)
        out_img = Image.new('RGB', desktop_size)
        num_tiles = [
                o // i + 1 for o, i in
                zip(out_img.size, in_img.size)
                ]
        for x in range(num_tiles[0]):
            for y in range(num_tiles[1]):
                out_img.paste(
                        in_img,
                        (
                                in_img.size[0] * x,
                                in_img.size[1] * y,
                                in_img.size[0] * (x + 1),
                                in_img.size[1] * (y + 1)
                                )
                        )
        return out_img

class CenteredStrategy:
    def make_background(self, img_file, desktop_size):
        in_img = Image.open(img_file)
        out_img = Image.new('RGB', desktop_size)
        left = (out_img.size[0] - in_img.size[0]) // 2
        top = (out_img.size[1] - in_img.size[1]) // 2
        out_img.paste(
                in_img,
                (left,
                 top,
                 left+in_img.size[0],
                 top + in_img.size[1]
                 )
                )
        return out_img

class ScaledStrategy:
    def make_background(self, img_file, desktop_size):
        in_img = Image.open(img_file)
        out_img = in_img.resize(desktop_size)
        return out_img

# State Pattern

class Node:
    def __init__(self, tag_name, parent=None):
        self.parent = parent
        self.tag_name = tag_name
        self.children = []
        self.text=""
    
    def __str__(self):
        if self.text:
            return self.tag_name + ':' + self.text
        else:
            return self.tag_name

class Parser:
    def __init__(self, parse_string):
        self.parse_string = parse_string
        self.root = None
        self.current_node = None
        
        self.state = FirstTag()
    
    def process(self, remaining_string):
        remaining = self.state.process(remaining_string, self)
        if remaining:
            self.process(remaining)
        
    def start(self):
        self.process(self.parse_string)

class FirstTag:
    def process(self, remaining_string, parser):
        i_start_tag = remaining_string.find('<')
        i_end_tag = remaining_string.find('>')
        tag_name = remaining_string[i_start_tag+1:i_end_tag]
        root = Node(tag_name)
        parser.root = parser.current_node = root
        parser.state = ChildNode()
        return remaining_string[i_end_tag+1:]

class ChildNode:
    def process(self, remaining_string, parser):
        stripped = remaining_string.strip()
        if stripped.startswith('</'):
            parser.state = CloseTag()
        elif stripped.startswith("<"):
            parser.state = OpenTag()
        else:
            parser.state = TextNode()
        return stripped

class OpenTag:
    def process(self, remaining_string, parser):
        i_start_tag = remaining_string.find('<')
        i_end_tag = remaining_string.find('>')
        tag_name = remaining_string[i_start_tag+1:i_end_tag]
        node = Node(tag_name, parser.current_node)
        parser.current_node.children.append(node)
        parser.current_node = node
        parser.state = ChildNode()
        return remaining_string[i_end_tag+1:]

class CloseTag:
    def process(self, remaining_string, parser):
        i_start_tag = remaining_string.find('<')
        i_end_tag = remaining_string.find('>')
        assert remaining_string[i_start_tag+1] == '/'
        tag_name = remaining_string[i_start_tag+2:i_end_tag]
        assert tag_name == parser.current_node.tag_name
        parser.current_node = parser.current_node.parent
        parser.state = ChildNode()
        return remaining_string[i_end_tag+1:].strip()

class TextNode:
    def process(self, remaining_string, parser):
        i_start_tag = remaining_string.find('<')
        text = remaining_string[:i_start_tag]
        parser.current_node.text = text
        parser.state = ChildNode()
        return remaining_string[i_start_tag:]

if __name__ == "__main__":
    import sys
    with open(sys.argv[1]) as file:
        contents = file.read()
        p = Parser(contents)
        p.start()
        
        nodes = [p.root]
        while nodes:
            node = nodes.pop(0)
            print(node)
            nodes = node.children + nodes

# Singleton (not always recommended for Python)

class OneOnly:
    _singleton = None
    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = super(OneOnly, cls).__new__(cls, *args, **kwargs)
        return cls._singleton

o1 = OneOnly()
o2 = OneOnly()

o1 == o2
o1
o2
# Same object at same address

# Use module level variables instead of a singleton 
# Most Pythonic implementation

class FirstTag:
    def process(self, remaining_string, parser):
        i_start_tag = remaining_string.find('<')
        i_end_tag = remaining_string.find('>')
        tag_name = remaining_string[i_start_tag+1:i_end_tag]
        root = Node(tag_name)
        parser.root = parser.current_node = root
        parser.state = child_node
        return remaining_string[i_end_tag+1:]

class ChildNode:
    def process(self, remaining_string, parser):
        stripped = remaining_string.strip()
        if stripped.startswith("</"):
            parser.state = close_tag
        elif stripped.startswith("<"):
            parser.state = open_tag
        else:
            parser.state = text_node
        return stripped

class OpenTag:
    def process(self, remaining_string, parser):
        i_start_tag = remaining_string.find("<")
        i_end_tag = remaining_string.find(">")
        tag_name = remaining_string[i_start_tag+1:i_end_tag]
        node = Node(tag_name, parser.current_node)
        parser.current_node.children.append(node)
        parser.current_node = node
        return remaining_string[i_end_tag+1:]

class TextNode:
    def process(self, remaining_string, parser):
        i_start_tag = remaining_string.find("<")
        text = remaining_string[:i_start_tag]
        parser.current_node.text = text
        parser.state = child_node
        return remaining_string[i_start_tag:]

class CloseTag:
    def process(self, remaining_string, parser):
        i_start_tag = remaining_string.find("<")
        i_end_tag = remaining_string.find(">")
        assert remaining_string[i_start_tag+1] == "/"
        tag_name = remaining_string[i_start_tag+2:i_end_tag]
        assert tag_name == parser.current_node.tag_name
        parser.current_node = parser.current_node.parent
        parser.state = child_node
        return remaining_string[i_end_tag+1:].strip()

first_tag = FirstTag()
child_node = ChildNode()
text_node = TextNode()
open_tag = OpenTag()
close_tag = CloseTag()

# Template pattern
# DRY

# Car sales reporter

# Create DB and stuff figures in
import sqlite3

conn = sqlite3.connect('sales.db')

conn.execute("CREATE TABLE Sales (salesperson text, "
            "amt currency, year integer, model text, new boolean)")
conn.execute("INSERT INTO Sales values"
            " ('Tim', 16000, 2010, 'Honda Fit', 'true')")
conn.execute("INSERT INTO Sales values"
             " ('Tim', 9000, 2006, 'Ford Focus', 'false')")
conn.execute("INSERT INTO Sales values"
             " ('Gayle', 8000, 2004, 'Dodge Neon', 'false')")
conn.execute("INSERT INTO Sales values"
             " ('Gayle', 28000, 2009, 'Ford Mustang', 'true')")
conn.execute("INSERT INTO Sales values"
             " ('Gayle', 50000, 2010, 'Lincoln Navigator', 'true')")
conn.execute("INSERT INTO Sales values"
             " ('Don', 20000, 2008, 'Toyota Prius', 'false')")
conn.commit()
conn.close()

import sqlite3

class QueryTemplate:
    def connect(self):
        self.conn = sqlite3.connect('sales.db')
    
    def construct_query(self):
        raise NotImplementedError()
    
    def do_query(self):
        results = self.conn.execute(self.query)
        self.results = results.fetchall()
    
    def format_results(self):
        output = []
        for row in self.results:
            row = [str(i) for i in row]
            output.append(", ".join(row))
        self.formatted_results = "\n".join(output)
    
    def output_results(self):
        raise NotImplementedError()
    
    def process_format(self):
        self.connect()
        self.construct_query()
        self.do_query()
        self.format_results()
        self.output_results()

import datetime
class NewVehiclesQuery(QueryTemplate):
    def construct_query(self):
        self.query = "select * from Sales where new='true'"
    
    def output_results(self):
        print(self.format_results)

class UserGrossQuery(QueryTemplate):
    def construct_query(self):
        self.query = ("select salesperson, sum(amt) from Sales group by salesperson")
    
    def output_results(self):
        filename = "gross_sales{0}".format(
                datetime.date.today().strftime("%Y%m%d"))
        with open(filename,'w') as outfile:
            outfile.write(self.format_results)





