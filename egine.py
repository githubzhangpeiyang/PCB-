from DataReader import get_part_list,get_pad_list
from matplotlib import pyplot as plt
from DataInfo import pad_struct,part_struct
import tooslib
import random
# iteam='8XJ038048/8XJ038048'
# iteam='MU_V3_A3AASC2_V2/MU_V3_A3AASC2_V2'
# iteam='T6-532J3701-R (TGZ)/T6-532J3701-R (TGZ)'
# iteam='288/288'
# iteam='CC0_100500-B/CC0_100500-B'
# iteam='DVI10_V2.4.2_ODB_20180411/DVI10_V2.4.2_ODB_20180411'
# iteam='n-5180/n-5180'
iteam='USa/USa'
pad_file_path='DataSP/'+iteam+'_Pad.txt'
part_file_path='DataSP/'+iteam+'_Part.txt'
pad_list=get_pad_list(pad_file_path)
part_list=get_part_list(part_file_path)
tooslib.serch_rc(pad_list,part_list)
# print pad_list
# print part_list
pad_info_list=[]
part_info_list=[]
for p_index, pad in enumerate(pad_list):
    if pad[3] == 0:
        pad_info_list.append(pad_struct(p_index, pad))

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
devices_index_sta=tooslib.get_devieces_do_index(pad_info_list,part_info_list)
# print devices_index_sta

    # part_info.centerx=part_info.centerx-0.5*part_max_x-0.5*part_min_x
    # part_info.centery=part_info.centery-0.5*part_max_y-0.5*part_min_y
# for pad in pad_list:
#     pad_info_list.append(pad_struct(pad))
# for part in part_list:
#     part_info_list.append(part_struct(part))

# init_list=[]
# for pad_info in pad_info_list:
#     pad_info.get_near_index(part_info_list)
#     init_list.append(pad_info.nearst_index)
# ans=[]
# for pad_info in pad_info_list:
#     pad_info.get_ans_index(part_info_list)
#     ans.append(pad_info.answer)



devices_label=tooslib.find_device_with_label(pad_info_list,part_info_list)
# for key,val in devices_label.items():
#     if len(val)==2:
#         print val[0].part_name

# tooslib.dist_statsctic(pad_info_list,part_info_list)
# tooslib.final_search(pad_info_list,part_info_list)

# tooslib.second_search(pad_info_list,part_info_list,max_edge=50)
tooslib.second_search(pad_info_list,part_info_list,max_edge=75)
# tooslib.third_search(pad_info_list,part_info_list,max_edge=15)
tooslib.draw_device(devices_label,show_center=True,show_text=False,do_index=devices_index_sta)
