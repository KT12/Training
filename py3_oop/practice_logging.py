#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 17:24:07 2017

@author: kt12
"""

import logging

logging.basicConfig(filename="sample.log", level=logging.INFO)

logging.debug('This is a debug message')
logging.info('Informational message')
logging.error('An error has occurred')