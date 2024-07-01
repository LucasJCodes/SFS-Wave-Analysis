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

#This function calculates an ensemble mean of an arbitrary number of datasets
import xarray as xr

def ens_mean(list_of_datasets):
    
    #calculate the mean of the datasets, assigning them to one other single dataset
    ens = sum(datasets) / len(datasets)

    print(ens)

    return ens
