#!/usr/bin/env python3

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 7/2/24
############################

#Simple function to determine the range for a sysmetrical matplotlib colorbar that is shared by multiple plots.
#Used for difference plots in this application.

def cbar_range(dataset):

    vmin = np.nan
    vmax = np.nan

    data_min = dataset.min().values
    data_max = dataset.max().values

    if data_max > abs(data_min):
        vmax = data_max
        vmin = -data_max

    else:
        vmax = abs(data_min)
        vmin = - abs(data_min)

    return vmin, vmax

