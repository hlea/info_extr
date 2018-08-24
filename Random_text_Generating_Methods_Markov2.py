# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 15:04:58 2017

@author: hlea
"""

import sys
from random import choice
import datetime
import uuid

EOS = ['.', '?', '!']
Brands = ['Aries', 'Hercules', 'Pluto']
sys.argv.append(r"C:\Users\hlea\Documents\Proposals_BusDev\AWS\Code\Sample_Product_Quality_Text.txt")

##################################################################################################
'''
This first set of functions builds random sentences using a dictionary with 2-word sequences as keys. 
The effect to build sentences that are less likely to be in the original corpus, although have a higher chance
of being grammatically accurate/syntactically realistic..
'''

def build_dict_short(words):
    """
    Build a dictionary from the words.
    (word1, word2) => [w1, w2, ...]  # key: tuple; value: list
    """
    d = {}
    for i, word in enumerate(words):
        try:
            first, second, third = words[i], words[i+1], words[i+2]
        except IndexError:
            break
        key = (first, second)
        if key not in d:
            d[key] = []
        
        d[key].append(third)

    return d

def generate_sentence_shortdict(d):
    li = [key for key in d.keys() if key[0][0].isupper()]
    key = choice(li)
    
    li = []
    first, second = key
    li.append(first)
    li.append(second)
    while True:
        try:
            third = choice(d[key])
        except KeyError:
            break
        li.append(third)
        if third[-1] in EOS:
            break
        key = (second, third)
        first, second = key
        
    return ' '.join(li)

def main_short():

    fname = sys.argv[1]
    with open(fname, "rt", encoding="utf-8") as f:
    #with open(fname) as f:
        text = f.read()
    words = text.split()
    d = build_dict_short(words)
    #pprint(d)
    #print()
    sent = generate_sentence_shortdict(d)
    print(sent)
    return sent


def record_maker():
    sent = main_short()
    brand = choice(Brands)
    date = datetime.datetime.today()
    ID = uuid.uuid4()
    lst = [str(ID), brand, date, sent]
    print(lst)
    return lst


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Error: provide an input corpus file.")
        sys.exit(1)
    record_maker()