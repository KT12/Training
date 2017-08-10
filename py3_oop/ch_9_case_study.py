#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 22:17:49 2017

@author: kt12
"""

import csv

dataset_filename = 'colors.csv'

def load_colors(filename):
    with open(filename) as dataset_file:
        lines = csv.reader(dataset_file)
        for line in lines:
            yield tuple(float(y) for y in line[0:3]), line[3]

from random import random

def generate_colors(count=100):
    for i in range(count):
        yield (random(), random(), random())
        
import math
def color_distance(color1, color2):
    channels = zip(color1, color2)
    sum_distance_squared = 0
    for c1, c2 in channels:
        sum_distance_squared += (c1 - c2)**2
    return math.sqrt(sum_distance_squared)

# Alternatively as a generator exp
def color_distance_2(color1, color2):
    return math.sqrt(sum((x[0] - x[1]) **2 for x in zip(color1, color2)))

def nearest_neighbors(model_colors, num_neighbors):
    model = list(model_colors)
    target = yield
    while True:
        distances = sorted(
                ((color_distance(c[0], target), c) for c in model),
                )
        target = yield [
                d[1] for d in distances[0:num_neighbors]
                ]

def write_results(filename='output.csv'):
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        while True:
            color, name = yield
            writer.writerow(list(color) + [name])


from collections import Counter
def name_colors(get_neighbors):
    color = yield
    while True:
        near = get_neighbors.send(color)
        name_guess = Counter(
                n[1] for n in near).most_common(1)[0][0]
        color = yield name_guess

def process_colors(dataset_filename='colors.csv'):
    model_colors =  load_colors(dataset_filename)
    get_neighbors = nearest_neighbors(model_colors, 5)
    get_color_name = name_colors(get_neighbors)
    output = write_results()
    next(output)
    next(get_neighbors)
    next(get_color_name)
    
    for color in generate_colors():
        name = get_color_name.send(color)
        output.send((color, name))

process_colors()