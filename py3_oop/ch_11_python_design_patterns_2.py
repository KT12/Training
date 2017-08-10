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
