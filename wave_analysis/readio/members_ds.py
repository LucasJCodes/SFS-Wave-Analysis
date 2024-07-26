#!/usr/bin/env python3

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 7/17/24
############################

#This method take a collection

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/readio")

import read_time
import numpy as np
import xarray as xr

def members_ds(filelist, out_name, variable, start_date, end_date):

    #create a numpy array that has the coordinates of the members dimension to add ot the final dataset
    members = np.arange(0, len(filelist))

    #create an empty list to hold the data set variables for each member
    list_members = []

    #read and subset each file
    for file in filelist:
        ds = read_time.read_time(file, variable, start_date, end_date)
        
        list_members.append(ds)

    member_ds = xr.concat(list_members, dim = members)

    print(member_ds)

    member_ds.to_netcdf(path = ("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/" + out_name), mode = "w")

