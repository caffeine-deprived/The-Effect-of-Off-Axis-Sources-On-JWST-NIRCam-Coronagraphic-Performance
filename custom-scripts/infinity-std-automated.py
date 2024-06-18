
"""
Klaus Stephenson
Created January, 2024

Description: infinity-std.py but automates to intake .fits files from a given folder
check infinity-std.py for better (or just in general) documentation
"""
from math import pi
import numpy as np
from astropy.io import fits
import os

def fits_to_numpy_array(file_path):
    with fits.open(file_path) as hdulist:
        data_array = hdulist[0].data
        header = hdulist[0].header
    return data_array, header

def find_dimensions(data_array):
    frames, rows, columns = data_array.shape
    return frames, rows, columns

def find_lambda_over_d(wavelength, aperture_in_meters):
    lambda_over_d = ((wavelength / aperture_in_meters) * (180 / pi) * 3600) / 0.063
    return lambda_over_d

def find_standard_deviation(data_array, lambda_over_d, rows, columns):
    std_dev_array = np.zeros((rows, columns), dtype=data_array.dtype)
    x_coords, y_coords = np.meshgrid(np.arange(rows), np.arange(columns), indexing='ij')
    for i in range(rows):
        print(f"processing row {i} out of {rows}")
        for j in range(columns):
            distances = np.sqrt((x_coords - i)**2 + (y_coords - j)**2) #euclidean distance aka radius vector
            mask = distances < lambda_over_d 

            pixel_subset = data_array[:, mask]
            std_of_pixel_subset = np.nanstd(pixel_subset)
            std_dev_array[i, j] = std_of_pixel_subset

    return std_dev_array

def process_fits_files(folder_path, output_folder, wavelength, aperture_in_meters):
    for filename in os.listdir(folder_path):
        if filename.endswith('.fits'):
            file_path = os.path.join(folder_path, filename)
            base_filename = os.path.splitext(filename)[0]
            data_array, header = fits_to_numpy_array(file_path)
            frames, rows, columns = find_dimensions(data_array)
            lambda_over_d = find_lambda_over_d(wavelength, aperture_in_meters)
            std_dev_array = find_standard_deviation(data_array, lambda_over_d, rows, columns)

            output_fits_path = os.path.join(output_folder, f'{base_filename}-std.fits')
            std_dev_array_hdulist = fits.PrimaryHDU(std_dev_array, header)
            std_dev_array_hdulist.writeto(output_fits_path, overwrite=True)

            print(f"Finished calculating std for {output_fits_path}")

# Example usage
folder_path = '/'
output_folder = ''
wavelength = 4.5e-6  # example wavelength in meters
aperture_in_meters = 5.2  # example aperture in meters, this is what we used for the paper

process_fits_files(folder_path, output_folder, wavelength, aperture_in_meters)
