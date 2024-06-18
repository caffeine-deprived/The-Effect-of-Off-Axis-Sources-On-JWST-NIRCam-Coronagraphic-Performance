""" 
Klaus Stephenson
Created December, 2024

Description: Use in the case of wanting to trim fits files by a few pixels if there was a discrepancy due to calculations made
for example, target and reference .fits files are 101px by 101px, and the STD .fits file corresponding to that PanCAKE data could be 100px by 98px
"""
import numpy as np
from astropy.io import fits

def remove_border_rows(input_fits_path, output_fits_path, top=0, bottom=0, left=0, right=0):
    """
    Remove a specified number of rows from each side of the image.

    Parameters:
        input_fits_path (str): Path to the input FITS file.
        output_fits_path (str): Path to the output FITS file.
        top (int): Number of rows to remove from the top, default is 0
        bottom (int): Number of rows to remove from the bottom, default is 0
        left (int): Number of columns to remove from the left, default is 0
        right (int): Number of columns to remove from the right, default is 0
    """
    # Load the original FITS file
    hdulist = fits.open(input_fits_path)
    original_data = hdulist[0].data

    # Remove specified number of rows/columns from each side
    cropped_data = original_data[top:-bottom, left:-right]

    # Save the cropped data to a new FITS file
    fits.writeto(output_fits_path, cropped_data, overwrite=True)

# Example usage:
input_fits_path = ''
output_fits_path = ''

# example removing 10 rows from the top and 5 rows from the bottom
remove_border_rows(input_fits_path, output_fits_path, top=10, bottom=5)
