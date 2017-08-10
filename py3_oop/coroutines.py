#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 16:22:19 2017

@author: kt12
"""
# http://www.effectivepython.com/2015/03/10/consider-coroutines-to-run-many-functions-concurrently/

def my_coroutine():
    while True:
        received = yield
        print('Received:', received)

it = my_coroutine()
next(it)
it.send('First')
it.send('Second')

def my_coroutine_2():
    received = yield
    print('Received:', received)
    
it2 = my_coroutine_2()
next(it2)
it2.send('First') # Raise stop iteration