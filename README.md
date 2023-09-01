# WFC3-ETC-KN
All necessary code/modules to splice information from synthetic kilonova sources and then run iterative code through STScI's WFC3 exposure time calculator to produce a training data set.

# Required Packages

* `numpy`
* `astropy`
* `astroquery`
* `bs4`
* `selenium`

# Installing Provided Packages

1. Download both WFC3_etc and spectrum_data_file. 

2. Then enter these commands into the terminal:

```
pip install WFC3_etc
pip install spectrum_data_file
```

3. Download both the Final_WFC3_UVIS.py and Final_WFC3_IR.py files.

4. Download the Raw Spectra. These are synthetic kilonova models designed by [Mattia Bulla](https://github.com/mbulla).

An important thing to note:

These packages require a copy to be in the same directory as the main program.

# User Supplied Changes

## spectrum_data_file

1. Assign file_path to the same path as Raw Spectra. (eg. 'C:\\Users\\USER\\Desktop\\Raw Spectra')

2. Then assign new_file_path as the path where ETC-compatible files should be created and stored.

## WFC3_etc

1. Assign binary_location to the path in which the Chrome browser is installed.

2. Assign driver_location to the path in which the [Chrome driver](https://chromedriver.chromium.org/downloads) is installed.

This package was produced based on code by [Sameeresque](https://github.com/sameeresque).

## Final_WFC3_UVIS and Final_WFC3_IR

Two sets of parameters are included with each file: a shortened set and a full set.

The user should only run the set of parameters they wish to iterate across. The other can be deleted or commented out.
