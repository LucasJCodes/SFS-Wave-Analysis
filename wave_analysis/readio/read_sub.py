#!/usr/bin/env python3

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 6/24/24
############################

#This method reads in a netcdf file at a given path and subsets it to a particular variable 

import xarray as xr

def read_sub(filepath, variable):

    #try to read in the data
    while True:
        try:
            ds_in = xr.open_mfdataset(filepath)
            break

        except (TypeError, NameError, ValueError):
            print("Invalid path specified")
    
    #subset the data
    while True:
        try:
            ds = ds_in[variable]
            ds_in.close()
            break

        except (TypeError, NameError, ValueError):
            print("Variable to subset by invalid or not found")

    return ds
