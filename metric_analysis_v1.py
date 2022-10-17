#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 16 14:41:50 2022

@author: florentraskin
"""

import numpy as np
import nibabel as nib 
import json

def metric_analysis(analysis_dico, cluster, root_registration, root_metric_maps, root_output):
    
    ROI = analysis_dico["ROI"]
    
    atlas = analysis_dico["atlas"]
    
    metric = analysis_dico["metric"]
    
    
    
    mean_metric_ipsi_E0 = []
    mean_metric_ipsi_E1 = []
    mean_metric_ipsi_E2 = []
    mean_metric_ipsi_E3 = []
    
    mean_metric_contra_E0 = []
    mean_metric_contra_E1 = []
    mean_metric_contra_E2 = []
    mean_metric_contra_E3 = []
    
    rmetric_E0 = []
    rmetric_E1 = []
    rmetric_E2 = []
    rmetric_E3 = []
    
    ametric_E0 = []
    ametric_E1 = []
    ametric_E2 = []
    ametric_E3 = []
    
    
    
    for patient in analysis_dico["patient_list"]: 
        
        #Load the ROI masks

        #Lesion on the left side of the brain
        if analysis_dico["side"]=='left':
            if analysis_dico["atlas"]=='XTRACT':
                ROI_file_contra = root_registration + patient + '/' + atlas +'/' + patient + ROI + "_R.nii.gz"
                ROI_file_ipsi = root_registration + patient + '/' + atlas +'/' + patient + ROI + "_L.nii.gz"
                
            else:
                ROI_file_contra = root_registration + patient + '/' + atlas +'/' + patient + ROI + "_Right.nii.gz"
                ROI_file_ipsi = root_registration + patient + '/' + atlas +'/' + patient + ROI + "_Left.nii.gz"
                
            ROI_volume_contra = nib.load(ROI_file_contra)
            ROI_volume_ipsi = nib.load(ROI_file_ipsi)
            ROI_mask_contra = ROI_volume_contra.get_fdata()
            ROI_mask_ipsi = ROI_volume_ipsi.get_fdata()
           
            
        #Lesion on the right side of the brain  
        elif analysis_dico["side"]=='right':
            
             if analysis_dico["atlas"]=='XTRACT':
                ROI_file_ipsi = root_registration + patient + '/' + atlas +'/' + patient + ROI + "_R.nii.gz"
                ROI_file_contra = root_registration + patient + '/' + atlas +'/' + patient + ROI + "_L.nii.gz"
                
             else:
                ROI_file_ipsi = root_registration + patient + '/' + atlas +'/' + patient + ROI + "_Right.nii.gz"
                ROI_file_contra = root_registration + patient + '/' + atlas +'/' + patient + ROI + "_Left.nii.gz"
            
           
             ROI_volume_ipsi = nib.load(ROI_file_ipsi)
             ROI_volume_contra = nib.load(ROI_file_contra)
             ROI_mask_ipsi = ROI_volume_ipsi.get_fdata()
             ROI_mask_contra = ROI_volume_contra.get_fdata()
             
             
            
            
        #Load metric map
        #Cluster
        if cluster == True:
            root_cluster_metric_maps = root_metric_maps + patient + '/dMRI/microstructure/'
            
            #DTI metrics
            if (metric == 'FA') or (metric == 'AD') or (metric == 'MD') or (metric == 'RD'):
                
                metric_volume_file = root_cluster_metric_maps + 'dti/' + patient + "_" + metric + ".nii.gz"
            
            
            #NODDI metrics
            if (metric == 'noddi_ODI') or (metric == 'noddi_fextra') or (metric == 'noddi_fintra') or (metric == 'noddi_fiso'):
                
                metric_volume_file = root_cluster_metric_maps + 'noddi/' + patient + "_" + metric + ".nii.gz"
            
            
            #MF metrics
            if (metric == 'mf_fvf_tot') or (metric == 'mf_fvf_f0') or (metric == 'mf_fvf_f1'):
                
                metric_volume_file = root_cluster_metric_maps + 'mf/' + patient + "_" + metric + ".nii.gz"
            
            
            #DIAMOND metrics
            
            if (metric == 'wFA') or (metric == 'wAD') or (metric == 'wMD') or (metric == 'wRD'):
                
                metric_volume_file = root_cluster_metric_maps + 'mf/' + patient + "_" + metric + ".nii.gz"
        #Local
        if cluster ==  False:
            patient_files = root_metric_maps + patient
            metric_volume_file = patient_files + "_" + metric + ".nii.gz"
        
        
        
        metric_map = nib.load(metric_volume_file).get_fdata()
        
        metric_ROI_ipsi = metric_map * ROI_mask_ipsi
        metric_ROI_contra = metric_map * ROI_mask_contra
        
        
        #means
        mean_metric_ipsi = np.mean(metric_ROI_ipsi[metric_ROI_ipsi>0])
        mean_metric_contra = np.mean(metric_ROI_contra[metric_ROI_contra>0])
        
        #print(patient)
        #print("Mean metric ipsi-lesional", mean_metric_ipsi)
        #print("Mean metric contra-lesional", mean_metric_contra)
        
        
        #rmetric
        rmetric = mean_metric_ipsi/mean_metric_contra
        
        #print("Ratio metric", rmetric)
        
        
        #metric_asym
        
        ametric = (mean_metric_contra - mean_metric_ipsi)/(mean_metric_contra + mean_metric_ipsi)
        
        #print("Metric asymmetry", ametric)
            
        
        #Time separation
        
        if 'E0' in patient:
            mean_metric_ipsi_E0.append(mean_metric_ipsi)
            mean_metric_contra_E0.append(mean_metric_contra)
            rmetric_E0.append(rmetric)
            ametric_E0.append(ametric)
            
        elif 'E1' in patient: 
            mean_metric_ipsi_E1.append(mean_metric_ipsi)
            mean_metric_contra_E1.append(mean_metric_contra)
            rmetric_E1.append(rmetric)
            ametric_E1.append(ametric)
            
        elif 'E2' in patient:
            mean_metric_ipsi_E2.append(mean_metric_ipsi)
            mean_metric_contra_E2.append(mean_metric_contra)
            rmetric_E2.append(rmetric)
            ametric_E2.append(ametric)
            
        else:
            mean_metric_ipsi_E3.append(mean_metric_ipsi)
            mean_metric_contra_E3.append(mean_metric_contra)
            rmetric_E3.append(rmetric)
            ametric_E3.append(ametric)
    
        
    #Output
    mean_metric_ipsi_tot = [mean_metric_ipsi_E0, mean_metric_ipsi_E1, mean_metric_ipsi_E2, mean_metric_ipsi_E3]
    mean_metric_contra_tot = [mean_metric_contra_E0, mean_metric_contra_E1, mean_metric_contra_E2, mean_metric_contra_E3]
    rmetric_tot = [rmetric_E0, rmetric_E1, rmetric_E2, rmetric_E3]
    ametric_tot = [ametric_E0, ametric_E1, ametric_E2, ametric_E3]
    
    metric_out = {"patient_list": analysis_dico["patient_list"], "type": analysis_dico["type"] ,"side": analysis_dico["side"], "atlas": atlas, "ROI": ROI, "metric": analysis_dico["metric"],"mean_metric_ipsi": mean_metric_ipsi_tot, "mean_metric_contra": mean_metric_contra_tot, "rmetric": rmetric_tot, "ametric": ametric_tot}
    
    filename_out = analysis_dico["type"] + '_' + analysis_dico["side"] + '_' + analysis_dico["metric"] + analysis_dico["test"] + '_' + analysis_dico["ROI"]
    
    with open(root_output + analysis_dico["metric"] + '_analysis_results/' + filename_out + '.json', 'w') as outfile:
       json.dump(metric_out, outfile)