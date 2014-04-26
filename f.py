#! /usr/bin/python

import sys

def my_fun(x1, x2):
  return x1*x1 + x2*x2

lines = sys.stdin.readlines()
params = [float(line) for line in lines]

print my_fun(params[0], params[1])
