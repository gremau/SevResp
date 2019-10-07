"""
This module loads (and partially cleans) datalogger data from the EDGE project
"""

import sys
sys.path.append('/home/greg/GitHub/')
import sawyer.io as sio
import numpy as np
import pandas as pd
import os

# Path to the files on greg's computer
#dpath = '/home/greg/GD_gregmaurer/Sev Soil Respiration Data/EDGE_Black_SoilSensorDat/'

def black_soil(dpath):
    """
    Load multiple datalogger files (TOA5 format) and join into one large
    dataframe
    """
    # Get the files with CO2 sensor data
    co2_1 = os.path.join(dpath, 'EDGE_Black_CR1000_1_co2.dat')
    co2_1 = sio.load_toa5(co2_1, skiprows=[200320,])
    co2_2 = os.path.join(dpath, 'EDGE_Black_CR1000_2_co2.dat')
    co2_2 = sio.load_toa5(co2_2, skiprows=[199549,])
    # join into one dataframe
    co2 = co2_1.join(co2_2, how='outer',rsuffix='_2')
    # Clean out the periods where sensors out for calibration
    co2[co2 > 5500] = np.nan
    
    # Get the files with VWC data (then join)
    vwc_1 = os.path.join(dpath, 'EDGE_Black_CR1000_1_vwc.dat')
    vwc_1 = sio.load_toa5(vwc_1, skiprows=[200322,])
    vwc_2 = os.path.join(dpath, 'EDGE_Black_CR1000_2_vwc.dat')
    vwc_2 = sio.load_toa5(vwc_2, skiprows=[199549,])
    vwc = vwc_1.join(vwc_2, how='outer',rsuffix='_2')
    # Get the files with soil temperature data (then join)
    ts_1 = os.path.join(dpath, 'EDGE_Black_CR1000_1_temp.dat')
    ts_1 = sio.load_toa5(ts_1, skiprows=[200327,])
    ts_2 = os.path.join(dpath, 'EDGE_Black_CR1000_2_temp.dat')
    ts_2 = sio.load_toa5(ts_2, skiprows=[199546,])
    ts = ts_1.join(ts_2, how='outer',rsuffix='_2')
    # Get the met file (only the pressure data needed for now...)
    met_2 = os.path.join(dpath, 'EDGE_Black_CR1000_2_met.dat')
    met_2 = sio.load_toa5(met_2, skiprows=[185100,])
    bp = met_2.loc[:,'bPressure_Avg']
    
    # Add more cleaning steps??
    
    # Join all these into one large dataframe
    out = co2.join(vwc, how='outer', rsuffix='_2')
    out = out.join(ts, how='outer', rsuffix='2')
    out = out.join(bp, how='outer', rsuffix='2')
    
    return out
    
    