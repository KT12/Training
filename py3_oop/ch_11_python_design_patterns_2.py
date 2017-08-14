#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 20:20:45 2017

@author: kt12
"""

class AgeCalculator:
    def __init__(self, birthday):
        self.year, self.month, self.day = (
                int(x) for x in birthday.split('-'))
    
    def calculate_age(self, date):
        year, month, day = (
                int(x) for x in date.split('-'))
        age = year - self.year
        if (month, day) < (self.month, self.day):
            age -= 1
        return age
    
# Adapter to re-use above code

import datetime

class DateAgeAdapter:
    def _str_date(self, date):
        return date.strftime("%Y-%m-%d")
    
    def __init__(self, birthday):
        birthday = self._str_date(birthday)
        self.calculator = AgeCalculator(birthday)
    
    def get_age(self, date):
        date = self._str_date(date)
        return self.calculator.calculate_age(date)

# Another way to do it - add adapter to date class

import datetime
class AgeableDate(datetime.date):
    def split(self, char):
        return self.year, self.month, self.day

# Somehow it works

bd = AgeableDate(1975, 6, 14)
today = AgeableDate.today()
today
AgeableDate(2015, 8, 4)
a = AgeCalculator(bd)
a.calculate_age(today)

# Facade pattern

import smtplib
import imaplib

class EmailFacade:
    def __init__(self, host, username, pasword):
        self.host = host
        self.username = username
        self.password = pasword
    
    def send_email(self, to_email, subject, message):
        if not "@" in self.username:
            from_email = "{0}@{1}".format(self.username, self.host)
        else:
            from_email = self.username
        
        message = ("From: {0}\r\n"
                   "To: {1}\r\n"
                   "Subject: {2}\r\n\r\n{3}").format(
                           from_email,
                           to_email,
                           subject,
                           message)
        
        smtp = smtplib.SMTP(self.host)
        smtp.login(self.username, self.password)
        smtp.sendmail(from_email, [to_email], message)
    
    def get_inbox(self):
        mailbox = imaplib.IMAP4(self.host)
        mailbox.login(bytes(self.username, 'utf8'),
                      bytes(self.password, 'utf8'))
        mailbox.select()
        x, data = mailbox.search(None, "ALL")
        messages = []
        for num in data[0].split():
            x, message = mailbox.fetch(num, '(RFC822)')
            messages.append(message[0][1])
        return messages

# Flyweight Pattern
# for memory optimization

import weakref

class CarModel:
    _models = weakref.WeakValueDictionary()
    
    def __new__(cls, model_name, *args, **kwargs):
        model = cls._models.get(model_name)
        if not model:
            model = super().__new__(cls)
            cls._models[model_name] = model
        
        return model
    
    def __init__(self, model_name, air=False, tilt=False,
                 cruise_control=False, power_locks=False,
                 alloy_wheels=False, usb_charger=False):
        if not hasattr(self, 'initted'):
            self.model_name = model_name
            self.air = air
            self.tilt = tilt
            self.cruise_control = cruise_control
            self.power_locks = power_locks
            self.alloy_wheels = alloy_wheels
            self.usb_charger = usb_charger
            self.initted = True
    
    def check_serial(self, serial_number):
        print("Sorry, we are unable to check "
              "the serial number {0} on the {1} "
              "at this time.".format(
                      serial_number, self.model_name))

class Car:
    def __init__(self, model, color, serial):
        self.model = model
        self.color = color
        self.serial = serial
    
    def check_serial(self):
        return self.model.check_serial(self.serial)

dx = CarModel('FIT DX')
lx = CarModel("FIT LX", air=True, cruise_control=True,
              power_locks=True, tilt=True)

car1 = Car(dx, 'blue', '12345')
car2 = Car(dx, 'black', '12346')
car3 = Car(lx, 'red', '12347')

# Check out weak refs at work
id(lx)
del lx
del car3
import gc
gc.collect()
# Should return 0

lx = CarModel('FIT LX', air=True, cruise_control=True,
              power_locks=True, tilt=True)
id(lx)
lx = CarModel('FIT LX')
id(lx)
lx.air

# Command Pattern

import sys

class Window:
    def exit(self):
        sys.exit(0)

class Document:
    def __init__(self, filename):
        self.filename = filename
        self.contents = 'This file cannot be modified'
    
    def save(self):
        with open(self.filename, 'w') as file:
            file.write(self.contents)

class ToolbarButton:
    def __init__(self, name, iconname):
        self.name = name
        self.iconname = iconname
    
    def click(self):
        self.command.execute()

class MenuItem:
    def __init__(self, menu_name, menuitem_name):
        self.menu = menu_name
        self.item = menuitem_name
    
    def click(self):
        self.command.execute()

class KeyboardShortcut:
    def __init__(self, key, modifier):
        self.key = key
        self.modifier = modifier
    
    def keypress(self):
        self.command.execute()

class SaveCommand:
    def __init__(self, document):
        self.document = document
    
    def execute(self):
        self.document.save()

class ExitCommand:
    def __init__(self, window):
        self.window = window
    
    def execute(self):
        self.window.exit()

window = Window()
document = Document("a_document.txt")
save = SaveCommand(document)
leave = ExitCommand(window)

save_button = ToolbarButton('save', 'save.png')
save_button.command = save
save_keystroke = KeyboardShortcut("s", "ctrl")
save_keystroke.command = save
exit_menu = MenuItem("File", "Exit")
exit_menu.command = leave

import sys

class Window:
    def leave(self):
        self.exit(0)

class MenuItem:
    def click(self):
        self.command()

window = Window()
menu_item = MenuItem()
menu_item.command = window.leave

class Document:
    def __init__(self, filename):
        self.filename = filename
        self.contents = 'This file cannot be modified'
    
    def save(self):
        with open(self.filename, 'w') as file:
            file.write(self.contents)

class KeyboardShortcut:
    def keypress(self):
        self.command()

class SaveCommand:
    def __init__(self, document):
        self.document = document
    
    def __call__(self):
        self.document.save()

document = Document("a_file.txt")
shortcut = KeyboardShortcut()
save_command = SaveCommand(document)
shortcut.command = save_command

# Abstract factory pattern

class FranceDateFormatter:
    def format_date(self, y, m, d):
        y, m, d = (str(x) for x in (y,m,d))
        y = '20' + y if len(y)  == 2 else y
        m = '0' + m if len(m) == 1 else m
        d = '0' + d if len(d) == 1 else d
        return("{0}/{1}/{2}".format(d,m,y))

class USADateFormatter:
    def format_date(self, y, m, d):
        y, m, d = (str(x) for x in (y,m,d))
        y = '20' + y if len(y)  == 2 else y
        m = '0' + m if len(m) == 1 else m
        d = '0' + d if len(d) == 1 else d
        return("{0}-{1}-{2}".format(m, d, y))

class FranceCurrencyFormatter:
    def format_curency(self, base, cents):
        base, cents = (str(x) for x in (base, cents))
        if len(cents) == 0:
            cents = '00'
        elif len(cents) == 1:
            cents = '0' + cents
        
        digits = []
        for i,c in enumerate(reversed(base)):
            if i and not i % 3:
                digits.append(' ')
            digits.append(c)
        base = ''.join(reversed(digits))
        return "{0}€{1}".format(base, cents)

class USACurrencyFormatter:
    def format_currency(self, base, cents):
        base, cents = (str(x) for x in (base, cents))
        if len(cents) == 0:
            cents = '00'
        elif len(cents) == 1:
            cents = '0' + cents
        digits = []
        for i,c in enumerate(reversed(base)):
            if i and not i % 3:
                digits.append(',')
            digits.append(c)
        base = ''.join(reversed(digits))
        return "${0}.{1}".format(base, cents)

class USAFormatterFactory:
    def create_date_formatter(self):
        return USADateFormatter()
    def create_currency_formatter(self):
        return USACurrencyFormatter()

class FranceFormatterFactory:
    def create_date_formatter(self):
        return FranceDateFormatter()
    def create_currency_formatter(self):
        return FranceCurrencyFormatter()

country_code = "US"

factory_map = {
        "US": USAFormatterFactory,
        "FR": FranceFormatterFactory}

formatter_factory = factory_map.get(country_code)()

# Composite pattern

class Component:
    def __init__(self, name):
        self.name = name
    
    def move(self, new_path):
        new_folder = get_path(new_path)
        del self.parent.children[self.name]
        new_folder.children[self.name] = name
        self.parent = new_folder
    
    def delete(self):
        del self.parent.children[self.name]
        
class Folder(Component):
    def __init__(self, name):
        super().__init__(name)
        self.children = {}
    
    def add_child(self, child):
        child.parent = self
        self.children[child.name] = child
    
    def copy(self, new_path):
        pass

class File:
    def __init__(self, name, contents):
        super().__init__(name)
        self.contents = contents
    
    def copy(self, new_path):
        pass

root = Folder('')
def get_path(path):
    names = path.split('/')[1:]
    node = root
    for name in names:
        node = node.children[name]
    return node













