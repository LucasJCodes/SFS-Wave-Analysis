#!/usr/bin/env python3

#SBATCH -J SST_weekly.py
#SBATCH -o SST_weekly_out
#SBATCH -e SST_weekly_error
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

#This program graphs ensemble mean wave - no wave differences in SSTs for 4 selected weeks 

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import xarray as xr

def main():

    #the filepath for the ensemble mean SST data
    waves = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/readio/SST1997w_ensemble.nc"
    nowaves = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/readio/SST1997now_ensemble.nc" 

    #read in data
    waves_in = xr.open_mfdataset(waves) - 273.15  #convert to deg C
    waves = waves_in.sel(time = (waves_in.time.dt.hour == 12))  #only the 12z times

    nowaves_in = xr.open_mfdataset(nowaves) - 273.15 #convert to deg C
    nowaves = nowaves_in.sel(time = (nowaves_in.time.dt.hour == 12)) #only the 12z times

    #calculate the difference between waves and no waves
    diff = waves - nowaves

    #subset into weekly periods (the first two and last two weeks of the period) and calculate the mean for each week (and make datarray for graphing but selecing var)
    week1 = diff.sel(time = slice("1997-11-01", "1997-11-07")).mean(dim = "time")["WTMP_surface"]
    week2 = diff.sel(time = slice("1997-11-08", "1997-11-14")).mean(dim = "time")["WTMP_surface"]
    week3 = diff.sel(time = slice("1998-01-16", "1998-01-22")).mean(dim = "time")["WTMP_surface"]
    week4 = diff.sel(time = slice("1998-01-23", "1998-01-29")).mean(dim = "time")["WTMP_surface"]

    print(week1)
    print(week2)
    print(week3)
    print(week4)

    #plot
    fig, axs = plt.subplots(nrows = 2, ncols = 2, subplot_kw = {"projection": ccrs.PlateCarree()})
    
    ax1 = axs[0][0].contourf(week1.longitude, week1.latitude, week1, transform = ccrs.PlateCarree(), cmap = "seismic")
    axs[0][0].coastlines()
    axs[0][0].set_title("Nov 1-7", loc = "left", pad = 4.0, fontsize = 10)

    plt.savefig("SST_weekly.png")

if __name__ == "__main__":
    main()
