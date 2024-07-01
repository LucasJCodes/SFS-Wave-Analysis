#!/usr/bin/env python3

import xarray as xr

def read_sub(filepath, variable)

    #try to read in the data
    while True:
        try:
            ds_in = xr.open_mfdataset(filepath)
            break

        except TypeError, NameError, ValueError:
            print("Invalid path specified")
    
    #subset the data
    while True:
        try:
            ds = ds_in[variable]
            break

        except TypeError, NameError, ValueError:
            print("Variable to subset by invalid or not found")

    return ds
