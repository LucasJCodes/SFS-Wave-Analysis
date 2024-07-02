#!/usr/bin/env python3

#SBATCH -J precip_ensemble.py
#SBATCH -o precip_ens_out
#SBATCH -e precip_ens_error
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

#This program calls functions to create a 6 files with the ensemble mean of model outputted precipitation for
#each of the 6 conditions respectively(with and without waves, for years 1997, 2015, 2020)

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis")

from readio import files_to_ens as fe

def main():
    
    #file paths for each condition
    #waves 1997
    w1997mem0 = "/work2/noaa/marine/ljones/90day_experiments/waves/IC1997/COMROOT/IC1997/gefs.19971101/00/mem001/products/atmos/grib2/1p00/gefs.t00z.pgrb2.1p00.f*.nc"
    w1997mem1 = "/work2/noaa/marine/ljones/90day_experiments/waves/IC1997/COMROOT/IC1997/gefs.19971101/00/mem002/products/atmos/grib2/1p00/gefs.t00z.pgrb2.1p00.f*.nc"

    #waves 2015

    #waves 2020

    #nowaves 1997
    now1997mem0 = "/work2/noaa/marine/ljones/90day_experiments/no_waves/IC1997/COMROOT/IC1997/gefs.19971101/00/mem001/products/atmos/grib2/1p00/gefs.t00z.pgrb2.1p00.f*.nc"
    now1997mem1 = "/work2/noaa/marine/ljones/90day_experiments/no_waves/IC1997/COMROOT/IC1997/gefs.19971101/00/mem002/products/atmos/grib2/1p00/gefs.t00z.pgrb2.1p00.f*.nc"

    #nowaves 2015

    #nowaves 2020

    #call the method to handle ensemble file creation for each grouping
    fe.files_to_ens("APCP_surface", "precip1997w_ensemble.nc", w1997mem0, w1997mem1)

    fe.files_to_ens("APCP_surface", "precip1997now_ensemble.nc", now1997mem0, now1997mem1)

if __name__ == "__main__":
    main()
