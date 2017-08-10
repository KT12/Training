#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 08:54:21 2017

@author: kt12
"""

e = ("Three " "Strings " "Together")

'45.2'.isdecimal()

float('45\u06602')

'\n'.isspace()

'127.0.0.1'.isnumeric()

s = 'Hello World'
s.count('l')
s.find('l')
 s.rindex('m')
s.lower()
s.index('o')

s = 'hello world, how are you'
s2 = s.split(' ')
s2

'#'.join(s2)

s.replace(' ', '**')

s.partition(' ')

# String formatting

template = "Hello {}, you are currently {}."
print(template.format('Dusty', 'writing'))

template = "Hello {0}, you are {1}.  Your name is {0}."
print(template.format('Dusty', 'writing'))

# Escaping braces

template = """
public class {0} {{
        public static void main(String[] args) {{
                System.out.println("{1}"):
        }}
    }}"""

print(template.format("MyClass", "print('hello world')"));

# Keywords args

template = """
From: <{from_email}>
To: <{to_email}>
Subject: {subject}

{message}"""

print(template.format(
        from_email = "a@example.com",
        to_email = "b@example.com",
        message = "Here's some mail for you. "
        " Hope you enjoy the message!",
        subject = "You have mail!"))

# Can even mix keyword and index arguments

print("{} {label} {}".format("x", "y", label="z"))

# Container lookups

emails = ("a@example.com", "b@example.com")
message = {
        'subject': "You Have Mail!",
        'message': "Here's some mail for you!"}

template = """
From: <{0[0]}>
To: <{0[1]}>
Subject: {message[subject]}
{message[message]}"""

print(template.format(emails, message=message))

# Object lookups
# Change email to a class

class EMail:
    def __init__(self, from_addr, to_addr, subject, message):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.subject = subject
        self.message = message
        
email = EMail("a@example.com", "b@example.com", 
              "You have mail!",
              "Here's some mail for you")

template = """
From <(0.from_addr)>
To: <(0.to_addr)>
Subject: (0.subject)

{0.message}"""

print(template.format(email))

# Making it look right
subtotal = 12.32
tax = subtotal * 0.07
total = subtotal + tax

print("Sub: ${0} Tax: ${1} Total: ${total}".format(
        subtotal, tax, total=total))

print("Sub: ${0:0.2f} Tax: ${1:0.2f} Total: ${total:0.2f}".format(
                subtotal, tax, total=total))


orders = [('burger', 2, 5),
          ('fries', 3.5, 1),
          ('cola', 1.75, 3)]

print("PRODUCT    QUANTITY    PRICE    SUBTOTAL")
for product, price, quantity in orders:
    subtotal = price * quantity
    print("{0:10s}{1: ^9d}    ${2: <8.2f}${3: >7.2f}".format(
            product, quantity, price, subtotal))


import datetime
print("{0:%Y-%m-%d %I:%M%p }".format(
        datetime.datetime.now()))

# Can also write custom formatters for user created objects
# Need to use __format__ method


# Strings and Unicode - bytes to text

characters = b'\x63\x6c\x69\x63\x68\xe9'
print(characters)
print(characters.decode("latin-1"))

characters = 'cliché'
print(characters.encode("UTF-8"))
print(characters.encode("latin-1"))
print(characters.encode("CP437"))
print(characters.encode("ascii")) # default is strict, throws error

# Exception handling at the method
print(characters.encode(encoding="ascii", errors='replace'))
print(characters.encode(encoding="ascii", errors='ignore'))
print(characters.encode(encoding="ascii", errors='xmlcharrefreplace'))
print(characters.encode(encoding="ascii", errors='backslashreplace'))

# Check default encoding
# Best to use UTF-8
import sys
sys.getdefaultencoding()

# Mutable byte strings
b = bytearray(b"abcdefgh")
b[4:6] = b"\x15\xa3"
print(b)

# Can convert single byte character into an integer using `ord` function

b = bytearray(b"abcdef")
b[3] = ord(b'g')
b[4] = 68
print(b)

# `chr()` is inverse of ord
chr(68)

# REGEX

import re

search_string = 'hello world'
pattern = 'hello world'

match = re.match(pattern, search_string)

if match:
    print('regex matches')

# Getting info from regex matches

pattern = "^[a-zA-Z.]+@([a-z.]*\.[a-z]+)$"
search_string = 'some.user@example.com'
match = re.match(pattern, search_string)

if match:
    domain = match.groups()[0]
    print(domain)

# re.findall is not consistent in its output

re.findall('a.', 'abacadefagah')

re.findall('a(.)', 'abacadefagah')

re.findall('(a)(.)', 'abacadefagah')

re.findall('((a)(.))', 'abacadefagah')

""" If calling regexes frequently, conversion of pattern takes time.
    Better if only converting once.
    re.compile can also help speed up
"""

# Serialization

import pickle

some_data = ['a list', 'containing', 5, 'values including another list',
             ['inner', 'list']]

with open('pickled_list', 'wb') as file:
    pickle.dump(some_data, file)

with open('pickled_list', 'rb') as file:
    loaded_data = pickle.load(file)
    
print(loaded_data)
assert loaded_data == some_data