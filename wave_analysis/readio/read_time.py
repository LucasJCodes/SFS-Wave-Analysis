#!/usr/bin/env python3

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 7/17/24
############################ 

#This method reads in a set of data and subsets it for a particular time slice, calculating the mean 
# along that slice.

import xarray as xr

def read_time(filename, variable, start_date, end_date):

    data_in = xr.open_mfdataset(filename)[variable]

    #subset the data
    data = data_in.sel(time = slice(start_date, end_date)).mean(dim = "time")

    return data

