#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import serial


class Pool_Matrix:
    """
    Class for the Duration of a pool-testing run.
    """

    sampleNum = 0
    dim = None
    readFile = None

    def __init__(self, dim=None, sampleNum=0, readFile=None):
        self.dim = dim
        self.sampleNum = sampleNum
        self.readFile = readFile

    def read_inputs(self):
        """
        Should read inputs from either the command line or a GUI
        """
        raise NotImplementedError

    def plus_one(self, parameter_list):
        """
        Increases the sample number by 1.
        """

        if (self.sampleNum, self.dim):
            self.sampleNum += 1
            return True
        else:
            return False

    def get_tests(self, cell, dim):
        """
        Takes in a cell (sample number) and dim (height or width of grid). Total
        number of samples is dim^2; cell is a number from 1 to dim^2.

        Returns a list of 3 integers corresponding to the 3 tests for which 'cell'
        is part of the testing pool.

        First number corresponds to the row test (number from 1 to dim), second
        number is for col test (from dim+1 to 2*dim), third number is for
        diagonal (wrapping) test (from 2*dim+1 to 3*dim).
        """
        if (cell % dim) >= math.ceil(cell / dim):
            return [
                math.ceil(cell / dim),
                dim + (cell % dim),
                2 * dim + (cell % (dim + 1)),
            ]
        else:
            return [
                math.ceil(cell / dim),
                dim + (cell % dim),
                2 * dim + ((cell % dim + math.ceil(cell / dim) * dim) % (dim + 1)),
            ]

    def send_to_arduino(self, leds):
        """
        Takes in the three(or really how many ever) integers from 0-90 that correspond
        to values for the 8x12 LED matrix and sends them over serial connection to the
        Arduino

        Returns True if successful, False if error occurred, and throws errors.
        """
        raise NotImplementedError


if __name__ == "__main__":
    run = Pool_Matrix()
    print(run.sampleNum)
