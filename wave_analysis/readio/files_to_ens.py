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

#This program reads in an arbitrary number of netcdf datasets at onetime, subsetting them using a another function, and then takes the ensemble mean and returns it as a single, separate file.  
#Be careful using overlarge datasets.

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/readio")

import ens_mean as em
import read_sub as rs
import xarray as xr

def files_to_ens(variable, out_name, filelist):

    #for each directory of files in the group of file paths, iteratively open it, subtset, and add it to a list of subsetted files. close the io channel for each dynamically

    data_list = []

    for file in filelist:
        data_list.append(rs.read_sub(file, variable))
    
    #once files are read in and subsetted, calculate the ensemble mean
    ens = em.ens_mean(data_list)

    ens.to_netcdf(path = ("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/ensembles/" + out_name), mode = "w")
