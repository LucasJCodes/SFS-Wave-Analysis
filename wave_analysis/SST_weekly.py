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

import xarray as xr

def main():

    #the filepath for the ensemble mean SST data
    waves = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/readio/SST1997w_ensemble.nc"
    #nowaves = 

    #read in data
    waves_in = xr.open_mfdataset(waves)- 273.15  #convert to deg C
    waves = waves_in.sel(time = (waves_in.time.dt.hour == 12))

    print(waves["time"])


    #calculate the difference between waves and no waves
    #diff = waves_in - nowaves_in

    #subset into weekly periods (the first two and last two weeks of the period) and calculate the mean for each week
    #week1 = diff.sel(time = slice("1997-11-01", "1997-11-07"))
    #week2 = diff.sel(time = slice("1997-11-08", "1997-11-14"))

    #plot

if __name__ == "__main__":
    main()
