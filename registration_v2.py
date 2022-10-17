
import numpy as np
import nibabel as nib
import os
from dipy.io.image import load_nifti, load_nifti_data
from dipy.align.imaffine import (transform_centers_of_mass,
                                 AffineMap,
                                 MutualInformationMetric,
                                 AffineRegistration)
from dipy.align.transforms import (TranslationTransform3D,
                                   RigidTransform3D,
                                   AffineTransform3D)
from dipy.align.imwarp import SymmetricDiffeomorphicRegistration
from dipy.align.metrics import CCMetric
#from nilearn.input_data import NiftiMasker
# Functions

def getTransform(static_volume_file,moving_volume_file,onlyAffine=False,
                 diffeomorph=False):
    '''

    Parameters
    ----------
    static_volume : 3D array of static volume
    moving_volume : 3D array of moving volume
    diffeomorph : if False then registration is only affine, mettre TRUE par après

    Returns
    -------
    mapping : transform operation to send moving_volume to static_volume space

    '''    
    
    static, static_affine = load_nifti(static_volume_file)
    static_grid2world = static_affine
    
    moving, moving_affine = load_nifti(moving_volume_file)
    moving_grid2world = moving_affine
    
    # Affine registration -----------------------------------------------------
    
    if onlyAffine:
        
        identity = np.eye(4)
        affine_map = AffineMap(identity,
                               static.shape, static_grid2world,
                               moving.shape, moving_grid2world)
        
        return affine_map
    
    c_of_mass = transform_centers_of_mass(static, static_grid2world,
                                          moving, moving_grid2world)
    
    nbins = 32
    sampling_prop = None
    metric = MutualInformationMetric(nbins, sampling_prop)
    
    level_iters = [10000, 1000, 100]
    sigmas = [3.0, 1.0, 0.0]
    factors = [4, 2, 1]
    affreg = AffineRegistration(metric=metric,
                                level_iters=level_iters,
                                sigmas=sigmas,
                                factors=factors)
    
    transform = TranslationTransform3D()
    params0 = None
    translation = affreg.optimize(static, moving, transform, params0,
                                  static_grid2world, moving_grid2world,
                                  starting_affine=c_of_mass.affine)
    
    transform = RigidTransform3D()
    rigid = affreg.optimize(static, moving, transform, params0,
                            static_grid2world, moving_grid2world,
                            starting_affine=translation.affine)
    
    transform = AffineTransform3D()
    affine = affreg.optimize(static, moving, transform, params0,
                             static_grid2world, moving_grid2world,
                             starting_affine=rigid.affine)
    
    # Diffeomorphic registration --------------------------
    
    if diffeomorph:
    
        metric = CCMetric(3)
        
        level_iters = [10000, 1000, 100]
        sdr = SymmetricDiffeomorphicRegistration(metric, level_iters)
        
        mapping = sdr.optimize(static, moving, static_affine, moving_affine,
                               affine.affine)
        
    else:
        
        mapping = affine
    
    return mapping

def applyTransform(file_path,mapping,static_file,output_path,binary=False):
    
    moving=nib.load(file_path)
    moving_data=moving.get_fdata()
            
    transformed=mapping.transform(moving_data)
    
    if binary:
        transformed[transformed>.5]=1
        transformed[transformed<=.5]=0
    
    static=nib.load(static_file)
    
    return transformed
            
    #out=nib.Nifti1Image(transformed,static.affine,header=static.header)
    #out.to_filename(output_path)
    

    
if __name__=='__main__':

    # static_volume_file="C:/Users/nicol/Desktop/PAT1_FA.nii.gz"
    # moving_volume_file= "C:/Users/nicol/Desktop/PAT2_FA.nii.gz"
    # dmap=getTransform(static_volume_file, moving_volume_file)
    
    # output_path = "C:/Users/nicol/Desktop/PAT2toPAT1.nii.gz"
    # applyTransform(moving_volume_file,dmap, static_volume_file, output_path)
    
    #-------------------------------------------
    
    #static_volume_file="/Users/florentraskin/Desktop/Registration/FSL_HCP1065_FA_1mm.nii.gz"
    #moving_volume_file= "/Users/florentraskin/Desktop/test2/20_03_01_E1_FA.nii.gz"
    #dmap=getTransform(static_volume_file, moving_volume_file, onlyAffine=False)
    
    #output_path = "/Users/florentraskin/Desktop/test2/20_03_01_E1_FA_ToMNI.nii.gz"
    #applyTransform(moving_volume_file,dmap, static_volume_file, output_path)

    #moving_volume_file="/Users/florentraskin/Desktop/Registration/FSL_HCP1065_FA_1mm.nii.gz"
    #static_volume_file= "/Users/florentraskin/Desktop/test2/20_03_01_E1_FA.nii.gz"
    #dmap=getTransform(static_volume_file, moving_volume_file, onlyAffine=False)
    
    #output_path = "/Users/florentraskin/Desktop/test2/20_03_01_E1_FA_REG.nii.gz"
    #applyTransform(moving_volume_file,dmap, static_volume_file, output_path)
    '''
    moving_volume_file="/Users/florentraskin/Desktop/Registration/XTRACT/xtract_prob_Forceps_Major.nii.gz"
    static_volume_file= "/Users/florentraskin/Desktop/test2/20_03_01_E1_FA.nii.gz"
    #dmap=getTransform(static_volume_file, moving_volume_file, onlyAffine=False)
    
    output_path = "/Users/florentraskin/Desktop/test2/20_03_01_E1_Forceps_Major.nii.gz"
    ROI_reg = applyTransform(moving_volume_file,dmap, static_volume_file, output_path)
    ROI_reg[ROI_reg<30]=0
    ROI_reg[ROI_reg>=30]=1
    #np.where(ROI_reg=>30,1,0)
    static=nib.load(static_volume_file)
    out=nib.Nifti1Image(ROI_reg,static.affine,header=static.header)
    out.to_filename(output_path)
    
    image = nib.load(static_volume_file)
    FA = image.get_fdata()
    maskedFA = FA*ROI_reg
    mean=np.mean(maskedFA[ROI_reg==1])
    print(mean)
    '''
    
#root_out = "/Users/florentraskin/Documents/Documents personnels/Thesis/Registration/" 
root_out = "/Users/florentraskin/Desktop/non_diff_registration/"
root_FA = "/Users/florentraskin/Documents/Documents personnels/Thesis/Data/FA_maps/"
#root_FA = "/Users/florentraskin/Documents/Documents personnels/Thesis/Data/T1_maps/"
root_atlas = "/Users/florentraskin/Desktop/Registration/XTRACT/CST/"
#root_atlas = "/Users/florentraskin/Desktop/Registration/"
root_masks = "/Users/florentraskin/Documents/Documents personnels/Thesis/study/subjects/"

#atlas_list= ['Harvard','XTRACT','Cerebellar','Harvard_cortex','Lobes']
#prob_tresh_list=[30, 30, 0.2, 30, 30] #[0:100]
moving_standard_brain ="/Users/florentraskin/Desktop/Registration/FSL_HCP1065_FA_1mm.nii.gz"
#patient_list=["20_02_02_E0", "20_11_02_E0", "20_08_02_E0", "20_05_01_E0", "20_06_02_E0", "20_10_02_E0", "20_07_01_E2", "20_01_01_E2", "20_05_02_E2", "20_03_01_E2", "20_08_01_E2", "20_02_01_E2", "20_10_01_E2", "20_02_01_E0", "20_08_01_E0", "20_05_02_E0", "20_03_01_E0", "20_06_01_E0", "20_01_01_E0", "20_08_02_E3", "20_11_02_E3", "20_10_02_E3", "20_05_01_E3", "20_02_02_E3", "20_03_01_E1", "20_06_01_E1", "20_10_01_E1", "20_01_01_E1", "20_08_01_E1", "20_02_01_E1", "20_02_02_E2", "20_11_02_E2", "20_08_02_E2", "20_10_02_E2", "20_05_01_E2", "20_06_02_E2", "20_06_02_E1", "20_08_02_E1", "20_05_01_E1", "20_10_02_E1", "20_02_02_E1", "20_06_01_E2", "20_06_02_E3", "20_07_01_E0", "20_07_01_E1", "20_11_02_E1"]
#patient_list=["20_05_02_E0", "20_03_01_E0", "20_06_01_E0", "20_01_01_E0", "20_08_02_E3", "20_11_02_E3", "20_10_02_E3", "20_05_01_E3", "20_02_02_E3", "20_06_01_E1", "20_10_01_E1", "20_01_01_E1", "20_08_01_E1", "20_02_01_E1", "20_02_02_E2", "20_11_02_E2", "20_08_02_E2", "20_10_02_E2", "20_05_01_E2", "20_06_02_E2", "20_06_02_E1", "20_08_02_E1", "20_05_01_E1", "20_10_02_E1", "20_02_02_E1", "20_06_01_E2", "20_06_02_E3", "20_07_01_E0", "20_07_01_E1", "20_11_02_E1"]
#patient_list = ["20_03_01_E1"]
#patient_list = ["20_01_01_E0"]
atlas_list= ['XTRACT']
prob_tresh_list=[30] #[0:100]

patient_list = ["20_02_02_E0"]
#atlas_list= ['Corpus_Callosum']
#prob_tresh_list=[0.3] #[0:100]
#moving_standard_brain ="/Users/florentraskin/Desktop/Registration/00Average_Brain.nii"


for patient in patient_list:
    patient_files = root_FA + patient
    static_volume_file = patient_files + "_FA.nii.gz"
    #static_volume_file = patient_files + '.nii.gz'
    static=nib.load(static_volume_file)
    dmap=getTransform(static_volume_file, moving_standard_brain, onlyAffine=False)
    
    brain_mask_file = root_masks + patient + '/masks/' + patient + '_brain_mask.nii.gz'
    brain_mask = nib.load(brain_mask_file)
    brain_masker = brain_mask.get_data()
    
    for i in range(len(atlas_list)):
        atlas_name = atlas_list[i]
        atlas_files = root_atlas + atlas_list[i]
        #print(atlas_files)
        
        atlas_directory = os.fsencode(root_atlas)
        
        #print(atlas_directory)
        
        atlas_threshold = prob_tresh_list[i]
        
        for file in os.listdir(atlas_directory):
            
            #moving_volume_path = os.fsdecode(file)
            #print(moving_volume_path)
            
            #moving_volume_file = atlas_files + '/' + str(moving_volume_path)
            #print(moving_volume_file)
            
           # output_dir = root_out + patient + '_' + atlas_name
           # print(output_dir)
            
            #output_dir_final = root_out + patient + '/' + atlas_name + '/'
            
            #output_filename = moving_volume_file.replace((atlas_files+'/'),"")
            #print(output_filename)
            
           # output_path = output_dir_final + patient + '_' + output_filename
           
            moving_volume_file_L = "/Users/florentraskin/Desktop/Registration/XTRACT/CST/xtract_prob_Corticospinal_Tract_L.nii.gz"
            moving_volume_file_R = "/Users/florentraskin/Desktop/Registration/XTRACT/CST/xtract_prob_Corticospinal_Tract_R.nii.gz"

            
            output_path_L = root_out + patient + '_CST_L.nii.gz'
            output_path_R = root_out + patient + '_CST_R.nii.gz'
            #print(output_path)
            
            atlas_reg_L = applyTransform(moving_volume_file_L ,dmap, static_volume_file, output_path_L)
            atlas_reg_L = np.where(atlas_reg_L >= atlas_threshold, 1, 0)
            
            atlas_reg_L_final = atlas_reg_L * brain_masker
            
            
            #out=nib.Nifti1Image(atlas_reg,static.affine,header=static.header)
            out_L = nib.Nifti1Image(atlas_reg_L_final,static.affine,header=None)
            out_L.to_filename(output_path_L)
            
            atlas_reg_R = applyTransform(moving_volume_file_R ,dmap, static_volume_file, output_path_R)
            atlas_reg_R = np.where(atlas_reg_R >= atlas_threshold, 1, 0)
            
            atlas_reg_R_final = atlas_reg_R * brain_masker
            
            
            #out=nib.Nifti1Image(atlas_reg,static.affine,header=static.header)
            out_R = nib.Nifti1Image(atlas_reg_R_final,static.affine,header=None)
            out_R.to_filename(output_path_R)
             
             
  #   output_path = "/Users/florentraskin/Desktop/"+atlas+"ToMNI/"+filename+"ToMNI.nii.gz"
        
    

#for atlas in atlas_list:
 #   atlas_files_path = "/Users/florentraskin/Desktop/Registration/"+atlas
 #   directory = os.fsencode(atlas_files_path)
 #   
  #  for file in os.listdir(directory):
  #   filename = os.fsdecode(file)
  #   region = load_nifti(filename)
  #   applyTransform(region ,dmap, static_volume_file, output_path)
  #   output_path = "/Users/florentraskin/Desktop/"+atlas+"ToMNI/"+filename+"ToMNI.nii.gz"
    
