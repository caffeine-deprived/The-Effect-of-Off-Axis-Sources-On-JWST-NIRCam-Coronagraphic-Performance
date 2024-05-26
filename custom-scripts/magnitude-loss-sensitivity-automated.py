""" 
Klaus Stephenson
Created May, 2024

Description: A basic PanCAKE script utilized to make individual simulations if say something was improperly calculated, needed double checking,
or if one of the automated scripts forgot something
"""
#importation of non-PANCake packages
import os
import numpy as np
from astropy.io import fits

#fits file to np.array()
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

#science parameters
sigma_contrast = 5 # in sigma units
stellar_flux = 68747.44677595097 # this is the peak_offaxis flux which can be found in pancake.analysis.py in line 324, add line print(offaxis_peak_flux)

def array_operations(data_array, sigma_contrast, stellar_flux):
    """
    this function performs basic array operations needed to find the magnitude sensitivity loss

    Args:
        data_array (numpy array): the .fits file that was converted into a usable array using fits_to_numpy_array()
        sigma_contrast (int): contrast number in sigma units
        stellar_flux (int): peak_offaxis flux
    Returns:
        magnitude_sensitive_array (numpy array): array that is at 5 sigma contrast normalized to peak offaxis 
        flux of on-axis source
    """
    # empty numpy array to store calculated std values in
    sigmaed_array = data_array * sigma_contrast # multiplied by 5
    fluxed_array = sigmaed_array / stellar_flux # divided by peak stellar offaxis flux
    magnitude_sensitive_array = 2.5 * np.log10(fluxed_array) # now make it magnitude sensitive
    return magnitude_sensitive_array

folder_path = '' #base folder with all the STD .fits files
contrast_image_output_folder = '' #where to put files that have undergone the array_operations()
magnitude_sensitivity_loss_folder = '' #where to put files that represent magnitude sensitivity loss

for filename in os.listdir(folder_path):
    if filename.endswith('.fits'):
        file_path = os.path.join(folder_path, filename) # Construct the full file path
        base_filename = os.path.splitext(filename)[0] #Extract the base filename without extension
        
        # Perform the array operations for the current file
        data_array_of_interest, header_of_interest = fits_to_numpy_array(file_path)

        #now do the same for the control scenario which will be our baseline for how much sensitivity loss there is
        STD_of_control = ''
        data_array_of_control, header_of_control = fits_to_numpy_array(STD_of_control)
        post_operations_STD_of_interest = array_operations(data_array_of_interest, sigma_contrast, stellar_flux)
        post_operations_control_STD= array_operations(data_array_of_control,sigma_contrast, stellar_flux)
        
        # Calculate the fractional change
        magnitude_sensitivity_loss = np.array(post_operations_STD_of_interest) - np.array(post_operations_control_STD)
        
        # Define the output paths based on the base filename and the output folders
        contrast_image_output_folder = os.path.join(contrast_image_output_folder, f'{base_filename}-CI.fits') #CI = contrast image
        magnitude_sensitivity_loss_image_output_folder = os.path.join(magnitude_sensitivity_loss_folder, f'{base_filename}-MSL.fits') #MSL = magnitude sensitivity loss
        
        # Save the contrast image (CI) to a new .fits file
        contrast_image = fits.PrimaryHDU(post_operations_STD_of_interest, header_of_interest)
        contrast_image.writeto(contrast_image_output_folder, overwrite=True)
        print(f"Done computing CI for {base_filename}")
        
        # Save the magnitude sesnsivity loss (MSL) to a new .fits file
        magnitude_sensitivity_loss_image = fits.PrimaryHDU(magnitude_sensitivity_loss, header_of_interest)
        magnitude_sensitivity_loss_image.writeto(magnitude_sensitivity_loss_image_output_folder, overwrite=True)
        print(f"Done computing MSL for {base_filename}")
