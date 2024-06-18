"""
Klaus Stephenson
Created January, 2024

Description: Used for troubleshooting, the RDI versus STD versus magnitude-sensitivity loss .fits files can have different dimensions making
them confusing to work with sometimes
"""
from astropy.io import fits
import numpy as np

def find_dimensions(fits_file_path):
    data = fits.getdata(fits_file_path)
    numpy_array = np.array(data)
    num_dimensions = numpy_array.ndim

    if num_dimensions == 2:
        num_rows, num_columns = numpy_array.shape
        print(f"Number of rows: {num_rows}")
        print(f"Number of columns: {num_columns}")
    elif num_dimensions == 3:
        num_frames, num_rows, num_columns = numpy_array.shape
        print(f"Number of frames: {num_frames}")
        print(f"Number of rows per frame: {num_rows}")
        print(f"Number of columns per frame: {num_columns}")
    else:
        print(f"The array has {num_dimensions} dimensions. Adjust the code accordingly.")

file = ''
find_dimensions(file)