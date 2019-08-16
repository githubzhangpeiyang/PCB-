import os
import pandas as pd
from pandas import DataFrame
root_path='DataSP'
iteam_names=os.listdir(root_path)
PCB_Name=[]
Time=[]
ACC=[]
Part_num=[]
Pad_num=[]
for iteam_name in iteam_names:
    iteam=iteam_name+'/'+iteam_name
    # iteam = 'n-5180/n-5180'
    pad_file_path=root_path+'/'+iteam+'_Pad.txt'
    pad_file_save_path=root_path+'/'+iteam+'_Pad_Result.txt'
    part_file_path=root_path+'/'+iteam+'_Part.txt'
    pad_list=get_pad_list(pad_file_path)
