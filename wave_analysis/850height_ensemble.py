#!/usr/bin/env python3

#SBATCH -J 850height_ensemble.py
#SBATCH -o 850height_ens_out
#SBATCH -e 850height_ens_error
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

#This program calls functions to create a 6 files wth the ensemble mean of model outputted 850 hPa geopotential heights for
#each of the 6 respective conditions(with and without waves, for years 1997, 2015, 2020)

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis")

from readio import files_to_ens as fe

def main():

    #file paths for each condition
    #waves 1997
    w1997mem0 = 
    w1997mem1 = 

    #waves 2015

    #waves 2020

    #nowaves 1997
    now1997mem0 = 
    now1997mem1 = 

    #nowaves 2015

    #nowaves 2020

    #call the method to handle ensemble file creation for each grouping
    fe.files_to_ens("HGT_850mb", "850heigt1997w_ensemble.nc", w1997mem0, w1997mem1)

    fe.files_to_ens("HGT_850mb", "850height1997now_ensemble.nc", now1997mem0, now1997mem1)

if __name__ == "__main__":
    main()

