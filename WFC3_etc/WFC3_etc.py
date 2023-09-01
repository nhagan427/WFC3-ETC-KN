# Programmer: Naomi Hagan
# Purpose: To automate the ETC in a chrome browser 
# Acknowledgements: Niharika Sravan (https://www.niharikasravan.in/cv), Sameeresque (https://github.com/sameeresque), Mattia Bulla (https://github.com/mbulla)

# The user should input the path of their chrome application as binary_location
# The user should input the path of their chrome driver as driver_location

# Necessary built in modules
import numpy as np
from astroquery.ipac.irsa.irsa_dust import IrsaDust
from bs4 import BeautifulSoup
from astropy import units as u
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException
import math
import re
import os

# Other module included as part of this project
import spectrum_data_file as sd

# Specify the locations of chrome application and driver
binary_location="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
driver_location="C:\\Users\\chromedriver.exe"

# Lists of proposed filters for each aperture of WFC3 - used to determine which website to go to
uvis_filters = ['F225W', 'F275W', 'F336W', 'F475W', 'F606W', 'F625W', 'F775W', 'F814W', 'F850LP']
ir_filters = ['F160W', 'F140W', 'F110W']

# Function which should be called in the main program
def run_etc(filter, num_exp, extract_reg, spectrum_file, extinction_rel, redshift, extinct_val, snr='default', exp_time='default'):
    try:
        # Selenium jargon
        options=Options()

        options = webdriver.ChromeOptions()
        options.binary_location = binary_location

        service = webdriver.chrome.service.Service(driver_location)

        service.start()

        driver = webdriver.Chrome(service=service, options=options)

        # Automation starts here

        # IR Specification
        if filter in ir_filters:
            driver.get("https://etc.stsci.edu/etc/input/wfc3ir/imaging/")

            # Selecting the filter
            select = Select(driver.find_element("name",'irfilt0'))
            select.select_by_value(filter)

        # UV Specification
        elif filter in uvis_filters:
            driver.get("https://etc.stsci.edu/etc/input/wfc3uvis/imaging/")

            # Selecting the filter
            select = Select(driver.find_element("name",'wfc3_filter_w'))
            select.select_by_value(filter)

        # Selecting number of independent exposures
        num_exp_default = driver.find_element("name", 'crsplit')
        num_exp_default.clear()
        val = num_exp
        num_exp_default.send_keys('{}'.format(val))

        # Determines whether user is calculating for SNR or exposure time
        if exp_time == 'default':
            # Inputting the S/N ratio
            driver.find_element("xpath",".//input[@type='radio' and @value='SNR']").click()

            snr_default = driver.find_element("name", 'SNR')
            snr_default.clear()
            val = snr
            snr_default.send_keys('{}'.format(val))

        elif snr == 'default':
            # Inputting the Exposure Time
            driver.find_element("xpath",".//input[@type='radio' and @value='Time']").click()

            exp_time_default = driver.find_element("name", 'Time')
            exp_time_default.clear()
            val = exp_time
            exp_time_default.send_keys('{}'.format(val))
        
        # Selecting extraction region
        driver.find_element("xpath",".//input[@type='radio' and @value='point']").click()

        # Square Extraction Region Specification
        if extract_reg[0].upper() == 'SQUARE':
            driver.find_element("xpath",".//input[@type='radio' and @value='Square']").click()
            
            select = Select(driver.find_element("name",'extractionRegionSquare'))
            select.select_by_value('{}'.format(extract_reg[1]))

        # Circular Extraction Region Specification
        elif extract_reg[0].upper() == 'CIRCLE':
            driver.find_element("xpath",".//input[@type='radio' and @value='UserCircle']").click()

            blank = driver.find_element("name", 'extractionRegionUserCircle')
            blank.clear()
            blank.send_keys('{}'.format(extract_reg[1]))

        # Also Circular, but dependent on total light, not radius
        else:
            driver.find_element("xpath",".//input[@type='radio' and @value='VariableCircle']").click()

            blank = driver.find_element("name", 'extractionRegionVariableCircle')
            blank.clear()
            blank.send_keys('{}'.format(extract_reg[1]))

        # Selecting Upload Spectrum File
        driver.find_element("xpath",".//input[@type='radio' and @value='SpectrumUpload']").click()
        file_input = driver.find_element("name", 'fUploadFile')
        file_path = sd.new_file_path + spectrum_file
        file_input.send_keys(file_path)

        # Selecting the extinction relationship
        select=Select(driver.find_element("name",'febmvtype'))
        select.select_by_value(extinction_rel)

        # Inputting the extinction value and applying it before normalization
        febv=driver.find_element("name",'febv')
        febv.clear()
        febv.send_keys('{}'.format(extinct_val))

        select=Select(driver.find_element("name",'fextinctiontype'))
        select.select_by_value('before')

        # Inputting the redshift
        blank = driver.find_element("name", 'fRedshift')
        blank.clear()
        blank.send_keys('{}'.format(redshift))

        # Normalizing the target's flux. This is done within the spectrum file so we will not be renormalizing
        driver.find_element("xpath",".//input[@type='radio' and @value='fno']").click()
        
        # Background levels for Zodiacal Light, Earth Shine, and Air Glow/Helium, all are set to Averages.
        driver.find_element("xpath",".//input[@type='radio' and @value='ZodiStandard']").click()
        select=Select(driver.find_element("name",'ZodiStandard'))
        select.select_by_value('Average')

        # Earth Shine
        driver.find_element("xpath",".//input[@type='radio' and @value='EarthshineStandard']").click()
        select=Select(driver.find_element("name",'EarthshineStandard'))
        select.select_by_value('Average')

        if filter in ir_filters:
            # IR includes helium standard
            select=Select(driver.find_element("name",'HeliumStandard'))
            select.select_by_value('None')

        elif filter in uvis_filters:
            # UV includes air glow standard
            select=Select(driver.find_element("name",'AirglowStandard'))
            select.select_by_value('Average')

        # Submit Calculation
        driver.find_element("xpath",".//input[@type='button' and @value='Submit Simulation']").click()
        
        # Read the result and find SNR/exp_time
        soup = BeautifulSoup(driver.page_source,"lxml")
        ps=soup.find_all('p')
        requestid = int(re.findall(r'\d+', ps[0].text)[1])
        
        time = ps[2].string.split(' ')[3]

        # String to float
        try:
            timeonsource = float(time.split(',')[0]+time.split(',')[1])
        except:
            timeonsource = float(time)
            
        return requestid, timeonsource

    # Just in case
    except (UnexpectedAlertPresentException,AttributeError) as e:
        print ("Error: ", e)
        return np.nan


