#!/usr/bin/env python3

#SBATCH -J total_precip.py
#SBATCH -o test_out
#SBATCH -e test_error
#SBATCH -q debug
#SBATCH -A marine-cpu
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH -t 05:00

import sys
sys.path.append("/work2/noaa/marine/ljones/SFS-Wave-Analysis/wave_analysis/readio")

from readio import hello

def main()
    
    hello.hello()

if __name__ == "__main__":
    main()
