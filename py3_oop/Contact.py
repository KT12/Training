#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 18:12:52 2017

@author: kt12
"""

class Contact:
    def __init__(self, first, last):
        self.first = first
        self.last = last
    
    @property
    def full_name(self):
        return("{} {}".format(self.first, self.last))

import json
class ContactEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Contact):
            return {'is_contact': True,
                    'first': obj.first,
                    'last': obj.last,
                    'full': obj.full_name}
        return super().defalt(obj)

def decode_contact(dic):
    if dic.get('is_contact'):
        return Contact(dic['first'], dic['last'])
    else:
        return dic