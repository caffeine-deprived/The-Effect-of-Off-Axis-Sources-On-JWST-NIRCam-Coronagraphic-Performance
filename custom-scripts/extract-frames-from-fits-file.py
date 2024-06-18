"""
Klaus Stephenson
Created January, 2024

Description: Used for troubleshooting, the RDI versus STD versus magnitude-sensitivity loss .fits files can have different dimensions making
them confusing to work with sometimes
"""

from astropy.io import fits
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import numpy as np

fits_file = ''
with fits.open(fits_file) as hdulist:
    try:
        frames = hdulist[1].data # Assuming there are frames in the second dimension since the first tends to just be the header
    except IndexError as e: #error handling 
        print(f"Error accessing frame data: {e}")
        print("FITS file may not have the expected structure. Maybe frames are in the first dimension?")
        hdulist.info()  # Print header information for debugging
    print(f"Frames shape: {frames.shape if frames is not None else None}")
