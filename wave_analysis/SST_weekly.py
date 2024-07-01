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

#This program graphs ensemble mean wave - no wave differences in SSTs for 4 selected weeks 
def main():

    #the filepath for each dataset in the ensemble

    #read, subset, and calculate ensemble mean

    #subset into weekly periods and calculate the mean for each week

    #plot

if __name__ == "__main__":
    main()
