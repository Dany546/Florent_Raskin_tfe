#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 15:02:42 2022

@author: florentraskin
"""
#import numpy as np
#import nibabel as nib 
#import json
#from FA_analysis_v1 import FA_analysis
from metric_analysis_v1 import metric_analysis
#from varname import nameof


patient_list_all=["20_02_02_E0", "20_11_02_E0", "20_08_02_E0", "20_05_01_E0", "20_06_02_E0", "20_10_02_E0", "20_07_01_E2", "20_01_01_E2", "20_05_02_E2", "20_03_01_E2", "20_08_01_E2", "20_02_01_E2", "20_10_01_E2", "20_02_01_E0", "20_08_01_E0", "20_05_02_E0", "20_03_01_E0", "20_06_01_E0", "20_01_01_E0", "20_08_02_E3", "20_11_02_E3", "20_10_02_E3", "20_05_01_E3", "20_02_02_E3", "20_03_01_E1", "20_06_01_E1", "20_10_01_E1", "20_01_01_E1", "20_08_01_E1", "20_02_01_E1", "20_02_02_E2", "20_11_02_E2", "20_08_02_E2", "20_10_02_E2", "20_05_01_E2", "20_06_02_E2", "20_06_02_E1", "20_08_02_E1", "20_05_01_E1", "20_10_02_E1", "20_02_02_E1", "20_06_01_E2", "20_06_02_E3", "20_07_01_E0", "20_07_01_E1", "20_11_02_E1"]
patient_list_test=["20_03_01_E0", "20_03_01_E1" , "20_03_01_E2", "20_06_02_E0", "20_06_02_E1", "20_06_02_E2", "20_06_02_E3"]
patient_list_test_case_R = ["20_03_01_E0", "20_03_01_E1" , "20_03_01_E2"]
patient_list_test_ctrl_R = ["20_06_02_E0", "20_06_02_E1", "20_06_02_E2", "20_06_02_E3"]


case_L = ["20_01_01_E0", "20_01_01_E1", "20_01_01_E2", "20_02_01_E0", "20_02_01_E1", "20_02_01_E2"]
case_R = ["20_03_01_E0", "20_03_01_E1", "20_03_01_E2", "20_05_02_E0", "20_05_02_E2", "20_06_01_E0", "20_06_01_E1", "20_06_01_E2", "20_07_01_E0", "20_07_01_E1", "20_07_01_E2", "20_08_01_E0", "20_08_01_E1", "20_08_01_E2", "20_10_01_E1", "20_10_01_E2"]
ctrl_L = ["20_02_02_E0", "20_02_02_E1", "20_02_02_E2", "20_02_02_E3", "20_05_01_E0", "20_05_01_E1", "20_05_01_E2", "20_05_01_E3", "20_11_02_E0", "20_11_02_E1", "20_11_02_E2", "20_11_02_E3"]
ctrl_R = ["20_06_02_E0", "20_06_02_E1", "20_06_02_E2", "20_06_02_E3", "20_08_02_E0", "20_08_02_E1", "20_08_02_E2", "20_08_02_E3", "20_10_02_E0", "20_10_02_E1", "20_10_02_E2", "20_10_02_E3"]



#dico in avec list de patients et metric qu'on veut 
#dico out avec list, resultats , nom de la métriuque
#autre code pour faire les boxplots 

#dico metric can be: 'FA', 'MD', 'AD', 'MD', 'noddi_odi' ,'noddi_fextra', 'noddi_fintra', 'noddi_fiso', 'mf_fvf_f0', 'mf_fvf_f1', mf_fvf_ftot'

cluster = False

#LOCAL ROOTS
if cluster == False:
    
    root_reg = "/Users/florentraskin/Documents/Documents personnels/Thesis/Registration/"
    
    root_FA = "/Users/florentraskin/Documents/Documents personnels/Thesis/Data/FA_maps/"
    root_AD = "/Users/florentraskin/Documents/Documents personnels/Thesis/Data/AD_maps/"
    root_MD = "/Users/florentraskin/Documents/Documents personnels/Thesis/Data/MD_maps/"
    root_RD = "/Users/florentraskin/Documents/Documents personnels/Thesis/Data/RD_maps/"
    root_noddi_odi = "/Users/florentraskin/Documents/Documents personnels/Thesis/Data/odi_maps/"
    root_noddi_fextra = "/Users/florentraskin/Documents/Documents personnels/Thesis/Data/fextra_maps/"
    root_noddi_fintra = "/Users/florentraskin/Documents/Documents personnels/Thesis/Data/fintra_maps/"
    root_noddi_fiso = "/Users/florentraskin/Documents/Documents personnels/Thesis/Data/fiso_maps/"
    root_mf_fvf_f0 = "/Users/florentraskin/Documents/Documents personnels/Thesis/Data/fvf_f0_maps/"
    root_mf_fvf_f1 = "/Users/florentraskin/Documents/Documents personnels/Thesis/Data/fvf_f1_maps/"
    root_mf_fvf_tot = "/Users/florentraskin/Documents/Documents personnels/Thesis/Data/fvf_tot_maps/"



    root_out = "/Users/florentraskin/Documents/Documents personnels/Thesis/Analysis/"


#CLUSTER ROOTS
if cluster == True:
    
    root_reg = '/home/ucl/ingi/raskinf/stroke/study/Registration/'
    
    root_subj = '/home/ucl/ingi/raskinf/stroke/study/subjects/'

    root_out = '/home/ucl/ingi/raskinf/stroke/study/Analysis/'

#analysis_dico = {"patient_list": patient_list, "type": ctrl or case ,"side": "right", "ROI": ROI_list, "metric_list": metric_list, "input_path": root, "output_path": root}

def analysis(analysis_dico):
              
    
    #DTI metrics analysis
    
    #FA
    if analysis_dico["metric"] == 'FA':
        
        #metric_analysis(analysis_dico, cluster, root_reg, root_FA, root_out)
        metric_analysis(analysis_dico, cluster, root_reg, root_subj, root_out)
  
    #MD
    if analysis_dico["metric"] == 'MD':
        
        #metric_analysis(analysis_dico, cluster, root_reg, root_MD, root_out)
        metric_analysis(analysis_dico, cluster, root_reg, root_subj, root_out)
        
    #AD
    if analysis_dico["metric"] == 'AD':
        
        #metric_analysis(analysis_dico, cluster, root_reg, root_AD, root_out)
        metric_analysis(analysis_dico, cluster, root_reg, root_subj, root_out)
        
    #RD
    if analysis_dico["metric"] == 'RD':
        
         #metric_analysis(analysis_dico, cluster, root_reg, root_RD, root_out)
         metric_analysis(analysis_dico, cluster, root_reg, root_subj, root_out)
        
        
        
        
    #NODDI metrics analysis
    
    #ODI
    if analysis_dico["metric"] == 'noddi_odi':
        
         #metric_analysis(analysis_dico, cluster, root_reg, root_noddi_odi, root_out)
         metric_analysis(analysis_dico, cluster, root_reg, root_subj, root_out)
        
    #fintra
    if analysis_dico["metric"] == 'noddi_fintra':
        
         #metric_analysis(analysis_dico, cluster, root_reg, root_noddi_fintra, root_out)
         metric_analysis(analysis_dico, cluster, root_reg, root_subj, root_out)
        
        
    #fiso
    if analysis_dico["metric"] == 'noddi_fiso':
        
         #metric_analysis(analysis_dico, cluster,root_reg, root_noddi_fiso, root_out)
         metric_analysis(analysis_dico, cluster, root_reg, root_subj, root_out)
        
    
    #fextra
    if analysis_dico["metric"] == 'noddi_fextra':
    
        #metric_analysis(analysis_dico, cluster, root_reg, root_noddi_fextra, root_out)
        metric_analysis(analysis_dico, cluster, root_reg, root_subj, root_out)
    
    
    
    #MF metrics analysis

    #fvf_ftot
    if analysis_dico["metric"] == 'mf_fvf_tot':
    
         #metric_analysis(analysis_dico, cluster, root_reg, root_mf_fvf_tot, root_out)
         metric_analysis(analysis_dico, cluster, root_reg, root_subj, root_out)

    
    #fvf_f0
    if analysis_dico["metric"] == 'mf_fvf_f0':
        
         #metric_analysis(analysis_dico, cluster,root_reg, root_mf_fvf_f0, root_out)
         metric_analysis(analysis_dico, cluster, root_reg, root_subj, root_out)

         
    #fvf_f1
    if analysis_dico["metric"] == 'mf_fvf_f1':
        
         #metric_analysis(analysis_dico, cluster, root_reg, root_mf_fvf_f1, root_out)
         metric_analysis(analysis_dico, cluster, root_reg, root_subj, root_out)

    
    
    
    #DIAMOND metrics analysis



#analysis(analysis_dico = {"patient_list": case_R, "type":'case' ,"side": "right", 'atlas':'XTRACT', "ROI": "_xtract_prob_Corticospinal_Tract", "metric": 'FA', "input_path": root_noddi_odi, "output_path": root_out})

testing = True

#Loop on all the data
#metric_list = ['FA', 'AD', 'MD', 'RD', 'noddi_odi', 'noddi_fextra', 'noddi_fintra', 'noddi_fiso',
#              'mf_fvf_tot', 'mf_fvf_f0', 'mf_fvf_f1']
metric_list = ['FA']

#patient_lists = [case_L, case_R, ctrl_L, ctrl_R]
patient_lists = [patient_list_test_case_R, patient_list_test_ctrl_R]


#Loop on all metrics
for met in metric_list:
    
    #Loop on all partient lists
    for p_list in patient_lists:
        
        
        check_case_L = all(item in case_L for item in p_list)

        if check_case_L == True:
            #print('1')
            p_type = 'case'
            p_side = 'left'
        
        check_case_R = all(item in case_R for item in p_list)

        if check_case_R == True:
            #print('2')
            p_type = 'case'
            p_side = 'right'
            
        check_ctrl_L = all(item in ctrl_L for item in p_list)

        if check_ctrl_L == True:
            #print('3')
            p_type = 'ctrl'
            p_side = 'left'
            
        check_ctrl_R = all(item in ctrl_R for item in p_list)

        if check_ctrl_R == True:
            #print('4')
            p_type = 'ctrl'
            p_side = 'right'
            
        #Testing
        if testing ==  True:
            p_test = 'test'
        else:
            p_test = ''
            
        #analysis_diction_CST = {"patient_list": p_list, "test": p_test ,"type": p_type, "side": p_side,'atlas':'XTRACT', "ROI": "_xtract_prob_Corticospinal_Tract", "metric": met} 
        #analysis(analysis_diction_CST)
        
        
        analysis_diction_CPCP = {"patient_list": p_list, "test": p_test ,"type": p_type, "side": p_side,'atlas':'Cerebellar', "ROI": "_Cortico_Ponto_Cerebellum", "metric": met} 
        analysis_diction_CPInf = {"patient_list": p_list, "test": p_test ,"type": p_type, "side": p_side,'atlas':'Cerebellar', "ROI": "_Inferior_Cerebellar_Pedunculus", "metric": met} 
        analysis_diction_CPSup = {"patient_list": p_list, "test": p_test ,"type": p_type, "side": p_side,'atlas':'Cerebellar', "ROI": "_Superior_Cerebelar_Pedunculus", "metric": met} 
        
        analysis(analysis_diction_CPCP)
        
        
        analysis_diction_SLF1 = {"patient_list": p_list, "test": p_test ,"type": p_type, "side": p_side,'atlas':'XTRACT', "ROI": "_xtract_prob_Superior_Longitudinal_Fasciculus_1", "metric":met}
        analysis_diction_SLF2 = {"patient_list": p_list, "test": p_test ,"type": p_type, "side": p_side,'atlas':'XTRACT', "ROI": "_xtract_prob_Superior_Longitudinal_Fasciculus_2", "metric":met}
        analysis_diction_SLF3 = {"patient_list": p_list, "test": p_test ,"type": p_type, "side": p_side,'atlas':'XTRACT', "ROI": "_xtract_prob_Superior_Longitudinal_Fasciculus_3", "metric":met}


        
#Upload registration sur clusters
#Modifier les root pour clusters 
#Tester pour les autres metrics? 
#Tout lancer 
#Faire tous les bp facilement 














