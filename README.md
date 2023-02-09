# User interface for CNN result visualisation for a microimaing vs histology study in meningiomas.
* Contact: *jbrabec2 [at] jh [dot] edu*

## Objective

To visualise 

## How to obtain data
1. Clone this repository to Your machine.
2. Download the data from [AIDA repository](https://aida-doi-repository.github.io) and paste them into folder **data** one level above this directory (**microimaging_histology_DIB**). The [AIDA repository](https://aida-doi-repository.github.io) contains both raw and processed data as well as data related to our [example analysis from our other manuscript](https://github.com/jan-brabec/microimaging_vs_histology_in_meningeomas).
3. You may also clone our [example analysis](https://github.com/jan-brabec/microimaging_vs_histology_in_meningeomas) of this data to the same folder (**microimaging_histology_DIB**).


## Data formats and how to read them
* Raw histological slides are stored as multi-image *.tif* files with separated RGB channels. We recommend viewing them using MATLAB:

```
H(:,:,1) = imread('filename.tif'),'Index',1);
H(:,:,2) = imread('filename.tif'),'Index',2);
H(:,:,3) = imread('filename.tif'),'Index',3);

imagesc(H);
axis image off;
```

* We have prepared a function that allows to view H&E, VEGF as well as Mean diffusivity and in-plane fractional anisotropy (FAIP). It allows also to zoom-in also on particular regions of the histology of DTI map by clicking on one of the maps. Navigate yourself to the folder **Step_5_View_data**

```
view_HE_VEGF_MR(sample)
```



* Raw DTI images are stored as compressed *.nii.gz* files. These can be viewed e.g. by GUI in [Multidimensional Diffusion MRI software (GitHub)](https://github.com/markus-nilsson/md-dmri).

```
%Clone repository first from https://github.com/markus-nilsson/md-dmri 
run setup_paths %Sets paths into the environment
mgui %Opens GUI
```
* Processed MR and histological slides are stored as *.mat* files and larger ones as *.mat -v7.3* files. The reason for chosing *.mat -v7.3* was that it provided faster reading and writing compared with storing them as *.tif* files, at least for the MATLAB environment.
  * The *.mat (-v7.3)* can opened using MATLAB that necessitate license but also by a free software [Octave](https://octave.org). The images in Octave can be stored as *.tif* images instead (or other image formats without compression):

```
load filename.mat %HE.mat or VEGF.mat or similar
imwrite(HE,'filename_tif','tif') %Often the structure name is HE, VEGF or similar
```

  * The data can also be opened in Python by using mat73 module:

```
pip install mat73 #If you did not have mat73 installed
import mat73 #Imports the mat73 module
data = mat73.loadmat('filename.mat') #Opens the file with name 'filename.mat'
```

## Data structure
* The data folder contains 16 folders numbered **1** to **16** where each corresponds to a single tumor sample. Each sample (**1-16**) has following sub-folders:
  * **raw_histo** folder contains multi-image *.tif* files of the histology as scanned by the digital pathology slides scanner. The *.tif* files provide 3 images with red, green and blue channels separated into three different images. The metadata obtained during the digitalization of the slices are stored in the *Metadata_HE.csv* and *metadata_VEGF.csv*. Samples 1 and 11 do not contain VEGF- but only H&E-stained histology slides because the VEGF files were corrupted during saving from the pathology slide scanner. Sample 12 does not contain metadata for the HE-stained histology slide (the file was deleted by mistake).
  * **init_MR** sub-folder contains DTI maps of a single slice prior to coregistration saved as *.mat* file.
  * **coreg_rigid** sub-folder contains approximately aligned histology with MR.
  * **coreg_fine** sub-folder contains coregistered DTI images in *MR.mat*, cropped H&E in *HE.mat*, defined landmarks in *HE_lm_fine.mat* and structure anisotropy map that helped to coregister the images in the file *aniso2coreg.mat* (see [our manuscript](https://github.com/jan-brabec/microimaging_vs_histology_in_meningeomas)).
  * **cell_density** sub-folder contains QuPath project with cell nuclei detected (see [our manuscript](https://github.com/jan-brabec/microimaging_vs_histology_in_meningeomas)).
  * **structure_anisotropy** sub-folder contains structure anisotropy maps (see [our manuscript](https://github.com/jan-brabec/microimaging_vs_histology_in_meningeomas)).
* The data folder also contains **DTI_raw**.
  * **raw** sub-folder contains raw *.nii* files from the two measurements of the sample holder (upper part and lower part of the sample holder)
  * **processed** sub-folder contains processed raw DTI data by DTI pipeline in [Step_1_Process_DTI](https://github.com/jan-brabec/microimaging_histology_DIB/tree/main/Step_1_Process_DTI).

## Summary of the DTI maps coregistered to the H&E-stained histology images.
* These are stored in the *MR* structure in *MR.mat* and contain
  * Calculated maps : S0 map, mean diffusivity (*MD*), fractional anisotropy (*FA*), in-plane fractional anisotropy (*FAIP*), axial diffuvisity (*AD*), radial diffusivity (*RD*).
  * Orientationally averaged diffusion-weighted data at 100 s/mm2 (single measurement), 1000 s/mm2 (averaged across 6 directions) and 3000 s/mm2 (also averaged across six directions) in the field *PA*.
  * All 13 diffusion-weighted measurements before averaging or calculating maps in field *DWI*.

## How to recreate the coregistered data from raw data

### Step 0: Preparations
1. Analysis was performed with MATLAB version R2020a so make sure you have installed MATLAB. If you do not have license for MATLAB, some of the MATLAB functionalities may be supported by free software [Octave](https://octave.org).
2. Clone [Multidimensional diffusion MRI repository](https://github.com/markus-nilsson/md-dmri) and run *setup_paths*.
3. Modify *dti_lls_4d_fit2param* function stored in file *mdm-dmri/methods/dti_llsdti_lls_4d_fit2param.m*. This is needed to save the estimated full diffusion tensor which is important later on for calculation of the in-plane FA (FAIP). Add line following code anywhere after line 24

```
dps.fulldt = dt_1x6; %paste anywhere below line 24 in the script mdm-dmri/methods/dti_llsdti_lls_4d_fit2param.m
```



### Step 1: Initialize
4. Process the raw DTI data by running script *a_DTI_meningiomas_pipeline* in the folder **Step_1_init** from this repository.
5. Create MR structure for the coregistration by running script *b_create_MR* in the folder **Step_1_init**. This will create **init_MR** folder.
6. Create thumbnails for the H&E and VEGF-stained histology by running *c_create_histo_thumbnail.m*. This will create thumbnails in the **raw_histo** folder to give a quick overview of the data.

### Step 2: Landmark-based rigid coregistration of H&E and VEGF images to MRI
7. Align approximately the histological slices with MR slices by running the script *register* in the folder **Step_3_Coreg_rigid**. See details in the section [Details of ridig coregistration](https://github.com/jan-brabec/microimaging_histology_DIB/blob/main/README.md#details-of-rigid-coregistration-step-2) below.



### Step 3: Landmark-based deformable coregistration of MRI to H&E images
8. Coregister the MR to histology by landmark-based approach for each sample by running the script *a_Coreg_fine_MR_to_HE* in the folder **Step_4_Coreg_HE_fine**. See further instructions below in the section [Details of land-mark based coregistration](https://github.com/jan-brabec/microimaging_histology_DIB/blob/main/README.md#details-of-landmark-based-deformable-coregistration-step-3) below.
9. Verify the position by *b_Validate_coregistration*. Click on either H&E or MRI image in the upper row and the bottom row will show zoom-in in the MRI image as well as corresponding histology patch.
10. Create a mask around H&E imageby running *draw_HE_mask* in folder **Step_3_Coreg_HE_fine**.
11. Apply H&E mask to all coregistered images by *d_apply_HE_mask*. This will replace HE.mat files in the **Step_3_Coreg_HE_fine** with the same H&E but masked. This will also store downsample H&E mask. For quantification analyses, it is useful to combine ROI around MR images with downsampled HE mask. This will make sure that only tumor regions are selected for the analysis.

### Step 4: Landmark-based rigid coregistration of VEGF to H&E images

12. Define landmarks on the H&E and VEGF maps by running script *a_Define_landmarks* in the folder **Step_5_Coreg_VEGF_to_HE**. The interface is the same as in the previous step but do not interpolate to obtain the deformable grid or register. Define landmarks and click 's' to save them.
13. Coregister the VEGF-stained histology to H&E-stained histology by running the script *b_Coregister_VEGF_to_HE*.
14. Investigate the quality of coregistration by running script *c_Validate_coregistration* and repeat defining newer landmarks if necessary.

### Step 5: View data

15. View the data by running the script *view_data* in the folder **Step_5_View_data**. Within this folder, you may also directly use function

```
view_HE_VEGF_MR(sample)
```


### What next?
16. You may see a sample analysis using cell density, structural anisotropy and by convolutional neuronal networks in the [repository related to our manuscript: Mean diffusivity and fractional anisotropy at the mesoscopic level in meningioma tumors: Relation with cell density and tissue anisotropy](https://github.com/jan-brabec/microimaging_vs_histology_in_meningeomas).

## Details of rigid coregistration (Step 2)
In this step, the histology image is cropped and rotated to approximately match the MR image without its shearing or image deformation. This is performed by running *Register* which performs following steps:
* Cropping: Points of the bounding box for each sample defined in *get_cropping_points*.
* Basic rotation such as by 90 or 180 degrees: Rotations defined in *get_H_transform*.
* More precise rotation calculated from landmarks on DTI map (MD or FA) and histology images: landmark points defined in *get_landmarks*. Out of these a more precise rotation angle is calculated. Since the goal is to define rotation angle only, these are often defined on the tumor borders clearly visible in both H&E and MRI image.
* The validate quality of coregistration the script *Register* outputs an image in the main folder. Here, the overlap between the landmark is shown. 


## Details of landmark-based deformable coregistration (Step 3)
* It coregisters image B (MRI) to image A (H&E) by creating a deformable meshgrid over over image B (MRI) based on define landmarks. It also cropps image A (H&E).
* These are defined both on both images in a way that we are certain that these landmarks are the same object in image A and B. For example, these can be tumor borders clearly visible on both histology and MRI image. Another within the tumors are high values of MD in MRI image and presence of vessels in the H&E image.
* The landmark-based coregistration tool was written by Markus Nilsson (markus.nilsson@med.lu.se). Contact Markus for e.g. further collaboration on the development of the tool.


### GUI
* The coregistration can be performed in GUI by running *Coreg_fine_MR_to_HE* in the folder **Step_4_Coreg_HE_fine**.

![alt text](https://github.com/jan-brabec/microimaging_histology_DIB/blob/main/Landmark_coregistration.png?raw=true)

In total 6 subplots appear.
* In the left column above we can observe H&E images with defined 10 landmarks (white color) where the active (6th) landmark is presented with yellow color. Similarly, below we can observe MD images with the same landmarks.
* In the middle column we can observe a zoom-in on the active landmark in the H&E image (above) and MR (below) to fine tune its position.
* In the right column we can observe deformable grid. Upper row shows grid over H&E. This is not deformed as H&E image is only cropped. The bottom row shows grid over MR image (here MD). The grid is deformed based on the distance between the landmarks.

* The GUI can be controlled by pressing:
  * a - adds landmark
  * d - deletes landmark
  * l - loads landmark file
  * s - saves landmark file
  * n - goes to next landmark
  * p - goes to previous landmark
  * i - shows the interpolation grid
  * r - computes final results and stores it in the folder **coreg_fine**

* We can also define landmarks based on FAIP and calculated structure anisotropy map. This we can do by exchanging the code in *Coreg_fine_MR_to_HE*

```
mn_reg_finetune(HE,MR.MD,lm_fn,o_pth,MR,'MR2HE',sample)
```

to this code

```
load(fullfile(o_pth,'aniso2coreg.mat'),'cFA') %this will load the calculated structure anisotropy map
mn_reg_finetune(cFA,MR.FAIP,lm_fn,o_pth,MR,'MR2HE',sample) %this will coregister FAIP map to structure anisotropy map
```


## Additional notes
* The histology slide scanner provided histology slides in *.svs* format. These were later saved as *.tif* files using [ImageJ](https://imagej.nih.gov/ij/index.html) (version 1.53t) with [Bioformat plugin](https://docs.openmicroscopy.org/bio-formats/5.8.2/users/imagej/installing.html) (version 6.11.1) that needs to be installed separately. Alternatively, they can be saved as *.tif* using [Fiji](https://imagej.net/software/fiji/downloads) which is one of the distribution of ImageJ containing Bioformat plugin. The red, green and blue channels were separated into three images within a single *.tif* file using Autoscale option on. The *.svs* files are not provided because they contains important metadata. The metadata from the slide scanner are, however, provided in the file **raw_histo** as *Metadata_HE.csv* or *Metadata_VEGF.csv*.
* Samples 1 and 11 do not contain VEGF- but only H&E-stained histology slides because the VEGF files were corrupted during saving from the pathology slide scanner.
* Sample 12 does not contain metadata for the HE-stained histology slide (the file was deleted by mistake).
* Licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
