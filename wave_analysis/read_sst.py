#!/usr/bin/env python3

#SBATCH -J total_precip.py
#SBATCH -o out_totalp
#SBATCH -e error_totalp
#SBATCH -q debug
#SBATCH -A marine-cpu
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH -t 05:00

############################
#Author: Lucas Jones, Hollings Scholar Intern at NOAA EMC
#Date: 6/24/24
############################

#This program reads in sevearl large sst datasets one at a time, subsetting them, and then takes the ensemble mean and returns it as a separate file

import xarray as xr

def main();

    #The file paths to read in
    w1997path = 
    w2015path = 
    w2020path = 

    now1997path = 
    now2015path = 
    now2020path = 

    #read in the data, subset, and close the input channel one file at a time
    w1997_in = xr.open_mfdataset(w1997path)
    w1997_sst = w1997_in["WTMP_surface"]
    w1997_in.close()

    now1997_in = xr.open_mfdataset(now1997path)
    now1997_sst = now1997_in["WTMP_surface"]

if __name__ == "__main__":
    main()
