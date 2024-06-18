"""
Klaus Stephenson
Created May, 2024

Description: Find global/total sensitivity loss and local sensitivity loss for magnitude scenarios
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

def get_coordinates(arcsecond_offset):
    coordinates = {
        #based on the separation the coords change. this is the magnitude-only script so no need to worry about anything changing
        #in the xhat direction
        '0.0': (50.5, 50.5),
        '0.5': (50.5, 42.56),
        '1.0': (50.5, 34.62),
        '1.5': (50.5, 26.69),
        '2.0': (50.5, 18.75),
        '2.5': (50.5, 10.81),
        '3.0': (50.5, 2.88)
    }
    return coordinates.get(arcsecond_offset, (None, None))

def process_files(directory):
    results = []
    for filename in os.listdir(directory):
        if filename.endswith(".fits"):
            parts = filename.split('-')
            r_value = parts[0][1:]  # r value finder
            m_value = parts[1][1:].replace(",", "")  # m-value finder also remove the commas within it
            x_location_of_companion, y_location_of_companion = get_coordinates(r_value)
            if x_location_of_companion is not None and y_location_of_companion is not None:
                file_path = os.path.join(directory, filename)
                data_array, header = fits_to_numpy_array(file_path)
                print(f"processing: {filename} with m value: {m_value}") #sanity check
                max_loss = round(find_max_loss(data_array), 2)
                local_loss = round(find_local_loss(data_array, x_location_of_companion, y_location_of_companion), 2)
                results.append((float(r_value), int(m_value), filename, max_loss, local_loss))
            else:
                print(f"wrong coords for: {filename}")
    
    results.sort(key=lambda x: (x[1], x[0]))
    write_to_txt_file(results, 'output-mags.txt')

def write_to_txt_file(results, filename):
    def write_section(file, section_name, loss_values): #personal preference since the plotting script
        #corresponding to this for the 'heatmap' plots in the paper took in lists separaed by commas
        m_values = sorted(set(row[1] for row in loss_values))
        r_values = sorted(set(row[0] for row in loss_values))
        header = "\t" + "\t".join([f"{r}\"" for r in r_values]) + "\n"
        file.write(header)
        for m_value in m_values:
            file.write(f"M={m_value}\t")
            m_value_loss = [row for row in loss_values if row[1] == m_value]
            loss_dict = {row[0]: row[4] if section_name == 'Local Loss' else row[3] for row in m_value_loss}
            line = "[" + ", ".join([f"{loss_dict.get(r, 'NaN')}" for r in r_values]) + "],"
            file.write(f"{line}\n")

    local_loss_values = [row for row in results] 
    total_loss_values = [row for row in results]

    with open(filename, 'w') as file:
        file.write("local loss\n")
        write_section(file, "local loss", local_loss_values)
        file.write("\total loss\n")
        write_section(file, "total loss", total_loss_values)

directory = ''
process_files(directory)
