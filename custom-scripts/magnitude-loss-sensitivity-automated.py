"""
Klaus Stephenson
Created January, 2024

Description: infinity-std.py but automates to intake .fits files from a given folder
check infinity-std.py for better (or just in general) documentation

note: 'STD(s)' is my lingo for standard deviation calculation
"""
import os
import numpy as np
from astropy.io import fits

def fits_to_numpy_array(file_path):
    """convert inputed .fits file to a workable format

    Args:
        file_path (string): complete path to file in question

    Returns:
        data_array: the x and y values for our array, used to calculate standard deviation
        header: needed for when we create a new HDU later filled with the calculated std values
    """
    with fits.open(file_path) as hdulist:
        data_array = hdulist[0].data
        header = hdulist[0].header # need the header for when we create a new HDU later with computed STDs
    return data_array, header

#science parameters
sigma_contrast = 5 # in sigma units
stellar_flux = 68747.44677595097 # taken from analysis.py in line 324 where i print the value of variable offaxis_peak_flux

def array_operations(data_array, sigma_contrast, stellar_flux):
    # empty numpy array to store calculated std values in
    sigmaed_array = data_array * sigma_contrast # multiplied by 5
    fluxed_array = sigmaed_array / stellar_flux # divided by peak stellar offaxis flux
    magnitude_sensitive_array = -2.5 * np.log10(fluxed_array) # now make it magnitude units
    return magnitude_sensitive_array

folder_path = ''
ci_output_folder = ''
sl_output_folder = ''

for filename in os.listdir(folder_path):
    if filename.endswith('.fits'):
        file_path = os.path.join(folder_path, filename)
        base_filename = os.path.splitext(filename)[0] #filename extraction
        
        # Perform the array operations on the current file
        data_array_of_interest, header_of_interest = fits_to_numpy_array(file_path)
        STD_of_control = ''
        data_array_of_control, header_of_control = fits_to_numpy_array(STD_of_control)
        post_operations_STD_of_interest = array_operations(data_array_of_interest, sigma_contrast, stellar_flux)
        post_operations_control_STD= array_operations(data_array_of_control,sigma_contrast, stellar_flux)
        
        # Calculate the sensitivity loss
        sensitivity_loss = np.array(post_operations_control_STD) - np.array(post_operations_STD_of_interest)

        ci_output_path = os.path.join(ci_output_folder, f'{base_filename}-CI.fits')
        sl_output_path = os.path.join(sl_output_folder, f'{base_filename}-MSL-control-20.fits')
        
        # Save post-standard deviation operations array to a new .fits file
        contrast_image = fits.PrimaryHDU(post_operations_STD_of_interest, header_of_interest)
        contrast_image.writeto(ci_output_path, overwrite=True)
        print(f"done computing CI for {base_filename}")
        
        # Save the sensitivity loss to a new .fits file
        sensitivity_loss_image = fits.PrimaryHDU(sensitivity_loss, header_of_interest)
        sensitivity_loss_image.writeto(sl_output_path, overwrite=True)
        print(f"done computing SL for {base_filename}")
