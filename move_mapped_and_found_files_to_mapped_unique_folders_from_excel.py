#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
import glob
#import fnmatch
#import shutil

parent_dir = "Raw_Data"
root_path = 'Batch'
qc_report = pd.read_excel("QC_Report.xlsx")
unique_study_ids = qc_report["STUDY_ID"].unique() #few unique ids

def grep(l, s):
    return [i for i in l if s in i]
  
# Get all idat files and their paths
files = []
for root, dir, files in os.walk(parent_dir):
    for file in files:
        if '.idat' in file:
            files.append(os.path.join(root, file))

# Make a folder with all of the unique study ids
for folder in unique_study_ids:
  os.mkdir(os.path.join(root_path,folder))

# Generate bash script to move or copy files
print("#!/bin/bash")
for index, row in qc_report.iterrows():
    # Generate the partial name of the idat files (red and green) from the excel file
    partial_idat_name = str(row['Sentrix_ID'])+"_"+str(row['Sentrix_Position'])
    study_id = row['STUDY_ID']
    # Map the generated partial idat name to the files and their paths
    found_idat_files = grep(files, partial_idat_name)
    # For every found idat mapped to the generated partial name from the excel file
    # Move those files to the unique study id folder
    # _it is always better and safer to copy instead of move_
    for i, val in enumerate(found_idat_files):   
        idat_basename = os.path.basename(found_idat_files[i])
        print("mv ",found_idat_files[i]," ",root_path,"/",study_id,"/",idat_basename, sep="")
