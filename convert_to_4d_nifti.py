# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 11:03:31 2017

@author: claire
"""

import os
import os.path as op
import shutil

from nipype.caching import Memory # to use nipype in simple python scripts (ie. not nipype pipeline)
from nipype.interfaces import fsl



root_dir = '/media/claire/NAS-DATA/EMPATHYP_DATA/Subjects_new_preprocessing/'
res_dir = '/home/claire/DATA/Empathyp/MVPA/Subjects/'
subj_list = ['S03', 'S05', 'S07', 'S08', 'S09', 'S10', 'S13', 'S15', 'S16', 'S18', 'S20']
cond_list = ['hypno1', 'hypno2', 'norm1', 'norm2'] #, '


for subj in subj_list:
    for cond in cond_list:
        # set path and output filename
        data_path=op.join(root_dir, subj, cond) 
        res_fname = cond + '.nii.gz'
        res_path = op.join(res_dir, subj, res_fname)
        os.chdir(data_path)
        # list all nii files we want
        fname= [f for f in os.listdir(data_path) if f.startswith('rf')]
        # nipype setup
        mem = Memory(base_dir='.')
        fsl_merge = mem.cache(fsl.Merge)
        results=fsl_merge(dimension = 't', tr = 2.1, output_type = 'NIFTI_GZ', in_files = fname)     
        # move output file to new location and rename
        shutil.move(results.outputs.merged_file, res_path)
        mem.clear_previous_runs()