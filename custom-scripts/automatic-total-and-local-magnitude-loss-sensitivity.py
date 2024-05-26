"""
Klaus Stephenson
Created May, 2024

Description: somewhat streamlined local and total sensivity loss calculator. Plug in a file path, and answer the terminal prompts to
recieve the total and local loss relative to the off-axis companion source location.

note:
Motivation was that different angular rotations and separations have to have local loss calculated at different pixel locations, so why not make the tedious task of finding a bunch of percentages a little bit easier?
"""
import os
from astropy.io import fits
import numpy as np
def fits_to_numpy_array(file_path):
    """
    this function converts inputed .fits file to a workable format

    Args:
        file_path (string): complete path to file of interest

    Returns:
        data_array: the x and y values for the array, used later to calculate STD
        header: needed for when creating a new HDU later filled with the calculated std values
    """
    with fits.open(file_path) as hdulist:
        data_array=hdulist[0].data
        header=hdulist[0].header
    return data_array, header


def find_dimensions(data_array):
    """
    This function find the dimensons of the array so that we can position ourselves when calculating np.nanstd later

    Args:
        data_array (numpy array): the .fits file that was converted into a usable array using fits_to_numpy_array()

    Returns:
        frames (int): number of frames; should be 1 if working with an RDI subtraction .fits file
        rows (int): number of rows/x-hat pixels
        columns (int): number of collumns/y-hat pixels
    """
    frames, rows, columns = data_array.shape #will find the number of dimensions, ie. 3 dimensions (header, x-hat, y-hat) which is what we are dealing with
    print(f"Number of frames: {frames}")
    print(f"Number of rows per frame: {rows}")
    print(f"Number of columns per frame: {columns}")
    return frames, rows, columns


def find_average_loss_total(data_array):
    """
    Find the highest value (maximum loss) within the data array.
    Args:
        data_array (numpy array): the .fits file that was converted into a usable array using fits_to_numpy_array()
    
    Returns:
    average_loss_total (int): the average loss for the entire .fits file
    """
    average = np.average(data_array)
    print(f"\nthe average is {average}")
    average_loss_total = average 
    print(f"max loss:  {average_loss_total*100:.0f} percent")
    #troubleshooting
    #min_value = np.nanmin(data_array)
    #max_value = np.nanmax(data_array)
    #print(f"The minimum raw pixel in {filename} is {min_value}")
    #print(f"The maximum raw pixel in {filename} is {max_value}")

def find_local_loss(data_array, x_location, y_location, filename, arcsec_per_pixel=0.063):
    """
    Find the average pixel value within 1" of the specified location.

    Args:
        data_array (numpy array): The data array from the .fits file.
        x_location : X coordinate of the location of interest.
        y_location : Y coordinate of the location of interest.
        filename (string): Name of the file for reporting.
        arcsec_per_pixel : Conversion factor from arcseconds to pixels.
    """
    if data_array.ndim == 2:
        rows, columns = data_array.shape
    elif data_array.ndim == 3:
        _, rows, columns = data_array.shape
    else:
        raise ValueError("Invalid dimensions of the data array")
    
    x_coords, y_coords = np.meshgrid(np.arange(columns), np.arange(rows))
    distances = np.sqrt((x_coords - x_location)**2 + (y_coords - y_location)**2)
    
    # Convert radius from arcseconds to pixels
    radius_pixels = 1 / arcsec_per_pixel
    #print(f"radius pixel is {radius_pixels}") #should be 15.87301587
    mask = distances <= radius_pixels
    
    pixel_subset = data_array[mask]
    average_loss_local = np.average(pixel_subset)
    print(f"\nthe average local to companion is {average_loss_local}")
    print(f"local loss: {average_loss_local*100:.0f} percent \n")


def get_coordinates(arcsecond_offset, theta_offset):
    """Get the x and y coordinates based on R and Theta."""
    if theta_offset =='0':
        if arcsecond_offset =='05':
            x_location_of_companion, y_location_of_companion = 42.56, 50.5
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='1':
            x_location_of_companion, y_location_of_companion = 34.62, 50.5
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='15':
            x_location_of_companion, y_location_of_companion = 26.69, 50.5
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='2':
            x_location_of_companion, y_location_of_companion = 18.75, 50.5
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='25':
            x_location_of_companion, y_location_of_companion = 10.81, 50.5
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='3':
            x_location_of_companion, y_location_of_companion = 2.88, 50.5
            return x_location_of_companion, y_location_of_companion
    elif theta_offset =='45':
        if arcsecond_offset =='05':
            x_location_of_companion, y_location_of_companion = 44.88915, 44.88915
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='1':
            x_location_of_companion, y_location_of_companion = 39.29, 39.29 
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='15':
            x_location_of_companion, y_location_of_companion = 33.6674, 33.6674
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='2':
            x_location_of_companion, y_location_of_companion = 28.0566, 28.0566
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='25':
            x_location_of_companion, y_location_of_companion = 22.445, 22.445
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='3':
            x_location_of_companion, y_location_of_companion = 16.8349, 16.8349
            return x_location_of_companion, y_location_of_companion
    elif theta_offset =='90':
        if arcsecond_offset =='05':
            x_location_of_companion, y_location_of_companion = 50.5, 42.56
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='1':
            x_location_of_companion, y_location_of_companion = 50.5, 34.62
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='15':
            x_location_of_companion, y_location_of_companion = 50.5, 26.69
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='2':
            x_location_of_companion, y_location_of_companion = 50.5, 18.75
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='25':
            x_location_of_companion, y_location_of_companion = 50.5, 10.81
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='3':
            x_location_of_companion, y_location_of_companion = 50.5, 2.88
            return x_location_of_companion, y_location_of_companion
    elif theta_offset =='135':
        if arcsecond_offset =='05':
            x_location_of_companion, y_location_of_companion = 56.11, 44.88915
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='1':
            x_location_of_companion, y_location_of_companion = 61.7217, 39.29
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='15':
            x_location_of_companion, y_location_of_companion = 67.33255, 33.6674
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='2':
            x_location_of_companion, y_location_of_companion = 72.9434, 28.0566
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='25':
            x_location_of_companion, y_location_of_companion = 78.55425, 22.445
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='3':
            x_location_of_companion, y_location_of_companion = 84.1651, 16.8349
            return x_location_of_companion, y_location_of_companion
    elif theta_offset =='180':
        if arcsecond_offset =='05':
            x_location_of_companion, y_location_of_companion = 58.4365, 50.5
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='1':
            x_location_of_companion, y_location_of_companion = 66.373, 50.5
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='15':
            x_location_of_companion, y_location_of_companion = 74.309, 50.5
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='2':
            x_location_of_companion, y_location_of_companion = 82.24, 50.5
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='25':
            x_location_of_companion, y_location_of_companion = 90.182, 50.5
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='3':
            x_location_of_companion, y_location_of_companion = 98.119, 50.5
            return x_location_of_companion, y_location_of_companion
    elif theta_offset =='225':
        if arcsecond_offset =='05':
            x_location_of_companion, y_location_of_companion = 56.11, 56.11
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='1':
            x_location_of_companion, y_location_of_companion = 61.7217, 61.7217 
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='15':
            x_location_of_companion, y_location_of_companion = 67.33255, 67.33255
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='2':
            x_location_of_companion, y_location_of_companion = 72.9434, 72.9434
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='25':
            x_location_of_companion, y_location_of_companion = 78.55425, 78.55425
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='3':
            x_location_of_companion, y_location_of_companion = 84.1651, 84.1651
            return x_location_of_companion, y_location_of_companion
    elif theta_offset =='270':
        if arcsecond_offset =='05':
            x_location_of_companion, y_location_of_companion = 50.5, 58.4365
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='1':
            x_location_of_companion, y_location_of_companion = 50.5, 66.373
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='15':
            x_location_of_companion, y_location_of_companion = 50.5, 74.309
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='2':
            x_location_of_companion, y_location_of_companion = 50.5, 82.24
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='25':
            x_location_of_companion, y_location_of_companion = 50.5, 90.182
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='3':
            x_location_of_companion, y_location_of_companion = 50.5, 98.119
            return x_location_of_companion, y_location_of_companion
    elif theta_offset =='315':
        if arcsecond_offset =='05':
            x_location_of_companion, y_location_of_companion = 44.88915, 56.11
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='1':
            x_location_of_companion, y_location_of_companion = 39.29, 61.7217 
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='15':
            x_location_of_companion, y_location_of_companion = 33.6674, 67.33255
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='2':
            x_location_of_companion, y_location_of_companion = 28.0566, 72.9434
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='25':
            x_location_of_companion, y_location_of_companion = 22.445, 78.55425
            return x_location_of_companion, y_location_of_companion
        elif arcsecond_offset =='3':
            x_location_of_companion, y_location_of_companion = 16.8349, 84.1651
            return x_location_of_companion, y_location_of_companion
    else:
        raise ValueError("Invalid Theta value")
    return None, None



filename = ''
arcsecond_offset = input('what is the R?: \n')
theta_offset = input('what is the theta? (in degrees): \n')  
x_location_of_companion, y_location_of_companion = get_coordinates(arcsecond_offset, theta_offset)  
print(f"\n CALCULATING FOR {filename} \n")
data_array, header = fits_to_numpy_array(filename)
rows, columns = find_dimensions(data_array)
find_average_loss_total(data_array, filename)  # Added filename as an argument
find_local_loss(data_array, x_location_of_companion, y_location_of_companion, filename)  # Added filename as an argument
