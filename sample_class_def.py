"""
Defines the class structure for the data, loads them into proper variables
and computes some missing fields

Some functions stored in fit_function.py

"""

import os
import h5py
from scipy import io
import numpy as np
from fit_functions import *

class c_sample:

    def __init__(self,sample): #no inheritance here, load data
        self.ts_meas_MD, \
        self.ts_pred_MD, \
        self.ts_meas_FAIP, \
        self.ts_pred_FAIP, \
        self.I_meas_MD, \
        self.I_pred_MD, \
        self.I_meas_FAIP, \
        self.I_pred_FAIP, \
        self.ROI = load_data(sample)
        
        
        #Calculate few missing features
        self.test_R2_MD = R2(self.ts_meas_MD, self.ts_pred_MD)
        self.test_R2_FAIP = R2(self.ts_meas_FAIP, self.ts_pred_FAIP)
        self.I_diff_MD   = calculate_diff_map(self.I_meas_MD,self.I_pred_MD)
        self.I_diff_FAIP = calculate_diff_map(self.I_meas_FAIP,self.I_pred_FAIP)
        self.I_diff_MD   = clean_diff_map(self.I_diff_MD,self.ROI,set_plot_lims('MD',sample-1)[1])
        self.I_diff_FAIP = clean_diff_map(self.I_diff_FAIP,self.ROI,set_plot_lims('FAIP',sample-1)[1])
    
    def get_lims(self,contrast,sample):
        self.lims, self.dif_lims = set_plot_lims(contrast,sample)
        return self.lims, self.dif_lims

