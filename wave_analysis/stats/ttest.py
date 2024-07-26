#!/usr/bin/env python3

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 7/3/24
############################

#This method performs a t test on the two given gridded data sets and returns an xarray holding
#gridded pvalues for locations that exceed the significance threshold, alpha.
#The t test is two sidded, performed along the first axis, and assumes equal variance

from cartopy.util import add_cyclic_point
import numpy as np
from scipy import stats
import xarray as xr

def ttest(data1, data2, alpha):

    #print("variance 1: ")
    #print(data1.var())
    #print("variance 2: ")
    #print(data2.var())

    #perform the t test
    tstat, pval = stats.ttest_ind(data1, data2, axis = 0, equal_var = True, alternative = "two-sided")
    
    #create latitude and longitude arrays for the plotting the p values
    lat = np.arange(-90, len(pval[:, 0]) - 90)  #-90 to make it -90 to 90 latitude
    lon = np.arange(0, len(pval[0, :]) + 1)  #add 1 to make 0 to 361 for adding cyclical point later

    #create a data array holding the p values and add a cyclic point to remove blank line
    xpval = xr.DataArray(add_cyclic_point(pval), coords = {"latitude": lat, "longitude": lon}, dims = ["latitude", "longitude"])

    #iget only statistically significant p values for plotting
    
    print(xpval.min())

    sig_pval = xpval.where(xpval.values <= alpha)

    return sig_pval
