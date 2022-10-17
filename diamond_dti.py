#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 21:26:49 2022

@author: florentraskin
"""
import numpy as np
import nibabel as nib
from dipy.io.image import load_nifti, save_nifti
from dipy.io.gradients import read_bvals_bvecs
from dipy.core.gradients import gradient_table
import dipy.reconst.dti as dti
from TIME.utils import tensor_to_DTI

#d_dti = load_nifti("/Users/florentraskin/Desktop/20_03_01_E1_diamond_dti.nii.gz")
#d_frac = load_nifti("/Users/florentraskin/Desktop/20_03_01_E1_diamond_fractions.nii.gz")

#d0 = d_dti[0][0]

#print(d0[0])
#tenmodel = dti.TensorModel(d_dti[0])

root = "/CECI/proj/pilab/PermeableAccess/stroke_UHlk48tPt545/study/subjects/"
root_out = "/CECI/proj/pilab/PermeableAccess/stroke_UHlk48tPt545/study/Analysis/diamond_maps/"

patient_list = ["20_03_01_E1"]

for patient in patient_list:
    print(patient)
    t0_filename = root + patient + "/dMRI/microstructure/diamond/" + patient + "_diamond_t0.nii.gz"
    im_t0 = nib.load(t0_filename)
    data_t0 = im_t0.get_fdata()
    
    t1_filename = root + patient + "/dMRI/microstructure/diamond/" + patient + "_diamond_t1.nii.gz"
    im_t1 = nib.load(t1_filename)
    data_t1 = im_t1.get_fdata()
    
    frac_filename = root + patient + "/dMRI/microstructure/diamond/" + patient + "_diamond_fractions.nii.gz"
    frac = nib.load(frac_filename).get_fdata()
    frac_t0 = frac[:,:,:,0,0]
    frac_t1 = frac[:,:,:,0,1]
    
    fa = nib.load(root + patient + "/dMRI/microstructure/dti/" + patient + "_FA.nii.gz")
    ad = nib.load(root + patient + "/dMRI/microstructure/dti/" + patient + "_AD.nii.gz")
    md = nib.load(root + patient + "/dMRI/microstructure/dti/" + patient + "_MD.nii.gz")
    rd = nib.load(root + patient + "/dMRI/microstructure/dti/" + patient + "_RD.nii.gz")
    
    FA_t0, AD_t0, RD_t0, MD_t0 = tensor_to_DTI(data_t0)
    FA_t1, AD_t1, RD_t1, MD_t1 = tensor_to_DTI(data_t1)
    
    wFA = (frac_t0*FA_t0 + frac_t1*FA_t1) / (frac_t0+frac_t1)
    wAD = (frac_t0*AD_t0 + frac_t1*AD_t1) / (frac_t0+frac_t1)
    wMD = (frac_t0*MD_t0 + frac_t1*MD_t1) / (frac_t0+frac_t1)
    wRD = (frac_t0*RD_t0 + frac_t1*RD_t1) / (frac_t0+frac_t1)
    
    outwFA = nib.Nifti1Image(wFA, fa.affine, fa.header)
    outwFA.to_filename(root_out + patient + "_wFA.nii.gz")
    
    outwAD = nib.Nifti1Image(wAD, ad.affine, ad.header) 
    outwAD.to_filename(root_out + patient + "_wAD.nii.gz")

    outwMD = nib.Nifti1Image(wMD, md.affine, md.header)
    outwMD.to_filename(root_out + patient + "_wMD.nii.gz")

    outwRD = nib.Nifti1Image(wRD, rd.affine, rd.header)
    outwRD.to_filename(root_out + patient + "_wRD.nii.gz")


"""
image_t0 = nib.load('/Users/florentraskin/Desktop/20_03_01_E1_diamond_t0.nii.gz')
image_t1= nib.load('/Users/florentraskin/Desktop/20_03_01_E1_diamond_t1.nii.gz')

data_t0 = image_t0.get_fdata()
data_t1 = image_t1.get_fdata()




FA_t0, AD_t0, RD_t0, MD_t0 = tensor_to_DTI(data_t0)
FA_t1, AD_t1, RD_t1, MD_t1 = tensor_to_DTI(data_t1)

fa = nib.load("/Users/florentraskin/Documents/Documents personnels/Thesis/study/subjects/20_03_01_E1/dMRI/microstructure/dti/20_03_01_E1_fargb.nii.gz")


#out=nib.Nifti1Image(FA, fa.affine, fa.header)
#out.to_filename("/Users/florentraskin/Desktop/fa_t0.nii.gz")

frac = nib.load('/Users/florentraskin/Desktop/20_03_01_E1_diamond_fractions.nii.gz').get_fdata()

frac_t0 = frac[:,:,:,0,0]
frac_t1 = frac[:,:,:,0,1]

wFA = (frac_t0*FA_t0 + frac_t1*FA_t1) / (frac_t0+frac_t1)

mask_L = nib.load("/Users/florentraskin/Documents/Documents personnels/Thesis/Registration/20_03_01_E1/XTRACT/20_03_01_E1_xtract_prob_Corticospinal_Tract_L.nii.gz").get_fdata()

masked_L_wFA = wFA * mask_L

out=nib.Nifti1Image(masked_L_wFA, fa.affine, fa.header)
out.to_filename("/Users/florentraskin/Desktop/masked_L_wFA_test.nii.gz")
"""