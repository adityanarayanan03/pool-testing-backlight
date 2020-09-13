#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 21:57:20 2020

@author: srinidhi
"""
import math

def get_tests(cell, dim):
    """
    Takes in a cell (sample number) and dim (height or width of grid). Total
    number of samples is dim^2; cell is a number from 1 to dim^2.
    
    Returns a list of 3 integers corresponding to the 3 tests for which 'cell' 
    is part of the testing pool.
    
    First number corresponds to the row test (number from 1 to dim), second
    number is for col test (from dim+1 to 2*dim), third number is for
    diagonal (wrapping) test (from 2*dim+1 to 3*dim).
    """
    if (cell % dim) >= math.ceil(cell/dim):
        return [math.ceil(cell/dim), dim + (cell % dim), 2*dim + (cell % (dim+1))]
    else:
        return [math.ceil(cell/dim), dim + (cell % dim), 
                2*dim + ((cell%dim + math.ceil(cell/dim)*dim) % (dim+1))]
