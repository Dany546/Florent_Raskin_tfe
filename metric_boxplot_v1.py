#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 16 11:20:27 2022

@author: florentraskin
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from fancy_boxplots import fancy_box
from matplotlib.patches import Polygon
from ttest_bp import ttest_bp


root_res = '/Users/florentraskin/Documents/Documents personnels/Thesis/Analysis/'
#ROI = ''
#ROI = '_Cortico_Ponto_Cerebellum/'
#ROI = '_Inferior_Cerebellar_Pedunculus/'
#ROI = '_Superior_Cerebelar_Pedunculus/'
#ROI = '_xtract_prob_Superior_Longitudinal_Fasciculus_1/'
#ROI = '_xtract_prob_Superior_Longitudinal_Fasciculus_2/'
ROI = '_xtract_prob_Superior_Longitudinal_Fasciculus_3/'

def metric_bp(root_results, metric, ROI):
    '''

    Input
    ----------
    File paths to the dictionnaries of the FA metrics for case left & right; control left & right

    Output
    -------
    Boxplots for all of the metrics

    '''    
    print(metric)
    results_dir = root_results + metric + '_analysis_results/' + ROI
    
    
    case_left_filepath = results_dir + 'case_left_' + metric
    case_right_filepath = results_dir + 'case_right_' + metric
    ctrl_left_filepath = results_dir + 'ctrl_left_' + metric
    ctrl_right_filepath = results_dir + 'ctrl_right_' + metric
    
    with open(case_left_filepath + '.json', 'r') as fp:
        case_left_results = json.load(fp)
    
    with open(case_right_filepath + '.json', 'r') as fp:
       case_right_results = json.load(fp)
       
    with open(ctrl_left_filepath + '.json', 'r') as fp:
       ctrl_left_results = json.load(fp)
       
    with open(ctrl_right_filepath + '.json', 'r') as fp:
       ctrl_right_results = json.load(fp)
       
       
    #MEAN METRIC IPSI-LESIONAL
    #Mean metric ipsi case
    mean_metric_ipsi_case_left = case_left_results["mean_metric_ipsi"]
    mean_metric_ipsi_case_right = case_right_results["mean_metric_ipsi"]
    
    
    #Mean metric ipsi ctrl
    mean_metric_ipsi_ctrl_left = ctrl_left_results["mean_metric_ipsi"]
    mean_metric_ipsi_ctrl_right = ctrl_right_results["mean_metric_ipsi"]
    
    #Change scale
    if (metric == 'AD') or (metric == 'MD') or (metric =='RD'):
        for i in range(4):
            
            
            mean_metric_ipsi_case_left[i] = [elem * 1000 for elem in mean_metric_ipsi_case_left[i]]
            mean_metric_ipsi_case_right[i] = [elem * 1000 for elem in mean_metric_ipsi_case_right[i]]
            mean_metric_ipsi_ctrl_left[i] = [elem * 1000 for elem in mean_metric_ipsi_ctrl_left[i]]
            mean_metric_ipsi_ctrl_right[i] = [elem * 1000 for elem in mean_metric_ipsi_ctrl_right[i]]
    
    #Mean metric ipsi tot
    mean_metric_ipsi = [mean_metric_ipsi_case_left[0]+mean_metric_ipsi_case_right[0], mean_metric_ipsi_ctrl_left[0]+mean_metric_ipsi_ctrl_right[0], 
                    mean_metric_ipsi_case_left[1]+mean_metric_ipsi_case_right[1], mean_metric_ipsi_ctrl_left[1]+mean_metric_ipsi_ctrl_right[1],
                    mean_metric_ipsi_case_left[2]+mean_metric_ipsi_case_right[2], mean_metric_ipsi_ctrl_left[2]+mean_metric_ipsi_ctrl_right[2],
                    mean_metric_ipsi_case_left[3]+mean_metric_ipsi_case_right[3], mean_metric_ipsi_ctrl_left[3]+mean_metric_ipsi_ctrl_right[3]]
    
    print(mean_metric_ipsi)
    
    
    #MEAN METRIC CONTRA-LESIONAL
    #Mean metric contra case 
    mean_metric_contra_case_left = case_left_results["mean_metric_contra"]
    mean_metric_contra_case_right = case_right_results["mean_metric_contra"]
    
    
    #Mean metric contra ctrl
    mean_metric_contra_ctrl_left = ctrl_left_results["mean_metric_contra"]
    mean_metric_contra_ctrl_right = ctrl_right_results["mean_metric_contra"]
    
    #Change scale
    if (metric == 'AD') or (metric == 'MD') or (metric == 'RD'):
        for i in range(4):
            
            
            mean_metric_contra_case_left[i] = [elem * 1000 for elem in mean_metric_contra_case_left[i]]
            mean_metric_contra_case_right[i] = [elem * 1000 for elem in mean_metric_contra_case_right[i]]
            mean_metric_contra_ctrl_left[i] = [elem * 1000 for elem in mean_metric_contra_ctrl_left[i]]
            mean_metric_contra_ctrl_right[i] = [elem * 1000 for elem in mean_metric_contra_ctrl_right[i]]

    
    #Mean metric contra tot
    mean_metric_contra = [mean_metric_contra_case_left[0]+mean_metric_contra_case_right[0], mean_metric_contra_ctrl_left[0]+mean_metric_contra_ctrl_right[0],
                      mean_metric_contra_case_left[1]+mean_metric_contra_case_right[1], mean_metric_contra_ctrl_left[1]+mean_metric_contra_ctrl_right[1],
                      mean_metric_contra_case_left[2]+mean_metric_contra_case_right[2], mean_metric_contra_ctrl_left[2]+mean_metric_contra_ctrl_right[2],
                      mean_metric_contra_case_left[3]+mean_metric_contra_case_right[3], mean_metric_contra_ctrl_left[3]+mean_metric_contra_ctrl_right[3]]
    print(mean_metric_contra)
    
    
    
    #RATIO METRIC
    #rmetric case
    rmetric_case_left = case_left_results["rmetric"]
    rmetric_case_right = case_right_results["rmetric"]
    
    
    #rmetric ctrl
    rmetric_ctrl_left = ctrl_left_results["rmetric"]
    rmetric_ctrl_right = ctrl_right_results["rmetric"]
    
    
    #rmetric tot
    rmetric = [rmetric_case_left[0]+rmetric_case_right[0], rmetric_ctrl_left[0]+rmetric_ctrl_right[0], 
                    rmetric_case_left[1]+rmetric_case_right[1], rmetric_ctrl_left[1]+rmetric_ctrl_right[1],
                    rmetric_case_left[2]+rmetric_case_right[2], rmetric_ctrl_left[2]+rmetric_ctrl_right[2],
                    rmetric_case_left[3]+rmetric_case_right[3], rmetric_ctrl_left[3]+rmetric_ctrl_right[3]]
    
    
    
    
    #ASYMMETRY METRIC
    #ametric case
    ametric_case_left = case_left_results["ametric"]
    ametric_case_right = case_right_results["ametric"]
    
    
    #ametric ctrl
    ametric_ctrl_left = ctrl_left_results["ametric"]
    ametric_ctrl_right = ctrl_right_results["ametric"]
    
    
    #Mean metric ipsi tot
    ametric = [ametric_case_left[0]+ametric_case_right[0], ametric_ctrl_left[0]+ametric_ctrl_right[0], 
                    ametric_case_left[1]+ametric_case_right[1], ametric_ctrl_left[1]+ametric_ctrl_right[1],
                    ametric_case_left[2]+ametric_case_right[2], ametric_ctrl_left[2]+ametric_ctrl_right[2],
                    ametric_case_left[3]+ametric_case_right[3], ametric_ctrl_left[3]+ametric_ctrl_right[3]]
    
   
    
    bottom = 0
    top = 1
    rtop = 1.5
    abot = -0.2
    atop = 0.2
    units = ''
    
    if (metric == 'AD'):
        top = 1.2
        units = r'$10^{-3} [\frac{mm^2}{s}$]'
    elif (metric == 'MD') or (metric == 'RD'):
        rtop = 2
        top = 1.6
        abot = -0.4
    elif (metric=='noddi_fextra'):
        rtop = 1.7
        abot = -0.4
    elif (metric == 'noddi_fintra'):
        atop = 0.5
    elif (metric == 'noddi_fiso'):
        rtop = 2.4
        abot = -0.5
    elif (metric == 'mf_fvf_f1'):
        print('yes')
        atop = 0.3
    elif (metric == 'mf_frac_csf'):
        top = 0.4
        rtop = 2.5
        abot = -0.5
    else:
        bottom = 0
        top = 1
        rtop = 1.5
        abot = -0.2
        atop = 0.2
        units = ''
        
   
    
    #BOXPLOTS CREATION with fancy_boxplot
    #fancy_box(mean_metric_ipsi, 'Mean ' + metric + ' values ipsi-lesional side for case and control patients', 'Patient populations', 'Mean ' + metric + ' ipsi-lesional ' + units, bottom, top)
    #fancy_box(mean_metric_contra, 'Mean ' + metric + ' values contra-lesional side for case and control patients', 'Patient populations', 'Mean ' + metric + ' contra-lesional ' + units, bottom, top)
    #fancy_box(rmetric, metric + ' ratio values for case and control patients', 'Patient populations', 'Ratio ' + metric, bottom, rtop)
    #fancy_box(ametric, metric + ' asymmetry values for case and control patients', 'Patient populations', metric + ' asymmetry', abot, atop)
    
    #BOXPLOTS CREATION with ttest_bp
    
    if ROI == '_xtract_prob_Superior_Longitudinal_Fasciculus_1/':
        ROI_title = 'SLF I'
    elif ROI == '_xtract_prob_Superior_Longitudinal_Fasciculus_2/':
        ROI_title = 'SLF II'
    elif ROI == '_xtract_prob_Superior_Longitudinal_Fasciculus_3/':
        ROI_title = 'SLF III'
    elif ROI == '':
        ROI_title = 'CST'
    elif ROI == '_Cortico_Ponto_Cerebellum/':
        ROI_title = 'CPC'
    elif ROI == '_Inferior_Cerebellar_Pedunculus/':
        ROI_title = 'iCP'
    elif ROI == '_Superior_Cerebelar_Pedunculus/':
        ROI_title = 'sCP'
        
    elif ROI == '_xtract_prob_Middle_Cerebellar_Peduncle/':
        ROI_title = 'mCP'
        
    
    
    ttest_bp(mean_metric_ipsi, 'Mean ' + metric + ' values ipsilesional side for case and control patients in the ' + ROI_title, 'Patient populations', 'Mean ' + metric + ' ipsilesional ' + units)
    ttest_bp(mean_metric_contra, 'Mean ' + metric + ' values contralesional side for case and control patients in the ' + ROI_title, 'Patient populations', 'Mean ' + metric + ' contralesional ' + units)
    ttest_bp(rmetric, metric + ' ratio values for case and control patients', 'Patient population in the ' + ROI_title, 'Ratio ' + metric)
    ttest_bp(ametric, metric + ' asymmetry values for case and control patients in the ' + ROI_title, 'Patient populations', metric + ' asymmetry')


#Loop on all the data
#metric_list = ['FA', 'AD', 'MD', 'RD',
#               'noddi_odi', 'noddi_fextra', 'noddi_fintra', 'noddi_fiso',
#               'mf_fvf_tot', 'mf_fvf_f0', 'mf_fvf_f1', 'mf_frac_f0', 'mf_frac_f1', 'mf_frac_csf', 'mf_wfvf',
#               'wFA', 'wAD', 'wMD', 'wRD']

#metric_list = ['wFA', 'wAD', 'wMD', 'wRD']


#metric_list = ['mf_fvf_tot', 'mf_fvf_f0', 'mf_fvf_f1', 'mf_frac_f0', 'mf_frac_f1', 'mf_frac_csf']
metric_list = ['wRD']

#metric_list = ['FA', 'AD', 'MD', 'RD','noddi_odi']
for met in metric_list:
    
    metric_bp(root_res, met, ROI)




