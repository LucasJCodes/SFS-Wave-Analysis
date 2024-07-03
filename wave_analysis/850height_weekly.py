#!/usr/bin/env python3

#SBATCH -J 850height_weekly.py
#SBATCH -o 850height_weekly_out
#SBATCH -e 850height_weekly_error
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

def main():
    
    #file path for the ensemble means
    wave_path = 
    nowave_path = 

    #open the data
    nowave_in = xr.open_mfdataset(path_nowave)
    wave_in = xr.open_mfdataset(path_wave)

    #subset data to get 850 hPa heights only at 12z each day
    nowave_850 = nowave_in["HGT_850mb"].sel(time = (nowave_in.time.dt.hour == 12))
    wave_850 = wave_in["HGT_850mb"].sel(time = (wave_in.time.dt.hour == 12))

    print(nowave_850)
    print(wave_850)

    #calculate the difference 
    850_diff = wave_850 - nowave_850

    #separate into weekly periods for graphing
    850_week1 = 850_diff.sel(time = slice("1997-11-01"

    #plot the differences
    fig, axs = plt.subplots(nrows = 2, ncols = 2, subplot_kw = {"projection": ccrs.PlateCarree()})
    fig.suptitle("Difference in 850hPa Geopotential Height (waves - w/o waves)", fontsize = 12)
    plt.subplots_adjust(wspace = 0.10, hspace = 0.0001)

    ax1 = axs[0][0].contourf(diff1.longitude, diff1.latitude, diff1, transform = ccrs.PlateCarree(), cmap = "seismic")
    axs[0][0].coastlines()
    axs[0][0].set_title("Nov 1-7", loc = "left", pad = 4.0, fontsize = 10)

    ax2 = axs[0][1].contourf(diff2.longitude, diff2.latitude, diff2, transform = ccrs.PlateCarree(), cmap = "seismic")
    axs[0][1].coastlines()
    axs[0][1].set_title("Nov. 8-14", loc = "left", pad = 4.0, fontsize = 10)

    ax3 = axs[1][0].contourf(diff3.longitude, diff3.latitude, diff3, transform = ccrs.PlateCarree(), cmap = "seismic")
    axs[1][0].coastlines()
    axs[1][0].set_title("Nov. 18-24", loc = "left", pad = 4.0, fontsize = 10)

    ax4 = axs[1][1].contourf(diff4.longitude, diff4.latitude, diff4, transform = ccrs.PlateCarree(), cmap = "seismic")
    axs[1][1].coastlines()
    axs[1][1].set_title("Nov. 25-Dec 1", loc = "left", pad = 4.0, fontsize = 10)

    cax = fig.add_axes([0.2, 0.1, 0.6, 0.04])
    plt.colorbar(ax4, cax = cax, extend = "both", orientation = "horizontal", label = "meters")

    plt.savefig("pres850_comp.png")


if __name__ == "__main__":
    main()
