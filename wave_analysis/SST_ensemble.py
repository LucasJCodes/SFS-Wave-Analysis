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

#This program calls functions to create a single file wth the ensemble mean of model outputted SSTs for 
#the 6 conditions(with and without waves, for years 1997, 2015, 2020)

import xarray as xr

def main():
    
    #The filepaths for each model output data
        #waves 1997
    w1997mem0 = "/work2/noaa/marine/ljones/90day_experiments/waves/IC1997/COMROOT/IC1997/gefs.19971101/00/mem001/products/ocean/grib2/1p00/gefs.ocean.t00z.1p00.f*.grib2.nc" 
    w1997mem1 = "/work2/noaa/marine/ljones/90day_experiments/waves/IC1997/COMROOT/IC1997/gefs.19971101/00/mem002/products/ocean/grib2/1p00/gefs.ocean.t00z.1p00.f*.grib2.nc"

        #waves 2015

        #waves 2020

        #no waves 1997

        #no waves 2015

        #no waves 2020

    #call the method to handle ensemble file creation for each grouping
    w1997_ens = files_to_ens(w1997mem0, w1997mem1)

if __name__ == "__main__":
    main()
