#!/usr/bin/env python3

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 7/19/24
############################

#This is a simple wrapper/helper function to read in data for a monthly period  and then calculate p values using the ttest()
#function.  These p values are returned as xarray datasets for graphing.

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/readio")

from stats import ttest
import xarray as xr

def monthly_ttest(variable, year, start_month, alpha):

    waves_in = xr.open_dataarray("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/monthly/" + variable + "w" + year + start_month + ".nc")
    nowaves_in = xr.open_dataarray("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/monthly/" + variable + year + start_month + ".nc")

    pvals = ttest.ttest(waves_in, nowaves_in, alpha)

    return pvals
