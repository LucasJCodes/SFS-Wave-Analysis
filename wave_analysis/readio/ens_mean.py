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

def ens_mean(*datasets):

