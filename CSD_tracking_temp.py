# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 16:13:26 2021

@author: DELINTE Nicolas

Combination of CSD_tracking2.py and CSD_trackingCluster2.py
"""


root='/Users/florentraskin/Desktop/test2'

import os
import json
import numpy as np
import nibabel as nib
from dipy.io import read_bvals_bvecs
from dipy.core.gradients import gradient_table
from dipy.io.image import load_nifti, load_nifti_data
from dipy.reconst.csdeconv import (ConstrainedSphericalDeconvModel,auto_response_ssst)
from dipy.tracking import utils
from dipy.tracking.local_tracking import LocalTracking
from dipy.tracking.utils import target
from dipy.tracking.streamline import Streamlines
from dipy.tracking.stopping_criterion import ThresholdStoppingCriterion
from dipy.segment.mask import median_otsu
from dipy.io.streamline import save_trk

PatientList=['p532']

params={'fa_thr':.3,'gfa_thresh':.3,'max_angle':15,'step_size':1, 'density':1}
#params={'fa_thr':.6,'gfa_thresh':.35,'max_angle':15,'step_size':1,'density':2}
#angle a impact direct sur le pas de temps et inversement

def brainTracking(Patient_files, params, seed_files=None, target_files=None,
                  all_seed=False):
    '''
    

    Parameters
    ----------
    Patient_files : path to diffusion files + filename (without extension)
    params : parameters dictionary (ex: {'fa_thr':.6,'gfa_thresh':.35,
                                         'max_angle':15,'step_size':1,'density':2})
    seed_files : list of paths to seed masks
    target_files : list of paths to target (logical AND) ROIs
    all_seed: bool
        forces all pixels to be seed candidates

    Returns
    -------
    tract : whole brain tractogram

    '''
    
    data, affine, img = load_nifti(Patient_files+'.nii.gz', return_img=True)
    bvals, bvecs = read_bvals_bvecs(Patient_files+'.bval', Patient_files+'.bvec')
    gtab = gradient_table(bvals, bvecs,atol=1)
    
    if all_seed:
        seed_mask=np.ones(data.shape[:-1])
        white_matter=seed_mask.copy()
        
    else:
    
        mask_data, white_matter = median_otsu(data, vol_idx=[0, 1], median_radius=4, numpass=2,
                                      autocrop=False, dilate=1)
        # white_matter=load_nifti_data(root+Patient+mas_dir+Patient+'_wm_mask'+'.nii.gz')
        
        seed_mask=white_matter
        
    if seed_files!=None:
        seed_mask=load_nifti_data(seed_files[0]+'.nii.gz')
        for i in range(1,len(seed_files)):
            seed_mask+=load_nifti_data(seed_files[i]+'.nii.gz')
            seed_mask[seed_mask>1]=1
        
    seeds = utils.seeds_from_mask(seed_mask, affine, density=params['density'])
    
    response, ratio = auto_response_ssst(gtab, data, roi_radii=10, fa_thr=params['fa_thr'])
    csd_model = ConstrainedSphericalDeconvModel(gtab, response, sh_order=6)
    csd_fit = csd_model.fit(data, mask=white_matter)
    
    from dipy.reconst.shm import CsaOdfModel
    
    csa_model = CsaOdfModel(gtab, sh_order=6)
    gfa = csa_model.fit(data, mask=white_matter).gfa
    stopping_criterion = ThresholdStoppingCriterion(gfa, params['gfa_thresh'])
    
    from dipy.direction import ProbabilisticDirectionGetter
    from dipy.io.stateful_tractogram import Space, StatefulTractogram
    
    
    # SH
    from dipy.data import default_sphere
    
    prob_dg = ProbabilisticDirectionGetter.from_shcoeff(csd_fit.shm_coeff,
                                                        max_angle=params['max_angle'],
                                                        sphere=default_sphere)
    
    streamline_generator = LocalTracking(prob_dg, stopping_criterion, seeds,
                                         affine, step_size=params['step_size'])
    streamlines = Streamlines(streamline_generator)
    
    if target_files!=None:
        for target_file in target_files:
            target_roi=load_nifti_data(target_file+'.nii.gz')
            streamlines = target(streamlines, affine, target_roi, include=True)
    
    tract = StatefulTractogram(streamlines, img, Space.RASMM)
    
    return tract

if __name__=='__main__':

    for Patient in PatientList:
        
        #Patient_files=root+Patient
        Patient_files='/Users/florentraskin/Desktop/test2/p532'
        
        # seed_files=[root+'Folder_containing_ROI/'+Patient+'_seed_name']
        # target_files=[root+'Folder_containing_ROI/'+Patient+'_target_name']
        
        # tract=brainTracking(Patient_files,params,seed_files=seed_files,
        #                    target_files=target_files)
        
        tract=brainTracking(Patient_files,params)
        
        output_dir=root+'Tracking/'
        
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        
        filename=Patient+'_track_name'
        
        save_trk(tract, output_dir+filename+'.trk')
        
        with open(output_dir+filename+'.txt', 'w') as outfile:
            json.dump(params, outfile)