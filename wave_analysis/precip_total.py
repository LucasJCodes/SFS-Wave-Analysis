#!/usr/bin/env python3

#SBATCH -J precip_total.py
#SBATCH -o precip_total_out
#SBATCH -e precip_total_error
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

#this takes ensemble mean precipitation data with and without waves and plots the difference in total precipitation

import xarray as xr

def main():
    
    #file paths for wave and non wave precip ensemble means
    waves_path = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/readio/precip1997w_ensemble.nc"
    nowaves_path = "/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/readio/precip1997now_ensemble.nc"

    #open and subset the wave data first
    waves_in = xr.open_mfdataset(waves_path)
    waves = waves_in["APCP_surface"] * 1000 / 100**3 * 39.3701 #kg/m^2 to inches using water density 1 g/m^3
    waves_in.close()

    #open and subset the no wave data
    nowaves_in = xr.open_mfdataset(nowaves_path)
    nowaves = nowaves_in["APCP_surface"] * 1000 / 100**3 * 39.3701 #kg/m^2 to inches using water density 1 g/m^c
    nowaves_in.close()

    #find the sum total precipitation for each data set
    total_waves = waves.sum(dim = "time")
    total_nowaves = nowaves.sum(dim = "time")

    #calculate the difference 
    diff = total_waves - total_nowaves

    print(diff)

    #plot the toal precipitation for each and the difference


if __name__ == "__main__":
    main()
