#!/usr/bin/env python3

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 7/2/24
############################

#Function to determine the level/bin divisions given a max and min value and number od desired levels.
#This can be used to ensure plots have the same contour levels between multiple plots of different data.

import numpy as np

def cont_levels(vmin, vmax, nlevels):

    step = (vmax - vmin) / nlevels
    levels = np.arange(vmin, vmax + 0.1, step) # levels for the contour p (+0.1 to make upper inclusive)

    return levels
