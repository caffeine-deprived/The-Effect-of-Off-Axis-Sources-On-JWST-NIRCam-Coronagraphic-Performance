"""
Klaus Stephenson
Created May, 2024

Description: exact same as automatic-sensitivity-loss-magnitude-scenarios.py but with tweaks
Find global/total sensitivity loss and local sensitivity loss for position angle scenarios.

you may be asking why is this a separate script from the magnitude script?
the answer is: this script was made in the dead of night during an observation run
and I have been too lazy since to combine the two.
"""
import os
from astropy.io import fits
import numpy as np

def fits_to_numpy_array(file_path): #what the title says
    with fits.open(file_path) as hdulist:
        data_array = hdulist[0].data
        header = hdulist[0].header
    return data_array, header

def find_dimensions(data_array): #for troubleshooting
    if data_array.ndim == 2:
        rows, columns = data_array.shape
    elif data_array.ndim == 3:
        _, rows, columns = data_array.shape
    else:
        raise ValueError("err! wrong dimensions.")
    return rows, columns

def find_max_loss(data_array): 
    average = np.average(data_array) #just the average of your input data array values
    return average

def find_local_loss(data_array, x_location, y_location, arcsec_per_pixel=0.063): 
    rows, columns = data_array.shape if data_array.ndim == 2 else data_array.shape[1:]
    x_coords, y_coords = np.meshgrid(np.arange(columns), np.arange(rows))
    distances = np.sqrt((x_coords - x_location)**2 + (y_coords - y_location)**2)
    radius_pixels = 1 / arcsec_per_pixel
    mask = distances <= radius_pixels
    pixel_subset = data_array[mask]
    average_loss = np.average(pixel_subset)
    return average_loss

def get_coordinates(arcsecond_offset, theta_offset):
    #because we are considering position angle we care about change in x and y axis and change in separation
    if theta_offset == '0':
        coordinates = {
            '0.5': (50.5, 42.56  ),
            '1': (50.5, 34.62  ),
            '1.5': (50.5, 26.69  ),
            '2': (50.5, 18.75  ),
            '2.5': (50.5, 10.81  ),
            '3': (50.5, 2.88  )
        }
    elif theta_offset == '45':
        coordinates = {
            '0.5': (44.88915, 44.88915),
            '1': (39.29, 39.29),
            '1.5': (33.6674, 33.6674),
            '2': (28.0566, 28.0566),
            '2.5': (22.445, 22.445),
            '3': (16.8349, 16.8349)
        }
    elif theta_offset == '90':
        coordinates = {
            '0.5': (42.56, 50.5),
            '1': (34.62, 50.5),
            '1.5': (26.69, 50.5),
            '2': (18.75, 50.5),
            '2.5': (10.81, 50.5),
            '3': (2.88, 50.5)
        }
    elif theta_offset == '135':
        coordinates = {
            '0.5': (44.88915, 56.11),
            '1': (39.29, 61.7217),
            '1.5': (33.6674, 67.33255),
            '2': (28.0566, 72.9434),
            '2.5': (22.445, 78.55425),
            '3': (16.8349, 84.1651)
        }
    elif theta_offset == '180':
        coordinates = {
            '0.5': (50.5, 58.4365  ),
            '1': (50.5, 66.373  ),
            '1.5': (50.5, 74.309  ),
            '2': (50.5, 82.24  ),
            '2.5': (50.5, 90.182  ),
            '3': (50.5, 98.119  )
        }
    elif theta_offset == '225':
        coordinates = {
            '0.5': (56.11, 56.11),
            '1': (61.7217, 61.7217),
            '1.5': (67.33255, 67.33255),
            '2': (72.9434, 72.9434),
            '2.5': (78.55425, 78.55425),
            '3': (84.1651, 84.1651)
        }
    elif theta_offset == '270':
        coordinates = {
            '0.5': (58.4365, 50.5),
            '1': (66.373, 50.5),
            '1.5': (74.309, 50.5),
            '2': (82.24, 50.5),
            '2.5': (90.182, 50.5),
            '3': (98.119, 50.5)
        }
    elif theta_offset == '315':
        coordinates = {
            '0.5': (56.11, 44.88915),
            '1': (61.7217, 39.29),
            '1.5': (67.33255, 33.6674),
            '2': (72.9434, 28.0566),
            '2.5': (78.55425, 22.445),
            '3': (84.1651, 16.8349)
        }
    else:
        raise ValueError("err! wrong theta value")
    return coordinates.get(arcsecond_offset, (None, None))


def process_files(directory):
    results = []
    for filename in os.listdir(directory):
        if filename.endswith(".fits"):
            parts = filename.split('-')
            r_value = parts[2][1:]  
            theta_value = parts[5][5:] 
            x_location_of_companion, y_location_of_companion = get_coordinates(r_value, theta_value)
            if x_location_of_companion is not None and y_location_of_companion is not None:
                file_path = os.path.join(directory, filename)
                data_array, header = fits_to_numpy_array(file_path)
                max_loss = round(find_max_loss(data_array), 2)
                local_loss = round(find_local_loss(data_array, x_location_of_companion, y_location_of_companion, arcsec_per_pixel=0.063), 2)
                results.append((float(r_value), int(theta_value), filename, max_loss, local_loss))
            else:
                print(f"wrong coords for: {filename}")

    results.sort(key=lambda x: (x[0], x[1], x[2])) 
    write_to_txt_file(results, 'output-rots.txt')

def write_to_txt_file(results, filename):
    def write_section(file, section_name, loss_values):
        degrees = sorted(set(row[1] for row in loss_values))
        r_values = sorted(set(row[0] for row in loss_values))

        header = "\t" + "\t".join([f"{r}\"" for r in r_values]) + "\n"
        file.write(header)

        for degree in degrees:
            file.write(f"{section_name} for {degree} degrees\n")
            degree_values = [row for row in loss_values if row[1] == degree]
            line = ", ".join([f"{row[4] if section_name == 'Local Loss' else row[3]}" for row in degree_values])
            file.write(f"{line}\n")

    local_loss_values = [row for row in results]
    total_loss_values = [row for row in results]

    with open(filename, 'w') as file:
        write_section(file, "local loss", local_loss_values)
        file.write("\n")
        write_section(file, "total loss", total_loss_values)

directory = ''
process_files(directory)