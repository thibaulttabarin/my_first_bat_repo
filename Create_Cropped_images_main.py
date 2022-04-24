# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 09:35:59 2021

@author: tabarin
"""
import os
import sys
#Mon13Dec21_Neon
import json
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.patches as patches
from PIL import Image
import pandas as pd
#import Drexel_metadata_TT_util as Drex_util
from pathlib import Path

#Images_folder_path = '/home/thibault/Documents/Data/Experiment_1/Images'
#metadata_drexel = '/home/thibault/Documents/Data/Experiment_1/metadata.json'


def Create_bbox_df(metadata_json_path):
    '''
    From the metadata.json, extract the bounding box and create dataframe column: file_nmae, bbox
    Select images where a fish has been detected
    boox value is list [left,top,right,bottom]
    When not fish is detected value is nan
    Parameters
    ----------
    metadata_json_path : path for the metadata.json
        DESCRIPTION.

    Returns
    -------
    TYPE pandas dataframe
        DESCRIPTION.
        column: file_nmae, bbox
    '''    
     
    # Import the metadata.json into a dataframe
    df_metadata = pd.read_json(metadata_json_path)

    # Transpose
    df_metadata_T = df_metadata.T
    # convert Index to columnn
    df_metadata_T = df_metadata_T.reset_index()
    # Rename column index => file_name 
    df_metadata_T = df_metadata_T.rename(columns={"index": "file_name"})


    # Apply a function to a column only on specific location (condition on other column)
    temp_bbox = df_metadata_T.loc[df_metadata_T['has_fish']==True, 'fish'].apply(lambda x : x[0]['bbox'])
    df_metadata_T.loc[df_metadata_T['has_fish']==True, 'bbox'] = temp_bbox
    
    return df_metadata_T[['file_name','bbox']]



def main(folder_path):
    
    Images_folder_path = os.path.join(folder_path, 'Images')
    metadata_json_path = os.path.join(folder_path, 'metadata.json')
       
    #%% Create a reshape the dataframe for file_name and bbox and create dictionnary

    df_bbox = Create_bbox_df(metadata_json_path)
    bbox_dict = pd.Series(df_bbox.bbox.values,index=df_bbox.file_name).to_dict()

    #%% Create the folder

    path1 = Path(Images_folder_path)
    Images_cropped_path = os.path.join(path1.parent, 'Images_cropped')
    if not os.path.isdir(Images_cropped_path):
        os.mkdir(Images_cropped_path)
    
#%%

    #file_path_test =os.join(Images_folder_path,filenames[0])
    

    for filename, bbox in bbox_dict.items():
        
        if not np.isnan(bbox).any():
            
            file_path = os.path.join(Images_folder_path,filename)
            if os.path.isfile(file_path):
            
                im = Image.open(file_path)
        
                im1 = im.crop(bbox) # bbox [left,top,right,bottom]
        
                file_path_saved = os.path.join(Images_cropped_path, filename)
                im1.save(file_path_saved)
            else :
                print('{} doesn\'t exist, we skipped it'.format(filename) )
        else: print('In {} no fish has been detected'.format(filename) )
        
    
    
if __name__ == '__main__':
    
    main(sys.argv[1])    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    