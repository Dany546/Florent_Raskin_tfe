#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 16 11:20:27 2022

@author: florentraskin
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from ttest_bp import ttest_bp


root_res = '/Users/florentraskin/Documents/Documents personnels/Thesis/Analysis/'
#ROI = ''
#ROI = '_Cortico_Ponto_Cerebellum/'
#ROI = '_Inferior_Cerebellar_Pedunculus/'
#ROI = '_Superior_Cerebelar_Pedunculus/'
#ROI = '_xtract_prob_Superior_Longitudinal_Fasciculus_1/'
#ROI = '_xtract_prob_Superior_Longitudinal_Fasciculus_2/'
#ROI = '_xtract_prob_Superior_Longitudinal_Fasciculus_3/'
ROI = '_xtract_prob_Middle_Cerebellar_Peduncle/'

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
    
    
    case_filepath = results_dir + 'case__' + metric
    
    ctrl_filepath = results_dir + 'ctrl__' + metric
    
    with open(case_filepath + '.json', 'r') as fp:
        case_results = json.load(fp)
    
       
    with open(ctrl_filepath + '.json', 'r') as fp:
       ctrl_results = json.load(fp)
       
       
    #MEAN METRIC
    #Mean metric case
    mean_metric_case = case_results["mCP_metric"]
    
    
    #Mean metric ctrl
    mean_metric_ctrl = ctrl_results["mCP_metric"]
   
    
    
    #Change scale
    if (metric == 'AD') or (metric == 'MD') or (metric =='RD'):
        for i in range(4):
            
            
            mean_metric_case[i] = [elem * 1000 for elem in mean_metric_case[i]]
            
            mean_metric_ctrl[i] = [elem * 1000 for elem in mean_metric_ctrl[i]]
    
    #Mean metric ipsi tot
    mean_metric = [mean_metric_case[0], mean_metric_ctrl[0], 
                    mean_metric_case[1], mean_metric_ctrl[1],
                    mean_metric_case[2], mean_metric_ctrl[2],
                    mean_metric_case[3], mean_metric_ctrl[3]]
    
    print(mean_metric)
    
   
    
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
        
    
    
    ttest_bp(mean_metric, 'Mean ' + metric + ' values ipsilesional side for case and control patients in the ' + ROI_title, 'Patient populations', 'Mean ' + metric + ' ipsilesional ' + units)
    #ttest_bp(mean_metric_contra, 'Mean ' + metric + ' values contralesional side for case and control patients in the ' + ROI_title, 'Patient populations', 'Mean ' + metric + ' contralesional ' + units)
    #ttest_bp(rmetric, metric + ' ratio values for case and control patients', 'Patient population in the ' + ROI_title, 'Ratio ' + metric)
    #ttest_bp(ametric, metric + ' asymmetry values for case and control patients in the ' + ROI_title, 'Patient populations', metric + ' asymmetry')


#Loop on all the data
metric_list = ['FA', 'AD', 'MD', 'RD',
               'noddi_odi', 'noddi_fextra', 'noddi_fintra', 'noddi_fiso',
               'mf_fvf_tot', 'mf_fvf_f0', 'mf_fvf_f1', 'mf_frac_f0', 'mf_frac_f1', 'mf_frac_csf', 'mf_wfvf',
               'wFA', 'wAD', 'wMD', 'wRD']

#metric_list = ['wFA', 'wAD', 'wMD', 'wRD']


#metric_list = ['mf_fvf_tot', 'mf_fvf_f0', 'mf_fvf_f1', 'mf_frac_f0', 'mf_frac_f1', 'mf_frac_csf']
#metric_list = ['wRD']

#metric_list = ['FA', 'AD', 'MD', 'RD','noddi_odi']
for met in metric_list:
    
    metric_bp(root_res, met, ROI)




