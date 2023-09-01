# Programmer: Naomi Hagan
# Purpose: To create machine learning training data sets from Mattia Bulla's synthetic sources and STScI's WFC3 UVIS ETC
# Acknowledgements: Niharika Sravan (https://www.niharikasravan.in/cv), Sameeresque (https://github.com/sameeresque), Mattia Bulla (https://github.com/mbulla)

# Main program that takes two specialized modules (spectrum_data_file and WFC3_etc) and creates the data sets

# Necessary modules
from time import *
import os
import spectrum_data_file as sd
import WFC3_etc

'''
spectrum_data_file:

    file_path
        user should paste the path to the raw spectrum files
    new_file_path
        user should paste the path to where the processed spectrum files should be written

    get_file(file_name, t_obs, view_ang, distance)
        input   - name of Bulla file, time of observation, observation angle, observation distance
        process - sorts through Bulla file to find the correct values and then scales them with distance
        output  - tuple: (upload_file, n_photons, m_ejecta, phi, t0, t_obs, view_ang, distance)


etc_wfc3IR:

    binary_location
        user should paste the path to their chrome application
    driver_location
        user should paste the path to the chrome driver

    run_etc(filter_, num_exp, extract_reg, spectrum_file, extinction_rel, extinct_val, redshift, exp_time/SNR)
        input   - filter_, number of independent exposures, extraction region (size and shape), spectrum file, 
                exinction relation, extinction value, redshift, SNR OR exp_time
        process - takes all inputs from above and puts them into the wfc3 etc website
        output  - tuple: (request ID, exposure time/SNR)
'''

# Timing
start = time()

# File in which the training set will be written
file_path = "uvis_training_set.txt"

# If the file doesn't exist, we create it
if not os.path.exists(file_path):
    with open(file_path, 'w') as file:
        file.write('n_photons,m_ejecta,phi,t0,t_obs,view_ang,distance,filter,num_exp,extract_reg_type,extract_reg_size,extinction_rel,extinct_val,redshift,exp_time,snr\n')
    final_entries = []
# If it does exist we read it to see which entries already exist
else:
    with open(file_path, 'r') as file:
        entries = file.readlines()
        final_entries = []
        for entry in entries:
            elements = entry.split(',')
            del elements[-1]
            modified_entry = ','.join(elements)
            final_entries.append(modified_entry)

# Unchanging parameters
extract_reg = ['percent', 90]
extinct_rel = 'mwavg'

# Shortened Iterative Parameters
m_ejecta_list = [0.02, 0.06, 0.10]
phi_list = [0, 30, 60, 90]
obs_ang_list = [0, 0.3, 0.5, 0.7, 1]
t_obs_list = [6, 8, 10, 12, 14]
distance_list = [40, 100, 140, 200]
uvis_filters = ['F225W', 'F475W', 'F625W', 'F850LP']
extinct_val_list = [0, 1, 2, 3, 4]
exp_time_list = [300, 1400, 2500, 3600]

'''
# All Iterative Parameters
m_ejecta_list = [0.02, 0.04, 0.06, 0.08, 0.10]
phi_list = [0, 15, 30, 45, 60, 75, 90]
obs_ang_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
t_obs_list = [6, 8, 10, 12, 14]
distance_list = [40, 100, 140, 200]
uvis_filters = ['F225W', 'F275W', 'F336W', 'F475W', 'F606W', 'F625W', 'F775W', 'F814W', 'F850LP']
extinct_val_list = [0, 1, 2, 3, 4]
exp_time_list = [300, 1400, 2500, 3600]
'''

# This code runs through all parameters
for m_ejecta in m_ejecta_list:
    for phi in phi_list:
        for obs_ang in obs_ang_list:
            for t_obs in t_obs_list:
                for distance in distance_list:
                    for filter_ in uvis_filters:
                        for extinct_val in extinct_val_list:
                            for exp_time in exp_time_list:
                   
                                # Creating a list of inputs
                                inputs = []
                                
                                # An issue with significant figures and calling the correct file
                                if m_ejecta == 0.1:
                                    file = 'nph1.0e+06_mej' + str(m_ejecta) + '0_phi' + str(phi) + '_T5.0e+03.txt'
                                else:
                                    file = 'nph1.0e+06_mej' + str(m_ejecta) + '_phi' + str(phi) + '_T5.0e+03.txt'

                                # From spectrum_data_file
                                file_name = sd.get_file(file, t_obs, obs_ang, distance)

                                # Checking if there is more than one observation angle
                                # spectrum_data_file is coded to return an obs_ang of 0 (file_name[6]) for any model that has only 1 observation angle. 
                                # If this function is trying to input a different observation angle, this if statement catches it, and doesn't run code for any observation angle cos > 0
                                if file_name[6] == obs_ang:

                                    # Lets append inputs to the input list. These are entered directly into the run_etc function
                                    inputs.append(filter_)
                                    inputs.append(1)
                                    inputs.append(extract_reg)
                                    inputs.append(file_name[0])
                                    inputs.append(extinct_rel)
                                    inputs.append(extinct_val)
                                    inputs.append(0)
                                    inputs.append(exp_time)

                                    # Defining output here in order to check if the output already exists in the destination before running the calculation
                                    output = []

                                    # Using indices because input is a keyword
                                    for k in range(1, 8):
                                        output.append(file_name[k])
                                    for k in range(len(inputs)):
                                        if k==2:
                                            output.append(inputs[k][0])
                                            output.append(inputs[k][1])
                                        elif not k==3:
                                            output.append(inputs[k])
                                            
                                    # Creating the string to look for in final_entries
                                    string = ''
                                    for outputs in output:
                                        string += str(outputs) + ','
                                    string = string[:-1]

                                    # Checking if the entry already exists
                                    if string in final_entries:
                                        # If it does, no calculation runs
                                        pass
                                    else:
                                        # If not, we need to calculate it
                                        snr = WFC3_etc.run_etc(filter=inputs[0], num_exp=inputs[1], extract_reg=inputs[2], 
                                                                    spectrum_file=inputs[3], extinction_rel=inputs[4], extinct_val=inputs[5], 
                                                                    redshift=inputs[6], exp_time=inputs[7])
                                        output.append(snr[1])

                                        # Writing the calculated entry into the training set file
                                        with open(file_path, "a") as file:
                                            for k in range(len(output)):
                                                if k == (len(output)-1):
                                                    file.write(str(output[k]))
                                                    file.write('\n')
                                                else:
                                                    file.write(str(output[k]))
                                                    file.write(',')
                                                   
# End timing and print elapsed time
end = time()
print(f'Time taken: {end-start}')
