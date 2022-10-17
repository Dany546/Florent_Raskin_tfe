
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

# Functions

def getTransform(static_volume_file,moving_volume_file,onlyAffine=False,
                 diffeomorph=True):
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
    
atlas_list= ['Harvard','XTRACT','Cerebellar','Harvard_cortex','Lobes']

#for atlas in atlas_list:
 #   atlas_files_path = "/Users/florentraskin/Desktop/Registration/"+atlas
 #   directory = os.fsencode(atlas_files_path)
 #   
  #  for file in os.listdir(directory):
  #   filename = os.fsdecode(file)
  #   region = load_nifti(filename)
  #   applyTransform(region ,dmap, static_volume_file, output_path)
  #   output_path = "/Users/florentraskin/Desktop/"+atlas+"ToMNI/"+filename+"ToMNI.nii.gz"
    
