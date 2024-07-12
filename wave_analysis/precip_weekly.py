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

#This program generates plots of weekly precipitation differences between SFS ensemble output data with and without waves.

def main():

    YEAR = "1997"

    path_nowaves = 
    path_waves = 

    #open and subset the wave data first
    waves_in = xr.open_mfdataset(path_waves)
    waves = waves_in["APCP_surface"] * 1000 / 100**3 * 39.3701 #kg/m^2 to inches using water density 1 g/m^3
    waves_in.close()

    #open and subset the no wave data
    nowaves_in = xr.open_mfdataset(path_nowaves)
    nowaves = nowaves_in["APCP_surface"] * 1000 / 100**3 * 39.3701 #kg/m^2 to inches using water density 1 g/m^c
    nowaves_in.close()

    #calculate the difference
    diff = waves - nowaves

    #find the largest and smallest values for determing the colorbar range and contour levels
    vmin, vmax = data_range(diff)

    levels = cont_levels(vmin, vmax, 10)

    #break into 4 weekly chunks for each dataset and average
    week1 = diff.sel(time = slice(YEAR + "-11-01", YEAR + "-11-07")).sum(dim = "time")
    week2 = diff.sel(time = slice(YEAR + "-11-08", YEAR + "-11-14")).sum(dim = "time")
    week3 = diff.sel(time = slice(YEAR + "-11-17", YEAR + "-11-23")).sum(dim = "time")
    week4 = diff.sel(time = slice(YEAR + "-11-24", YEAR + "-11-30")).sum(dim = "time")

    #plot the weekly differences
    fig, axs = plt.subplots(nrows = 2, ncols = 2, subplot_kw = {"projection": ccrs.PlateCarree()})

    p1 = axs[0][0].contourf(week1.longitude, week1.latitude, week1, transform = ccrs.PlateCarree(), cmap = "seismic", levels = levels, vmin = vmin, vmax = vmax)
    axs[0][0].set_title("Nov. 1-7, " + YEAR)
    axs[0][0].coastlines()

    p2 = axs[0][1].contourf(week2.longitude, week2.latitude, week2, transform = ccrs.PlateCarree(), cmap = "seismic", levels = levels, vmin = vmin, vmax = vmax)
    axs[0][1].set_title("Nov. 8-14, " + YEAR)
    axs[0][1].coastlines()

    p3 = axs[1][0].contourf(week3.longitude, week3.latitude, week3, transform = ccrs.PlateCarree(), cmap = "seismic", levels = levels, vmin = vmin, vmax = vmax)
    axs[1][0].set_title("Nov. 15-21, " + YEAR) 
    axs[1][0].coastlines()

    p4 = axs[1][1].contourf(week4.longitude, week4.latitude, week4, transform = ccrs.PlateCarree(), cmap = "seismic", levels = levels, vmin = vmin, vmax = vmax) 
    axs[1][1].set_title("Nov. 22-28, " + YEAR)
    axs[1][1].coastlines()

    fig.colorbar(p1, ax = axs, location = "bottom", extend = "both")

    plt.savefig("precip" + YEAR + "weekly.png")

if __name__ = "__main__":
    main()
