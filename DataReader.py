def get_pad_list(pad_file_path):
    with open(pad_file_path,'r') as pad_obj:
        pad_lines=pad_obj.readlines()
        pad_lines_num=len(pad_lines)
        i=3
        all_type_list=[]
        while(True):
            if i>=pad_lines_num:
                break
            content=pad_lines[i]
            content_split=content.split()
            first_content=content_split[0]
            if first_content=='ROUND':
                all_type_list.append(['ROUND'])
                all_type_list[-1].append([float(content_split[1]),
                                                     float(content_split[2]),float(content_split[3]),
                                                     ]
                                                    )
                all_type_list[-1].append(0)
                all_type_list[-1].append(content_split[4])
            elif first_content=='RECT':
                all_type_list.append(['RECT'])
                all_type_list[-1].append([float(content_split[1]),
                                                     float(content_split[2]), float(content_split[3]),
                                                     float(content_split[4]),
                                                    ]
                                                    )
                all_type_list[-1].append(0)
                all_type_list[-1].append(content_split[5])

            elif first_content=='POLY':
                temp_goal=content_split[1]
                temp_cont=[]
                while True:
                    i += 1
                    content = pad_lines[i]
                    content_split = content.split()
                    first_content_inner = content_split[0]
                    if first_content_inner=='ENDPOLY':
                        break
                    temp_cont.append(float(content_split[0]))
                    temp_cont.append(float(content_split[1]))
                while temp_cont[0]==temp_cont[-2] and temp_cont[1]==temp_cont[-1]:
                    temp_cont.pop()
                    temp_cont.pop()
                all_type_list.append(['POLY'])
                all_type_list[-1].append(temp_cont)
                all_type_list[-1].append(0)
                all_type_list[-1].append(temp_goal)
            i+=1
    for ele in all_type_list:
        if ele[0]=='RECT':
            minx, miny, maxx, maxy=ele[1]
            x = (minx + maxx) / 2
            y = (miny + maxy) / 2
            ele.insert(2,[x,y])
        elif ele[0]=='ROUND':
            centerx, centery, diameter =ele[1]
            ele.insert(2,[centerx,centery])
        elif ele[0]=='POLY':
            data_in =ele[1]
            x = []
            y = []
            for i in range(len(data_in)):
                if i % 2 == 0:
                    x.append(data_in[i])
                else:
                    y.append(data_in[i])
            mean_x = sum(x) / len(x)
            mean_y = sum(y) / len(y)
            ele.insert(2,[mean_x,mean_y])
    return all_type_list
def get_part_list(part_file_path):
    with open(part_file_path, 'r') as part_obj:
        part_lines=part_obj.readlines()
        part_lines_num=len(part_lines)
        part_list=[]
        for i in range(1,part_lines_num):
            content=part_lines[i]
            content_split=content.split()
            PartX,PartY,Angle,PartName,PackageName=float(content_split[0]),float(content_split[1]),float(content_split[2]),content_split[3],content_split[4]
            part_list.append([PartX,PartY,Angle,PartName,PackageName,[]])
    return part_list