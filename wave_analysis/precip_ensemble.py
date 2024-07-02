#!/usr/bin/env python3

#SBATCH -J precip_weekly.py
#SBATCH -o precip_weekly_out
#SBATCH -e precip_weekly_error
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

#This program calls functions to create a single file wth the ensemble mean of model outputted precipitation for
#the 6 conditions(with and without waves, for years 1997, 2015, 2020)

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis")

from readio import files_to_ensemble as fe

def main():
    
    #file paths for each condition
    #waves 1997
    w1997mem0 = "/work2/noaa/marine/ljones/90day_experiments/waves/IC1997/COMROOT/IC1997/gefs.19971101/00/mem001/products/atmos/grib2/1p00/gefs.t00z.pgrb2.1p00.f*.nc"

    #waves 2015

    #waves 2020

    #nowaves 1997

    #nowaves 2015

    #nowaves 2020

    #call the method to handle ensemble file creation for each grouping
    w1997_ens = fe.files_to_ens()

    now1997_ens = fe.files_to_ens()

if __name__ == "__main__":
    main()
