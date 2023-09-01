# Programmer: Naomi Hagan
# Purpose: To sort and return spectra information from Bulla synthetic sources
# Acknowledgements: Niharika Sravan (https://www.niharikasravan.in/cv), Sameeresque (https://github.com/sameeresque), Mattia Bulla (https://github.com/mbulla)

# The user should input the path of the Bulla file repository as file_path
# The user should input the destination path of the resulting ETC compatible file

# Necessary built in modules
import os
import numpy
import math
import pandas
import re

# Specify the locations of the paths detailed above
file_path = 'C:\\Users\\HP\\Desktop\\STAR Scholars\\Research Things\\Browser Automation Codes\\Raw Spectra\\'
new_file_path = 'C:\\Users\\HP\\Desktop\\STAR Scholars\\Research Things\\Browser Automation Codes\\Processed Spectra\\'

# Function which should be called in the main program
def get_file(file_name, t_obs, obs_ang, distance):

    # Extracting intrinsic parameters based on information in the file name
    components = file_name.split('_')
    
    file_info = []
    for component in components:
        match = re.search(r'(\d+(?:\.\d+(?:[eE][+-]?\d+)?)?)', component)
        if match:
            file_info.append(match.group(1))

    # Assigning the intrinsic parameters to variables
    n_photons = file_info[0]
    m_ejecta = file_info[1]
    phi = file_info[2]
    t0 = file_info[3]

    # Obtaining the first 3 lines from each file: number of observation angles, number of wavelength bins, information on time
    with open(file_path + file_name, 'r') as file:
        info_parameters = file.read().splitlines()[:3]
    time_info = info_parameters[2].split()

    n_obs = int(info_parameters[0]) 
    n_wave = int(info_parameters[1])
    n_timebins = int(time_info[0])
    t_i = float(time_info[1])
    t_f = float(time_info[2])

    # Obtaining observation time step
    time_step = (t_f - t_i)/n_timebins

    # Selecting which column of flux to return based on t_obs
    col = (t_obs/time_step)

    # Some Bulla files (phi = 0 and phi = 90) have only 1 observation angle
    if n_obs > 1:
        # For an n_obs = 1, this creates an error hence the if else statement
        obs_ang_step = 1/(n_obs-1)

        # Different observation angles give different fluxes and all the data is contained within the same file so this line sorts through to find the correct chunk of data
        df = pandas.read_csv(file_path + file_name, skiprows=range(round((n_wave*(obs_ang/obs_ang_step))+3)), delimiter=' ', nrows=n_wave, header=None)
    else:
        # Default observation angle
        obs_ang = 0

        # Different observation angles give different fluxes and all the data is contained within the same file so this line sorts through to find the correct chunk of data
        df = pandas.read_csv(file_path + file_name, skiprows=range(3), delimiter=' ', nrows=n_wave, header=None)

    # Flux scaling based on distance
    divisor = ((distance*(10**6))/10)**(2)

    # This takes the data frame created above and selects the proper column of data using numpy arrays
    df_cols = df.iloc[:, [0, col]]
    df_array = df_cols.values

    for i in range(100):
            df_array[i, 1] = df_array[i, 1]/divisor

    scaled_df = pandas.DataFrame(df_array)

    # Creating the name of the file that will be uploaded into the ETC
    upload_file = file_name.split('.txt')[0] + "_at_" + str(t_obs) + "d_at_cos(" + str(obs_ang) + ")deg_at_" + str(distance) + "Mpc.dat"

    # Writing the new file with the data
    scaled_df.to_csv(upload_file, sep=' ', index=False)

    # The new file includes the column names/numbers so these lines remove the first line from the final .dat file
    with open(upload_file, 'r') as file:
        lines = file.readlines()
    lines = lines[1:]
    with open(new_file_path + upload_file, 'w') as file:
        file.writelines(lines)
    os.remove(upload_file)

    return upload_file, n_photons, m_ejecta, phi, t0, t_obs, obs_ang, distance

