from matplotlib import pyplot as plt
import re
import math
import random
import numpy as np
import cv2
import pandas as pd
from pandas import DataFrame
def serch_rc(pads_in,parts_in,e=15):
    for part_inf in parts_in:
        part_name=part_inf[3]
        if re.match(r'"C{1}\d+"$', part_name, re.I) is not None or re.match(r'"R{1}\d+"$', part_name, re.I) is not None:
            candi_list=[]
            part_center_x=part_inf[0]
            part_center_y=part_inf[1]
            for index,pad_inf in enumerate(pads_in):
                if pad_inf[3]==1:
                    continue
                pad_center_x,pad_center_y=pad_inf[2]
                distance=get_dist(part_center_x,part_center_y,pad_center_x,pad_center_y)
                if distance<e:
                    candi_list.append([index,distance])
                    candi_list=sorted(candi_list,key=lambda x:x[1])
            while len(candi_list)>=2:
                temp_points_list=[pads_in[candi_list[0][0]][2],pads_in[candi_list[1][0]][2]]
                x, y, w, h = my_bounding_rect(temp_points_list)
                device_centerx = x + w / 2.0
                device_centery = y + h / 2.0
                temp_dist = get_dist(device_centerx, device_centery, part_center_x, part_center_y)
                if temp_dist<1e-3:
                    part_inf[-1].append(candi_list[0][0])
                    part_inf[-1].append(candi_list[1][0])
                    pads_in[candi_list[0][0]][3] = part_name
                    pads_in[candi_list[1][0]][3] = part_name
                    break
                else:
                    candi_list.remove(candi_list[0])
            # if len(candi_list)<2:
            #     part_inf[-1].append('ERROR!')
            #     print 'e_ERROR!'
            # else:
            #     part_inf[-1].append(candi_list[0][0])
            #     part_inf[-1].append(candi_list[1][0])
            #     pads_in[candi_list[0][0]][3]=part_name
            #     pads_in[candi_list[1][0]][3] = part_name
def get_dist(x1,y1,x2,y2):
    del_x=x1-x2
    del_y=y1-y2
    return math.sqrt(del_x**2+del_y**2)
def find_device_with_label(pad_info_l_in,part_inf_l_in):
    parts_dict={}
    for part_inf in part_inf_l_in:
        PartX, PartY, Angle, PartName, PackageName = part_inf.centerx,part_inf.centery,\
                                                     part_inf.angel,part_inf.part_name,part_inf.package_name
        parts_dict[PartName]=[part_inf]
        for index,pad_info in enumerate(pad_info_l_in):
            if pad_info.label==PartName:
                parts_dict[PartName].append(pad_info)
    return parts_dict
def find_device_nearst(pad_info_l_in,part_inf_l_in):
    parts_dict={}
    for part_inf in part_inf_l_in:
        PartX, PartY, Angle, PartName, PackageName = part_inf.centerx,part_inf.centery,\
                                                     part_inf.angel,part_inf.part_name,part_inf.package_name
        parts_dict[PartName]=[part_inf]
        for pad_info in pad_info_l_in:
            if pad_info.nearst_index is None:
                print 'pad_info.nearst_index is None!Init it befor use!'
                return None
            if part_inf_l_in[pad_info.nearst_index].part_name==PartName:
                parts_dict[PartName].append(pad_info)
    return parts_dict
def draw_pad(type_name,points,pad_center,color,show_center):
    x=[]
    y=[]
    if type_name=='RECT':
        minx, miny, maxx, maxy=points
        x = [minx, maxx, maxx, minx, minx]
        y = [miny, miny, maxy, maxy, miny]
    elif type_name=='ROUND':
        centerx, centery, diameter=points
        num_points=30
        radius = diameter / 2.0
        x = []
        y = []
        for i in range(num_points):
            angel = 0 + 2 * math.pi * (i * 1.0 / (num_points - 1))
            x.append(centerx + radius * math.sin(angel))
            y.append(centery + radius * math.cos(angel))
    elif type_name=='POLY':
        data_in=points
        x = []
        y = []
        for i in range(len(data_in)):
            if i % 2 == 0:
                x.append(data_in[i])
            else:
                y.append(data_in[i])
        x.append(x[0])
        y.append(y[0])
    if show_center:
        plt.scatter(pad_center[0],pad_center[1],color=color,marker='.')
        # x.append(pad_in[2][0])
        # y.append(pad_in[2][1])
    plt.plot(x,y,color=color)
def draw_part(PartX, PartY,color,marker):
    plt.scatter(PartX, PartY, c=color, marker=marker)
def my_bounding_rect(points):
    x_min=points[0][0]
    y_min=points[0][1]
    x_max=points[0][0]
    y_max=points[0][1]
    for point in points:
        if point[0]<x_min:
            x_min=point[0]
        if point[0]>x_max:
            x_max=point[0]
        if point[1]<y_min:
            y_min=point[1]
        if point[1]>y_max:
            y_max=point[1]
    return x_min,y_min,x_max-x_min,y_max-y_min
def draw_device(devices,show_center=False,show_text=False,show_edge=False,do_index=None):
    plt.figure(figsize=(50,50))
    plt.axis("equal")
    for part_name, pad_info in devices.items():
        PartX, PartY, Angle, PartName, PackageName = pad_info[0].centerx,pad_info[0].centery, \
                                                     pad_info[0].angel,pad_info[0].part_name,pad_info[0].package_name
        r = random.random()
        g = random.random()
        b = random.random()
        color = (r, g, b)
        if len(pad_info)==1:
            plt.text(PartX, PartY, PartName, color='r', fontsize=20)
            draw_part(PartX, PartY, color='r', marker='+')
            print 'NONE!!'
            continue
        sum_pad_x = 0
        sum_pad_y = 0
        points_list=[]
        for index, pad in enumerate(pad_info):
            if index == 0:
                continue
            sum_pad_x += pad.centerx
            sum_pad_y += pad.centery
            points_list.append([pad.centerx, pad.centery])
            draw_pad(pad.shape,pad.points_list,(pad.centerx,pad.centery), color=color, show_center=show_center)
        sum_pad_x /= (len(pad_info) - 1)
        sum_pad_y /= (len(pad_info) - 1)
        points_nda = np.array(points_list, dtype=np.float32)

        # box2d = cv2.minAreaRect(points_nda)
        # if (box2d[1][0]<1e-3 or box2d[1][1]<1e-3) and abs(box2d[-1]-180.0)<1e-3:
        #     box2d=list(box2d)
        #     box2d[1]=list(box2d[1])
        #     box2d[1]=(box2d[1][1],box2d[1][0])
        #     box2d[-1]=0
        #     box2d=tuple(box2d)
        # boundary4points = cv2.boxPoints(box2d)

        lx, ly, w, h = my_bounding_rect(points_nda)
        boundary4points=[[lx,ly],[lx+w,ly],[lx+w,ly+h],[lx,ly+h]]


        boundary4points_x = [x[0] for x in boundary4points]
        boundary4points_x.append(boundary4points[0][0])
        boundary4points_y = [x[1] for x in boundary4points]
        boundary4points_y.append(boundary4points[0][1])
        # rect = plt.Rectangle(boundary4points[1], box2d[1][0], box2d[1][1], angle=box2d[2], fill=False)
        # rect.contains_point([15.0, 7.6])

        plt.plot(boundary4points_x, boundary4points_y, color=(0.5, 0.24, 1))

        # plt.scatter(box2d[0][0], box2d[0][1], color=(0.1, 0.75, 0.1), marker='x')
        # print x,y,w,h
        plt.scatter(lx+w/2, ly+h/2, color=(0.1, 0.75, 0.1), marker='x')

        # temp_dist = get_dist(PartX, PartY, sum_pad_x, sum_pad_y)
        # plt.scatter(sum_pad_x, sum_pad_y, color='k', marker='x')
        draw_part(PartX, PartY, color=color, marker='+')

        # if PartName in ("\"CN11\"","\"CN23\"","\"CN5\""):
        #     print 'in'
        #     plt.text(PartX, PartY, PartName, color=color, fontsize=10)

        if show_text:
            plt.text(PartX, PartY, PartName, color=color, fontsize=10)
            # plt.text(PartX, PartY, PartName + '+' + PackageName, color=color, fontsize=10)
        if do_index!=None:
            plt.text(PartX, PartY, str(do_index[PartName]), color=color, fontsize=10)

    plt.savefig('qwe.jpg')
    plt.show()
def draw_circle(cx,cy,r,color):
    theta = np.linspace(0, 2*np.pi,50)
    q,w = cx+np.cos(theta)*r, cy+np.sin(theta)*r
    plt.plot(q, w, color=color, linewidth=1.0)
    plt.scatter(cx, cy, color=color, marker='x')
def draw_cmp(solution_index,answer_index,pad_inf_l,part_inf_l):
    plt.axis('equal')
    print len(solution_index)
    for e_num,index in enumerate(solution_index):
        if index==answer_index[e_num]:
            draw_pad(pad_inf_l[e_num].shape,pad_inf_l[e_num].points_list,
                     (pad_inf_l[e_num].centerx,pad_inf_l[e_num].centery),color='g',show_center=True)
        else:
            draw_pad(pad_inf_l[e_num].shape, pad_inf_l[e_num].points_list,
                     (pad_inf_l[e_num].centerx, pad_inf_l[e_num].centery), color='r', show_center=True)
    for part_inf in part_inf_l:
        draw_part(part_inf.centerx,part_inf.centery,color='g',marker='+')

    parts_ans_dict = {}
    for e_num,index in enumerate(answer_index):
        if index not in parts_ans_dict:
            parts_ans_dict[index]=[e_num]
        else:
            parts_ans_dict[index].append(e_num)
    for key,val in parts_ans_dict.items():
        points=[]
        for e_num in val:
            points.append([pad_inf_l[e_num].centerx,pad_inf_l[e_num].centery])
        cx,cy,r=get_out_circle(points)
        draw_circle(cx,cy,r,color='y')

    parts_solu_dict = {}
    for e_num,index in enumerate(solution_index):
        if index not in parts_solu_dict:
            parts_solu_dict[index]=[e_num]
        else:
            parts_solu_dict[index].append(e_num)
    for key,val in parts_solu_dict.items():
        points=[]
        for e_num in val:
            points.append([pad_inf_l[e_num].centerx,pad_inf_l[e_num].centery])
        cx,cy,r=get_out_circle(points)
        draw_circle(cx,cy,r,color='m')
    pass
def get_outer_circle_three(A,B,C):
    a1=B[0]-A[0]
    b1=B[1]-A[1]
    c1=(a1*a1+b1*b1)/2.0
    a2=C[0]-A[0]
    b2=C[1]-A[1]
    c2 = (a2 * a2 + b2 * b2)/2.0
    d = (a1 * b2 - a2 * b1)*1.0
    if d!=0:
        x = A[0] + (c1 * b2 - c2 * b1) / d
        y = A[1] + (a1 * c2 - a2 * c1) / d
        return x,y
    else:
        point_list=[A,B,C]
        point_list=sorted(point_list,key=lambda x:(x[0],x[1]))
        x,y=point_list[1]
        return x,y
def get_out_circle(points):
    point_num=len(points)
    eps = 1e-8
    if point_num==1:
        return points[0][0],points[0][1],0
    elif point_num==2:
        return (points[0][0]+points[1][0])/2.0,(points[0][1]+points[1][1])/2.0,get_dist(points[0][0],points[0][1],(points[0][0]+points[1][0])/2.0,(points[0][1]+points[1][1])/2.0)
    else:
        center=[points[0][0],points[0][1]]
        r=0
        for i in range(1,point_num):
            if get_dist(center[0],center[1],points[i][0],points[i][1])+eps>r:
                center = [points[i][0], points[i][1]]
                r=0
                for j in range(i):
                    if get_dist(center[0],center[1],points[j][0],points[j][1])+eps>r:
                        center[0]=(points[i][0]+points[j][0])/2.0
                        center[1] = (points[i][1] + points[j][1]) / 2.0
                        r=get_dist(center[0],center[1],points[j][0],points[j][1])
                        for k in range(j):
                            if get_dist(center[0],center[1],points[k][0],points[k][1])+eps>r:
                                center[0],center[1]=get_outer_circle_three(points[i],points[j],points[k])
                                r=get_dist(center[0],center[1],points[k][0],points[k][1])
        return center[0],center[1],r
def out_circle_and_index(points,index_in):
    point_num=len(points)
    eps = 1e-8
    index_sta={}
    if point_num==1:
        index_sta[index_in[0]]=[]
        return points[0][0],points[0][1],0,index_sta
    elif point_num==2:
        index_sta[index_in[0]] = []
        index_sta[index_in[1]] = []
        return (points[0][0]+points[1][0])/2.0,(points[0][1]+points[1][1])/2.0,get_dist(points[0][0],points[0][1],(points[0][0]+points[1][0])/2.0,(points[0][1]+points[1][1])/2.0),index_sta
    else:
        center=[points[0][0],points[0][1]]
        r=0
        for i in range(1,point_num):
            if get_dist(center[0],center[1],points[i][0],points[i][1])+eps>r:
                center = [points[i][0], points[i][1]]
                r=0
                for j in range(i):
                    if get_dist(center[0],center[1],points[j][0],points[j][1])+eps>r:
                        center[0]=(points[i][0]+points[j][0])/2.0
                        center[1] = (points[i][1] + points[j][1]) / 2.0
                        r=get_dist(center[0],center[1],points[j][0],points[j][1])
                        for k in range(j):
                            if get_dist(center[0],center[1],points[k][0],points[k][1])+eps>r:
                                center[0],center[1]=get_outer_circle_three(points[i],points[j],points[k])
                                r=get_dist(center[0],center[1],points[k][0],points[k][1])
        for e_num,point in enumerate(points):
            if math.fabs(get_dist(point[0],point[1],center[0],center[1])-r)<1e-7:
                index_sta[index_in[e_num]] = []
        return center[0],center[1],r,index_sta
def get_geo_center(points):
    sum_x=0
    sum_y=0
    for point in points:
        sum_x+=point[0]
        sum_y+=point[1]
    sum_x=sum_x*1.0/len(points)
    sum_y=sum_y*1.0/len(points)
    return sum_x,sum_y
def getMinIndex(my_list):
    min = my_list[0]
    for i in my_list:
        if i < min:
            min = i
    return my_list.index(min)
def dist_statsctic(pad_info_l_in,part_inf_l_in):
    devices=find_device_with_label(pad_info_l_in, part_inf_l_in)
    dist_sta=[]
    angle_sta=[]
    angle_label=[]
    width_sta=[]
    height_sta=[]
    number_sta=[]
    bound_sta=[]
    for part_name, pad_info in devices.items():
        PartX, PartY, Angle, PartName, PackageName = pad_info[0].centerx,pad_info[0].centery, \
                                                     pad_info[0].angel,pad_info[0].part_name,pad_info[0].package_name
        if len(pad_info)==1:
            plt.text(PartX, PartY, PartName, color='r', fontsize=20)
            draw_part(PartX, PartY, color='r', marker='+')
            print 'NONE!!'
            continue
        points_list=[]
        for index, pad in enumerate(pad_info):
            if index == 0:
                continue
            points_list.append([pad.centerx,pad.centery])
        points_nda = np.array(points_list, dtype=np.float32)
        x_min,y_min,wid,hei=my_bounding_rect(points_nda)
        my_bounding_disdt=get_dist(PartX, PartY, x_min+wid/2, y_min+hei/2)
        box2d = cv2.minAreaRect(points_nda)
        temp_dist = get_dist(PartX, PartY, box2d[0][0], box2d[0][1])
        dist_sta.append(temp_dist)
        angle_sta.append(box2d[2])
        width_sta.append(box2d[1][0])
        height_sta.append(box2d[1][1])
        angle_label.append(Angle)
        number_sta.append(len(pad_info)-1)
        bound_sta.append(my_bounding_disdt)

    excel_table_path = 'statistic.xlsx'
    writer = pd.ExcelWriter(excel_table_path)
    data = DataFrame(data={'dist_sta': dist_sta,'angle_sta':angle_sta,
                           'angle_label':angle_label,'width_sta':width_sta,'height_sta':height_sta,
                           'number_sta':number_sta,
                           'bound_sta':bound_sta
                           })
    DataFrame.to_excel(data, writer, sheet_name='Sheet1', startcol=0)

    # excel_table_path = 'statistic.xlsx'
    # data_ori = pd.read_excel(excel_table_path)
    # writer = pd.ExcelWriter(excel_table_path)
    # data = DataFrame(data={iteam: dist_list})
    # data_save = pd.concat([data_ori, data], axis=1)
    # data_save = DataFrame(data_save)
    # DataFrame.to_excel(data_save, writer, sheet_name='Sheet1', startcol=0)
def get_device_index(pad_info_l_in,part_inf_l_in):
    pass
def draw_device_with_index(pad_info_l_in,part_inf_l_in):
    pass
def final_search(pad_info_l_in,part_inf_l_in):
    device=find_device_with_label(pad_info_l_in,part_inf_l_in)
    pad_number=1
    toler_thresh=1e-3
    de_thresh=2.5
    part_index_do=[i for i in range(len(part_inf_l_in))]
    pad_index_do=[i for i in range(len(pad_info_l_in))]
    done=True
    record_log_file = open('record.txt', 'w')
    wrong_log_file=open('wrong.txt','w')
    print_index=0
    while True:
        if de_thresh < 1e-3:
            break
        print_index+=1
        print_index%=100000
        if print_index%1000==0:
            print 'part_num:',len(part_index_do),'pad_do_num:',\
                len(pad_index_do),'pad_number:',pad_number,\
                'toler_thresh:',toler_thresh,'de_thresh:',de_thresh

        if len(part_index_do) == 1 or len(pad_index_do) == 0:
            break
        star_iter_num=len(pad_index_do)
        for index in part_index_do:
            if done:
                min_dist = 1e3
                for other_index in part_index_do:
                    if other_index==index:
                        continue
                    temp_dist=get_dist(part_inf_l_in[index].centerx,part_inf_l_in[index].centery,
                                       part_inf_l_in[other_index].centerx, part_inf_l_in[other_index].centery)
                    if temp_dist<min_dist:
                        min_dist=temp_dist
                part_inf_l_in[index].search_radius=min_dist
                # print min_dist
                temp_candi_list = []
                for pad_index in pad_index_do:
                    temp_dist = get_dist(part_inf_l_in[index].centerx, part_inf_l_in[index].centery,
                                         pad_info_l_in[pad_index].centerx, pad_info_l_in[pad_index].centery)
                    if temp_dist<=part_inf_l_in[index].search_radius:
                        temp_candi_list.append([pad_index,temp_dist])
                temp_candi_list=sorted(temp_candi_list,key=lambda x:x[1],reverse=False)
                part_inf_l_in[index].candi_elements=temp_candi_list

            if pad_number>len(part_inf_l_in[index].candi_elements):
                continue
            this_num_dev_dist=0
            find_succeed=False
            for i in range(pad_number,len(part_inf_l_in[index].candi_elements)):
                points_list = []
                for j in range(i):
                    # print len(part_inf_l_in[index].candi_elements),j
                    points_list.append([pad_info_l_in[(part_inf_l_in[index].candi_elements[j][0])].centerx,
                                        pad_info_l_in[(part_inf_l_in[index].candi_elements[j][0])].centery])
                points_nda = np.array(points_list, dtype=np.float32)
                box2d = cv2.minAreaRect(points_nda)
                # print box2d,points_nda
                temp_dist=get_dist(box2d[0][0],box2d[0][1],part_inf_l_in[index].centerx,part_inf_l_in[index].centery)
                if i==pad_number:
                    this_num_dev_dist=temp_dist
                    # print this_num_dev_dist
                    if this_num_dev_dist>toler_thresh:
                        find_succeed=False
                        break
                else:
                    if temp_dist<=de_thresh:
                        find_succeed=False
                        break
                    if i==len(part_inf_l_in[index].candi_elements)-1:
                        if this_num_dev_dist<=toler_thresh:
                            find_succeed=True
            if find_succeed:
                content=str(index)+' '
                for j in range(pad_number):
                    pad_info_l_in[part_inf_l_in[index].candi_elements[j][0]].answer=index
                    pad_index_do.remove(part_inf_l_in[index].candi_elements[j][0])
                    if part_inf_l_in[index].part_name!=pad_info_l_in[part_inf_l_in[index].candi_elements[j][0]].label:
                        print 'lost'
                    else:
                        content+=str(part_inf_l_in[index].candi_elements[j][0])+' '
                content+='\n'
                record_log_file.writelines(content)
                if len(device[part_inf_l_in[index].part_name])-1==pad_number:
                    pass
                    # print 'succeed!','num succeed!'
                else:
                    print 'succeed!','num lost!',pad_number,'/',len(device[part_inf_l_in[index].part_name])
                    wrong_log_file.writelines(str(index)+' '+str(pad_number)+' '+
                                              str(len(device[part_inf_l_in[index].part_name])-1)+' '+
                                              str(de_thresh)+
                                              '\n')
                part_index_do.remove(index)
                done=True
                break
            else:
                pass
        end_iter_num=len(pad_index_do)
        if end_iter_num == star_iter_num:
            done=False
        # if end_iter_num==star_iter_num and pad_number>300:
        #     toler_thresh+=1e-3
        #     pad_number=1
        #     if toler_thresh>=0.01:
        #         toler_thresh=1e-3
        #         de_thresh-=1e-1
        if end_iter_num==star_iter_num and pad_number>300:
            # toler_thresh=1e-3
            pad_number=1
            de_thresh -= 1e-2
            if de_thresh<=1.5:
                de_thresh += 1e-2
                de_thresh -= 1e-3
                # toler_thresh+=1e-2
                # de_thresh=2.5
        else:
            pad_number+=1
    wrong_log_file.close()
    record_log_file.close()
def point_in_rect(point,left_bot,right_top):
    if point[0]<left_bot[0]:
        return False
    if point[1]<left_bot[1]:
        return False
    if point[0]>right_top[0]:
        return False
    if point[1]>right_top[1]:
        return False
    return True
def get_devieces_do_index(pad_info_l_in,part_inf_l_in):
    part_index_do = [i for i in range(len(part_inf_l_in))]
    part_index_do = sorted(part_index_do,
                           key=lambda x: (0.9*max(abs(part_inf_l_in[x].centerx), abs(part_inf_l_in[x].centery))+
                                          0.1*(abs(part_inf_l_in[x].centerx) + abs(part_inf_l_in[x].centery))
                                              ),
                           reverse=True)
    devices_index_sta={}
    for index,i in enumerate(part_index_do):
        devices_index_sta[part_inf_l_in[i].part_name]=index
    return devices_index_sta
def core(x):
    if x>=0:
        return str(int(x*10)/10.0)
    else:
        return str(-1*int(x * 10) / 10.0)
# def core(x):
#     if x>=0:
#         return str(round(x,1))
#     else:
#         return str(-1*round(x,1))
def second_search(pad_info_l_in,part_inf_l_in,max_edge=50):
    strict_factor=3
    device=find_device_with_label(pad_info_l_in,part_inf_l_in)
    print 'find device with label complete.'
    for index, part_info in enumerate(part_inf_l_in):
        part_info.get_around_thing(index, part_inf_l_in, pad_info_l_in,radius=max_edge)
    print 'around thing get complete.'

    part_index_do = [i for i in range(len(part_inf_l_in))]
    part_index_do=sorted(part_index_do,key=lambda x: (0.9*max(abs(part_inf_l_in[x].centerx), abs(part_inf_l_in[x].centery))
                                                      +0.1*(abs(part_inf_l_in[x].centerx) + abs(part_inf_l_in[x].centery))),
                         reverse=True)
    print part_index_do
    pad_index_do = [i for i in range(len(pad_info_l_in))]
    part_complete={}
    pad_complete={}
    for order_index,this_index in enumerate(part_index_do):
        if this_index in part_complete:
            continue
        part_centerx = part_inf_l_in[this_index].centerx
        part_centery = part_inf_l_in[this_index].centery
        part_name    = part_inf_l_in[this_index].part_name
        posi_pad_x={}
        negi_pad_x={}
        abs_pad_x={}
        posi_pad_y={}
        negi_pad_y={}
        abs_pad_y={}
        candi_width=0
        candi_width_list=[0.001]
        candi_height=0
        candi_height_list=[0.001]
        for near_index_dist in part_inf_l_in[this_index].aroundPad:
            if near_index_dist[0] in pad_complete:
                # print 'in'
                continue
            this_pad_index=near_index_dist[0]
            delta_x=pad_info_l_in[this_pad_index].centerx-part_centerx
            delta_y=pad_info_l_in[this_pad_index].centery-part_centery


            if delta_x < 0:
                delta_x_str = core(delta_x)
                negi_pad_x[delta_x_str] = True

                negi_pad_x[core(delta_x-1e-2)] = True
                negi_pad_x[core(delta_x + 1e-2)] = True

                if delta_x_str in posi_pad_x:
                    if delta_x_str not in abs_pad_x:
                        candi_width = -1 * delta_x
                        candi_width_list.append(-1 * delta_x+0.1)
                        abs_pad_x[delta_x_str]=True
            else:
                delta_x_str = core(delta_x)
                posi_pad_x[delta_x_str] = True

                posi_pad_x[core(delta_x-1e-2)] = True
                posi_pad_x[core(delta_x + 1e-2)] = True

                if delta_x_str in negi_pad_x:
                    if delta_x_str not in abs_pad_x:
                        candi_width = delta_x
                        candi_width_list.append(delta_x+0.1)
                        abs_pad_x[delta_x_str] = True

            if delta_y < 0:
                delta_y_str = core(delta_y)
                negi_pad_y[delta_y_str] = True

                negi_pad_y[core(delta_y-1e-2)] = True
                negi_pad_y[core(delta_y + 1e-2)] = True

                if delta_y_str in posi_pad_y:
                    if delta_y_str not in abs_pad_y:
                        candi_height = -1 * delta_y
                        candi_height_list.append(-1 * delta_y+0.1)
                        abs_pad_y[delta_y_str] = True
            else:
                delta_y_str = core(delta_y)
                posi_pad_y[delta_y_str] = True

                posi_pad_y[core(delta_y-1e-2)] = True
                posi_pad_y[core(delta_y + 1e-2)] = True

                if delta_y_str in negi_pad_y:
                    if delta_y_str not in abs_pad_y:
                        candi_height = delta_y
                        candi_height_list.append(delta_y+0.1)
                        abs_pad_y[delta_y_str] = True


        # print posi_pad_x
        # print negi_pad_x
        # print candi_height,candi_width
        perfect_width=0.01
        perfect_height=0.01
        max_delta=0
        perfect_candi_index=[]
        succeed=False
        candi_width_list=sorted(candi_width_list,reverse=True)
        candi_height_list=sorted(candi_height_list,reverse=True)
        # candi_width_list.reverse()
        # candi_height_list.reverse()
        print '                               ',candi_width_list
        print '                               ',candi_height_list
        for candi_width in candi_width_list:
            for candi_height in candi_height_list:
                # candi_width+=0.01
                # candi_height+=0.01
                # print candi_width,candi_height,
                points_candi=[]
                points_candi_index=[]
                for near_index_dist in part_inf_l_in[this_index].aroundPad:
                    this_pad_index = near_index_dist[0]
                    if this_pad_index in pad_complete:
                        continue
                    delta_x = pad_info_l_in[this_pad_index].centerx - part_centerx
                    delta_y = pad_info_l_in[this_pad_index].centery - part_centery
                    # print delta_x,delta_y
                    if abs(delta_x)<=candi_width and abs(delta_y)<=candi_height:
                        points_candi.append([pad_info_l_in[this_pad_index].centerx,pad_info_l_in[this_pad_index].centery])
                        points_candi_index.append(this_pad_index)
                if len(points_candi)!=0:
                    x,y,w,h=my_bounding_rect(points_candi)
                    device_centerx=x+w/2.0
                    device_centery=y+h/2.0
                    temp_dist=get_dist(device_centerx,device_centery,part_centerx,part_centery)
                    # print 'qwe',temp_dist,

                    points_nda = np.array(points_candi, dtype=np.float32)
                    box2d = cv2.minAreaRect(points_nda)
                    # print box2d,points_nda
                    temp_dist_min_rect = get_dist(box2d[0][0], box2d[0][1], part_centerx,
                                         part_centery)

                    no_part_in=True
                    if temp_dist<1e-3 or temp_dist_min_rect<1e-3:
                        for around_part_index in part_inf_l_in[this_index].aroundPart:
                            if around_part_index in part_complete:
                                continue
                            around_part_point=[part_inf_l_in[around_part_index].centerx,part_inf_l_in[around_part_index].centery]
                            if point_in_rect(around_part_point,[x,y],[x+w,y+h]):
                                no_part_in=False
                                break
                        if no_part_in:
                            succeed=True
                            temp_min_delta=min(candi_width,candi_height)
                            if temp_min_delta>max_delta:
                                max_delta=temp_min_delta
                                perfect_width = candi_width
                                perfect_height = candi_height
                                perfect_candi_index=points_candi_index
                    else:
                        pass
                else:
                    pass
            if succeed and candi_width<max_delta:
                break
        if succeed:
            print order_index, this_index, 'succeed!', len(perfect_candi_index), '/', len(
                device[part_inf_l_in[this_index].part_name]) - 1,part_inf_l_in[this_index].package_name,\
                part_inf_l_in[this_index].angel,perfect_width,perfect_height
            for p_index in perfect_candi_index:
                pad_complete[p_index] = True
                part_complete[this_index]=True
                pad_info_l_in[p_index].do=this_index
                pad_info_l_in[p_index].result=part_name
        else:
            print order_index, this_index,'lost',0,'/', len(
                device[part_inf_l_in[this_index].part_name]) - 1,part_inf_l_in[this_index].package_name, \
                part_inf_l_in[this_index].angel
        pass

def third_search(pad_info_l_in,part_inf_l_in,max_edge=50):
    strict_factor=3
    device=find_device_with_label(pad_info_l_in,part_inf_l_in)
    print 'find device with label complete.'
    for index, part_info in enumerate(part_inf_l_in):
        part_info.get_around_thing(index, part_inf_l_in, pad_info_l_in,radius=max_edge)
    print 'around thing get complete.'

    part_index_do = [i for i in range(len(part_inf_l_in))]
    part_index_do=sorted(part_index_do,key=lambda x: (0.9*max(abs(part_inf_l_in[x].centerx), abs(part_inf_l_in[x].centery))
                                                      +0.1*(abs(part_inf_l_in[x].centerx) + abs(part_inf_l_in[x].centery))),
                         reverse=True)
    print part_index_do
    pad_index_do = [i for i in range(len(pad_info_l_in))]
    part_complete={}
    pad_complete={}
    for order_index,this_index in enumerate(part_index_do):
        if this_index in part_complete:
            continue
        part_centerx = part_inf_l_in[this_index].centerx
        part_centery = part_inf_l_in[this_index].centery

        abs_pad_x={}
        abs_pad_y={}
        candi_width=0
        candi_width_list=[0.01]
        candi_height=0
        candi_height_list=[0.01]
        for near_index_dist in part_inf_l_in[this_index].aroundPad:
            if near_index_dist[0] in pad_complete:
                # print 'in'
                continue
            this_pad_index=near_index_dist[0]
            delta_x=pad_info_l_in[this_pad_index].centerx-part_centerx
            delta_y=pad_info_l_in[this_pad_index].centery-part_centery



            if delta_x < 0:
                delta_x_str = core(delta_x)
                if delta_x_str not in abs_pad_x:
                    abs_pad_x[delta_x_str]=True
                    candi_width_list.append(-1 * delta_x+0.01)
                else:
                    pass
            else:
                delta_x_str = core(delta_x)
                if delta_x_str not in abs_pad_x:
                    abs_pad_x[delta_x_str]=True
                    candi_width_list.append(delta_x+0.01)
                else:
                    pass

            if delta_y < 0:
                delta_y_str = core(delta_y)
                if delta_y_str not in abs_pad_y:
                    abs_pad_y[delta_y_str]=True
                    candi_height_list.append(-1 * delta_y+0.01)
                else:
                    pass
            else:
                delta_y_str = core(delta_y)
                if delta_y_str not in abs_pad_y:
                    abs_pad_y[delta_y_str]=True
                    candi_height_list.append(delta_y+0.01)
                else:
                    pass




        # print posi_pad_x
        # print negi_pad_x
        # print candi_height,candi_width
        perfect_width=0.01
        perfect_height=0.01
        perfect_candi_index=[]
        succeed=False
        candi_height_list.reverse()
        candi_width_list.reverse()
        for candi_width in candi_width_list:
            for candi_height in candi_height_list:
                # candi_width+=0.01
                # candi_height+=0.01
                # print candi_width,candi_height,
                points_candi=[]
                points_candi_index=[]
                for near_index_dist in part_inf_l_in[this_index].aroundPad:
                    this_pad_index = near_index_dist[0]
                    if this_pad_index in pad_complete:
                        continue
                    delta_x = pad_info_l_in[this_pad_index].centerx - part_centerx
                    delta_y = pad_info_l_in[this_pad_index].centery - part_centery
                    if abs(delta_x)<=candi_width and abs(delta_y)<=candi_height:
                        points_candi.append([pad_info_l_in[this_pad_index].centerx,pad_info_l_in[this_pad_index].centery])
                        points_candi_index.append(this_pad_index)
                if len(points_candi)!=0:
                    x,y,w,h=my_bounding_rect(points_candi)
                    device_centerx=x+w/2.0
                    device_centery=y+h/2.0
                    temp_dist=get_dist(device_centerx,device_centery,part_centerx,part_centery)
                    if temp_dist<1e-3:
                        succeed=True
                        perfect_width=candi_width
                        perfect_height=candi_height
                        perfect_candi_index=points_candi_index
                        break
                        # print order_index,this_index,'succeed!',len(points_candi_index),'/',len(device[part_inf_l_in[this_index].part_name]) - 1
                        # for p_index in points_candi_index:
                        #     pad_complete[p_index]=True
                    else:
                        pass
                        # print order_index,this_index,'lost',temp_dist
                else:
                    pass
                    # print order_index,this_index,'None'
        if succeed:
            print order_index, this_index, 'succeed!', len(perfect_candi_index), '/', len(
                device[part_inf_l_in[this_index].part_name]) - 1,part_inf_l_in[this_index].package_name
            for p_index in perfect_candi_index:
                pad_complete[p_index] = True
        else:
            print order_index, this_index,'lost',0,'/', len(
                device[part_inf_l_in[this_index].part_name]) - 1,part_inf_l_in[this_index].package_name
        pass
    # record_log_file = open('record.txt', 'w')
    # wrong_log_file = open('wrong.txt', 'w')
    # print_index = 0
    # for s in range(1):
    #     print_index += 1
    #     print_index %= 100000
    #     if print_index % 1000 == 0:
    #         print 'part_num:', len(part_index_do), 'pad_do_num:', len(pad_index_do)
    #     if len(part_index_do) == 1 or len(pad_index_do) == 0:
    #         break
    #     for e_index,part_index in enumerate(part_index_do):
    #         part_centerx = part_inf_l_in[part_index].centerx
    #         part_centery = part_inf_l_in[part_index].centery
    #         for ele in part_inf_l_in[part_index].aroundPart:
    #             if ele in part_complete:
    #                 part_inf_l_in[part_index].aroundPart.remove(ele)
    #         for ele in part_inf_l_in[part_index].aroundPad:
    #             if ele[0] in pad_complete:
    #                 part_inf_l_in[part_index].aroundPad.remove(ele)
    #         temp_points_list=[]
    #         candi_points_list=[]

    #     star_iter_num = len(pad_index_do)
    #     for index in part_index_do:
    #         temp_candi_list = []
    #         for i in range(pad_number, len(part_inf_l_in[index].candi_elements)):
    #             points_list = []
    #             for j in range(i):
    #                 # print len(part_inf_l_in[index].candi_elements),j
    #                 points_list.append([pad_info_l_in[(part_inf_l_in[index].candi_elements[j][0])].centerx,
    #                                     pad_info_l_in[(part_inf_l_in[index].candi_elements[j][0])].centery])
    #             points_nda = np.array(points_list, dtype=np.float32)
    #             box2d = cv2.minAreaRect(points_nda)
    #             # print box2d,points_nda
    #             temp_dist = get_dist(box2d[0][0], box2d[0][1], part_inf_l_in[index].centerx,
    #                                  part_inf_l_in[index].centery)
    #             if i == pad_number:
    #                 this_num_dev_dist = temp_dist
    #                 # print this_num_dev_dist
    #                 if this_num_dev_dist > toler_thresh:
    #                     find_succeed = False
    #                     break
    #             else:
    #                 if temp_dist <= de_thresh:
    #                     find_succeed = False
    #                     break
    #                 if i == len(part_inf_l_in[index].candi_elements) - 1:
    #                     if this_num_dev_dist <= toler_thresh:
    #                         find_succeed = True
    #         if find_succeed:
    #             content = str(index) + ' '
    #             for j in range(pad_number):
    #                 pad_info_l_in[part_inf_l_in[index].candi_elements[j][0]].answer = index
    #                 pad_index_do.remove(part_inf_l_in[index].candi_elements[j][0])
    #                 if part_inf_l_in[index].part_name != pad_info_l_in[part_inf_l_in[index].candi_elements[j][0]].label:
    #                     print 'lost'
    #                 else:
    #                     content += str(part_inf_l_in[index].candi_elements[j][0]) + ' '
    #             content += '\n'
    #             record_log_file.writelines(content)
    #             if len(device[part_inf_l_in[index].part_name]) - 1 == pad_number:
    #                 pass
    #                 # print 'succeed!','num succeed!'
    #             else:
    #                 print 'succeed!', 'num lost!', pad_number, '/', len(device[part_inf_l_in[index].part_name])
    #                 wrong_log_file.writelines(str(index) + ' ' + str(pad_number) + ' ' +
    #                                           str(len(device[part_inf_l_in[index].part_name]) - 1) + ' ' +
    #                                           str(de_thresh) +
    #                                           '\n')
    #             part_index_do.remove(index)
    #             done = True
    #             break
    #         else:
    #             pass
    #     end_iter_num = len(pad_index_do)
    #     if end_iter_num == star_iter_num:
    #         done = False
    #     if end_iter_num == star_iter_num:
    #         break
    # wrong_log_file.close()
    # record_log_file.close()