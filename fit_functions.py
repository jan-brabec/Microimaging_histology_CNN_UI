# Libraries
import os
from scipy import io
import numpy as np

def R2(y_meas,y_pred): #Computes R2 matrix
  return 1 - np.var(y_meas-y_pred)/(np.var(y_meas))

def set_plot_lims(contrast, sample):   #Set lims for the type of image
    sample = int(sample) #make sure it is integer
    
    if contrast == 'FAIP':
       lims = np.array([0, 0.8])
       dif_lims = np.array([-lims[1]/2,lims[1]/2])
    elif contrast == 'MD':
        if sample == 3:
            lims = np.array([0, 2])
        else:
            lims = np.array([0, 1])
           
    dif_lims = np.array([-0.5,0.5])
       
    return lims, dif_lims

def calculate_diff_map(I_measured,I_predicted):
    
    I_diff = I_measured - I_predicted
    
    return I_diff

def clean_diff_map(I_diff,ROI,dif_lims):
    
    I_diff[ROI==1 & (I_diff >= dif_lims[1])] = dif_lims[1]
    I_diff[ROI==1 & (I_diff <= -dif_lims[1])] = -dif_lims[1]
    I_diff[ROI==0] = dif_lims[1]+10
    
    return I_diff

def load_data(sample): #load measured data
    
    sample = sample - 1 #because it starts with 0s
    path = os.path.join(os.path.split(os.getcwd())[0],"microimaging_vs_histology_in_meningeomas","Step_e_Manuscript_figures")
    
    summary = io.loadmat(os.path.join(path,"summary.mat"))
    
    sMD_CNN =  summary.get("sMD_CNN")
    sMD_CNN = sMD_CNN[0,sample]
    
    I_meas_MD  = sMD_CNN["I_measured"][0,0]
    I_pred_MD  = sMD_CNN["I_pred"][0,0]
    ts_meas_MD = sMD_CNN["measured"][0,0]
    ts_pred_MD = sMD_CNN["predicted"][0,0]

    sFAIP_CNN =  summary.get("sMD_CNN")
    sFAIP_CNN = sFAIP_CNN[0,sample]
    
    I_meas_FAIP  = sFAIP_CNN["I_measured"][0,0]
    I_pred_FAIP  = sFAIP_CNN["I_pred"][0,0]
    ts_meas_FAIP = sFAIP_CNN["measured"][0,0]
    ts_pred_FAIP = sFAIP_CNN["predicted"][0,0]
    
    sROI = summary.get("sROI")
    ROI = np.array(sROI[0,sample], dtype=bool)
    
    return ts_meas_MD, ts_pred_MD, ts_meas_FAIP, ts_pred_FAIP, I_meas_MD, I_pred_MD, I_meas_FAIP, I_pred_FAIP, ROI


