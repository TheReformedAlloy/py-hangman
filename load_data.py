# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 16:11:05 2019

@author: Clint Mooney
"""

import os

word_list = []

def process_word_data():
    temp_list = []
    with open('data/dict/index.sense') as word_file:
        for line in word_file.readlines():
            keep = False
            for letter in line:
                if letter.isalpha():
                    keep = True
                    break
            if keep:
                word = line.split('%')[0].replace('_', ' ')
                temp_list.append(word)
    with open('data/processed_data.tsv', 'w') as data_file:
        start = True
        for word in temp_list:
            if start != True:
                data_file.write('\t')
            else:
                start = False
            data_file.write(word)

def read_processed_data():
    if os.path.isfile('data/processed_data.tsv'):
        with open('data/processed_data.tsv') as data_file:
            for word in data_file.read().split('\t'):
                word_list.append(word)
        
        return word_list
    else:
        process_word_data()
        read_processed_data()

def get_data():
    read_processed_data()
    return word_list