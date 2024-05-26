"""
Klaus Stephenson
Created January, 2024

Description: given a folder filled with .fits RDI simulations, for each simulation create a standard deviation (STD) 
plot with a filename based on the simulation

Notes: 
possible update for public users' experience -- instead of asking for aperture_in_meters just ask for the instrument (nircam, miri) 
and the added mask (lyot,pupil,bar) and have default hard-coded values based on what the user inputs
"""

#can import everything outside of __name__='__main__' brackets since not using pancake... 
from math import pi
import numpy as np
from astropy.io import fits
import os

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

def find_lambda_over_d(wavelength,aperture_in_meters):
    """
    mostly created this function for my (klaus') own conceptual understanding
    this function answers the question 'where should the box-ring region start and stop?'
    utilizing lambda/d ='wavelength-observing-in'/'effective aperture of science instrument'

    Args:
        wavelength (float): complete path to file of interest
        aperture_in_meters(float): the effective aperture of the science instrument + coronagraphic tool used

    Returns:
        lambda_over_d: the pixel value of lambda/d to be used as a spacing 
        constant when finding the box-ring pixel subset around a specific pixel

example usage:
an observation taken at 4.5 micron, so lambda = 4.5e-6 m
D for JWST is nominally ~6.5m, but for NIRCam coronagraphy the effective diameter is reduced due to 
the Lyot stop (see Figure 3 here: https://jwst-docs.stsci.edu/jwst-near-infrared-camera/nircam-instrumentation/nircam-coronagraphic-occulting-masks-and-lyot-stops). In this case, it’s closer to ~5.2m.
lambda/D = 4.5e-6 / 5.2 = 8.65e-7, in radians
need to convert to useful units for simulation data
radians > degrees > arcseconds > pixels
8.65e-7 radians * 180/pi * 3600 arcseconds = 0.178 arcseconds
The NIRCam long wavelength channel pixel scale is 1 pixel per 0.063 arcseconds (https://jwst-docs.stsci.edu/jwst-near-infrared-camera/nircam-instrumentation/nircam-detector-overview). 
0.178 arcseconds / 0.063 arcseconds =~ 2.82 pixels
    """
    lambda_over_d=((wavelength/aperture_in_meters)*(180/pi)*3600)/0.063
    #print(f'this is lambda/d: {lambda_over_d}') #troubleshooting
    return lambda_over_d

def find_standard_deviation(data_array, lambda_over_d, rows, columns):
    """
    This function find the standard deviation for all pixels in a given .fits file

    Args:
        data_array (numpy array): the .fits file that was converted into a usable array using fits_to_numpy_array()
        lambda_over_d (int): science parameter, check previous funtion
        rows, columns (int): from find_dimensions(), used to do some fun math that needs x/y positions
    Returns:
        std_array (numpy array): new numpy array of properly calculated STDs for each pixel in original .fits file, that can then be processed into a .fits file
    """
    std_array = np.zeros((rows, columns), dtype=data_array.dtype) # empty numpy array to store calculated std values in
    x_coords, y_coords = np.meshgrid(np.arange(rows), np.arange(columns)) # create coordinate grids
    for i in range(rows):
        for j in range(columns):
        
            distances = np.sqrt((x_coords - i)**2 + (y_coords - j)**2) # calculate distances, based on https://numpy.org/doc/stable/reference/generated/numpy.meshgrid.html 
            mask = (distances <= lambda_over_d*2) & (distances > lambda_over_d) # create mask for circular region surrounding pixel of interest aka pixel whose STD is currently being computed

            pixel_subset = data_array[:, mask] # extract the local region using the circular mask

            ##print(f"Number of pixels in the mask for specific position {i},{j}: {np.sum(mask)}") #used for troubleshooting, when the script
            ## was originally made the size of the circular mask was questionable as well as the accuracy for STDs of pixels located at border locations

            std_of_pixel_subset = np.nanstd(pixel_subset) # Calculate the standard deviation for the local region, excluding nan values
            std_array[i, j] = std_of_pixel_subset # Store the standard deviation in the array
    return std_array


folder_path = '' #folder containing all of the RDI .fits files
output_folder = '' #folder to store all of the STD .fits files
# Iterate through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.fits'):
        file_path = os.path.join(folder_path, filename) #folder path and filename
        base_filename = os.path.splitext(filename)[0] #extract just filename
        
        # Perform the standard deviation calculation
        data_array, header = fits_to_numpy_array(file_path)
        frames, rows, columns = find_dimensions(data_array)
        wavelength = 4.5e-6  # example wavelength in meters; this is what was used for our paper
        aperture_in_meters = 5.2  # example aperture in meters; this was used for our paper
        lambda_over_d = find_lambda_over_d(wavelength, aperture_in_meters)
        std_array = find_standard_deviation(data_array, lambda_over_d, rows, columns)
        # Define the output path based on the base filename and the output folder
        output_fits_path = os.path.join(output_folder, f'{base_filename}-std.fits')
        
        # Save the standard deviation array to a new .fits file
        std_array_hdulist = fits.PrimaryHDU(std_array, header)
        std_array_hdulist.writeto(output_fits_path, overwrite=True)
        
        # Print a message indicating the completion of the calculation
        print(f"Finished calculating std for {output_fits_path}")
