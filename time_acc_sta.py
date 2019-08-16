from DataReader import get_part_list,get_pad_list
from matplotlib import pyplot as plt
from DataInfo import pad_struct,part_struct
import tooslib
import random
import os
import pandas as pd
from pandas import DataFrame
import time
# iteam='8XJ038048/8XJ038048'
# iteam='MU_V3_A3AASC2_V2/MU_V3_A3AASC2_V2'
# iteam='T6-532J3701-R (TGZ)/T6-532J3701-R (TGZ)'
# iteam='288/288'
# iteam='CC0_100500-B/CC0_100500-B'
# iteam='DVI10_V2.4.2_ODB_20180411/DVI10_V2.4.2_ODB_20180411'
# iteam='n-5180/n-5180'
# iteam='USa/USa'
# fileSaveDir='DataRE'
# if os.path.exists(fileSaveDir):
#     pass
# else:
#     os.makedirs(fileSaveDir)
root_path='DataSP'
iteam_names=os.listdir(root_path)
PCB_Name=[]
Time=[]
ACC=[]
DACC=[]
NDN=[]
Part_num=[]
Pad_num=[]
for iteam_name in iteam_names:
    time_start=time.time()
    iteam=iteam_name+'/'+iteam_name
    # iteam = 'n-5180/n-5180'
    pad_file_path=root_path+'/'+iteam+'_Pad.txt'
    pad_file_save_path=root_path+'/'+iteam+'_Pad_Result.txt'
    part_file_path=root_path+'/'+iteam+'_Part.txt'
    pad_list=get_pad_list(pad_file_path)


    part_list=get_part_list(part_file_path)
    tooslib.serch_rc(pad_list,part_list)

    pad_info_list=[]
    part_info_list=[]
    for p_index,pad in enumerate(pad_list):
        if pad[3]==0:
            pad_info_list.append(pad_struct(p_index,pad))

    part_max_x=None
    part_min_x=None
    part_max_y=None
    part_min_y=None
    for part in part_list:
        if part[5]==[]:
            part_info_list.append(part_struct(part))
            if part_max_x==None:
                part_max_x=part[0]
                part_min_x=part[0]
                part_max_y=part[1]
                part_min_y=part[1]
            else:
                if part[0]>part_max_x:
                    part_max_x=part[0]
                if part[0]<part_min_x:
                    part_min_x=part[0]
                if part[1]>part_max_y:
                    part_max_y=part[1]
                if part[1]<part_min_y:
                    part_min_y=part[1]
    for part_info in part_info_list:
        part_info.centerx=part_info.centerx-0.5*part_max_x-0.5*part_min_x
        part_info.centery=part_info.centery-0.5*part_max_y-0.5*part_min_y
    for pad_info in pad_info_list:
        if pad_info.shape=='ROUND':
            pad_info.centerx=pad_info.centerx-0.5*part_max_x-0.5*part_min_x
            pad_info.centery = pad_info.centery - 0.5 * part_max_y - 0.5 * part_min_y
            pad_info.points_list[0]=pad_info.points_list[0]-0.5*part_max_x-0.5*part_min_x
            pad_info.points_list[1] = pad_info.points_list[1] - 0.5 * part_max_y - 0.5 * part_min_y
        elif pad_info.shape=='RECT':
            pad_info.centerx = pad_info.centerx - 0.5 * part_max_x - 0.5 * part_min_x
            pad_info.centery = pad_info.centery - 0.5 * part_max_y - 0.5 * part_min_y
            pad_info.points_list[0] = pad_info.points_list[0] - 0.5 * part_max_x - 0.5 * part_min_x
            pad_info.points_list[1] = pad_info.points_list[1] - 0.5 * part_max_y - 0.5 * part_min_y
            pad_info.points_list[2] = pad_info.points_list[2] - 0.5 * part_max_x - 0.5 * part_min_x
            pad_info.points_list[3] = pad_info.points_list[3] - 0.5 * part_max_y - 0.5 * part_min_y
        else:
            pad_info.centerx = pad_info.centerx - 0.5 * part_max_x - 0.5 * part_min_x
            pad_info.centery = pad_info.centery - 0.5 * part_max_y - 0.5 * part_min_y
            for index,ele in enumerate(pad_info.points_list):
                if index%2==0:
                    pad_info.points_list[index] = pad_info.points_list[index] - 0.5 * part_max_x - 0.5 * part_min_x
                else:
                    pad_info.points_list[index] = pad_info.points_list[index] - 0.5 * part_max_y - 0.5 * part_min_y
    for pad_info in pad_info_list:
        pad_info.get_ans_index(part_info_list)
    tooslib.second_search(pad_info_list,part_info_list,max_edge=75)
    time_end=time.time()
    time_use=time_end-time_start
    right_num=0
    for ele in pad_info_list:
        if ele.do==ele.answer:
            right_num+=1
    acc=(right_num+len(pad_list)-len(pad_info_list))*1.0/len(pad_list)
    Time.append(time_use)
    PCB_Name.append(iteam_name)
    # ACC.append(acc)
    Part_num.append(len(part_list))
    Pad_num.append(len(pad_list))
    for pad_info in pad_info_list:
        pad_list[pad_info.ori_index][3]=pad_info.result
    content_lines=[]
    done_num=0
    right_num=0
    all_num=len(pad_list)
    for p_d in pad_list:
        # content=str(p_d[3])+'\n'
        if str(p_d[3])==str(p_d[-1]):
            right_num+=1
        if p_d[3] is not None:
            done_num+=1
        content = str(p_d[3]) + ' ' + str(p_d[-1]) + '\n'
        content_lines.append(content)
    ACC.append(1.0*right_num/all_num)
    DACC.append(1.0*right_num/done_num)
    NDN.append(1.0*(all_num-done_num)/all_num)
    with open(pad_file_save_path,'w') as file_write_obj:
        file_write_obj.writelines(content_lines)
excel_table_path = 'statistic.xlsx'
writer = pd.ExcelWriter(excel_table_path)
data = DataFrame(data={'PCB_Name': PCB_Name,'Time':Time,
                       'Part_num':Part_num,'Pad_num':Pad_num,
                       'ACC':ACC,'DACC':DACC,'NDR':NDN
                       })
DataFrame.to_excel(data, writer, sheet_name='Sheet1', startcol=0)


    # tooslib.third_search(pad_info_list,part_info_list,max_edge=15)
    # tooslib.draw_device(devices_label,show_center=True,show_text=False,do_index=devices_index_sta)
