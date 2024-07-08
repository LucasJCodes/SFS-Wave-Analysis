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
#Date: 7/8/24
############################


