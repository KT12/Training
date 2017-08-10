#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 17:35:22 2017

@author: kt12
"""

import logging

logging.basicConfig(filename='sample.log', level=logging.INFO)
log = logging.getLogger('ex')

try:
    raise RuntimeError
except Exception:
    log.exception('Error!')