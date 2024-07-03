#!/usr/bin/env python3

#SBATCH -J var_test.py
#SBATCH -o var_test_out
#SBATCH -e var_test_error
#SBATCH -q debug
#SBATCH -A marine-cpu
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH -t 05:00

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 7/2/24
############################

import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import xarray as xr

def main():

    nwpath = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/SST1997now_ensemble.nc"
    wpath = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/SST1997w_ensemble.nc"

    #read in data
    waves_in = xr.open_mfdataset(wpath)["WTMP_surface"] - 273.15  #convert to deg C
    waves = waves_in.sel(time = (waves_in.time.dt.hour == 12))  #only the 12z times

    nowaves_in = xr.open_mfdataset(nwpath)["WTMP_surface"] - 273.15 #convert to deg C
    nowaves = nowaves_in.sel(time = (nowaves_in.time.dt.hour == 12)) #only the 12z times

    #calculate the difference between waves and no waves
    diff = waves - nowaves

    var_waves = np.var(waves).values
    var_nowaves = np.var(nowaves).values

    tstat, pval = stats.ttest_ind(waves, nowaves, axis = 0, equal_var = True, alternative = "two-sided")
    
    #create latitude and longitude arrays for the plotting the p values
    lat = np.arange(-90, len(pval[:, 0]) - 90)
    lon = np.arange(0, len(pval[0, :]))
    
    #create a data array holding the p values
    xpval = xr.DataArray(pval, coords = {"latitude": lat, "longitude": lon}, dims = ["latitude", "longitude"])

    xpval = xr.DataArray(add_cyclic_point(xpval))
    print(xpval)
    
    #iget only statistically significant p values for plotting
    sig_pval = xpval.where(xpval.values < 0.05)
    print(sig_pval)
    
    #contour plot the p values
    fig, ax = plt.subplots(subplot_kw = {"projection": ccrs.PlateCarree()})
    ax.contourf(sig_pval.longitude, sig_pval.latitude, sig_pval, transform = ccrs.PlateCarree())
    ax.coastlines()

    plt.savefig("stat_sig.png")
    

if __name__ == "__main__":
    main()
