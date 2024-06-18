"""
Klaus Stephenson
Created December, 2023
Description: this script is an early rendition of the magnitude-loss-sensitivity script but may be helpful for some.

this script proceeds as follow (to be updated with annotations):
1. takes two folders, finds all .fits files within them
2. stacks .fits file within a folder into a singular .fits file
3. divides first folder's stacked .fits file by second folder's stacked .fits file
4. resultant division of stacked .fits file is saved under new file name

"""

from astropy.io import fits
import numpy as np
import os

def stack_fits_files(folder_path):
    fits_files = [f for f in os.listdir(folder_path) if f.endswith('.fits')]

    if not fits_files:
        print(f"No .fits files found in the folder: {folder_path}")
        return None
    stacked_data = None
    for file_name in fits_files:
        print(f"Processing file: {file_name}")
        with fits.open(os.path.join(folder_path, file_name)) as hdul:
            try:
                data = hdul[0].data
                if data is None:
                    print(f"Error: No data found in file: {file_name}")
                    continue
                print(f"Data shape: {data.shape}")
                if stacked_data is None:
                    stacked_data = data
                else:
                    stacked_data += data
            except Exception as e:
                print(f"Error reading file: {file_name}: {e}")

    print(f"Number of .fits files found: {len(fits_files)}")
    if stacked_data is not None:
        print(f"Stacked data shape: {stacked_data.shape}")
    return stacked_data



def divide_and_save(fits_folder1, fits_folder2, output_filename):
    stack1 = stack_fits_files(fits_folder1)
    stack2 = stack_fits_files(fits_folder2)

    if stack1 is None or stack2 is None:
        print("Error: Unable to stack .fits files.")
        return

    divided_data = np.divide(stack1, stack2)
    
    hdu = fits.PrimaryHDU(divided_data)
    hdu.writeto(output_filename, overwrite=True)
    print(f"Division result saved to {output_filename}")

#running
folder_path1 = ''
folder_path2 = ''
output_file = 'folder-one-divided-by-folder-two'
divide_and_save(folder_path1, folder_path2, output_file)