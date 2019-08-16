import tooslib
class pad_struct:
    def __init__(self,ori_index,data):
        self.shape=data[0]
        self.points_list=data[1]
        self.centerx=data[2][0]
        self.centery = data[2][1]
        self.label=data[4]
        self.nearst_index=None
        self.answer=None
        self.do=None
        self.ori_index=ori_index
        self.result=None
    def get_near_index(self,part_info_list):
        min_dist=1e5
        candi_index=0
        for index,part_info in enumerate(part_info_list):
            temp_dist=tooslib.get_dist(part_info.centerx,part_info.centery,self.centerx,self.centery)
            if temp_dist<min_dist:
                min_dist=temp_dist
                candi_index=index
        self.nearst_index=candi_index
    def get_ans_index(self,part_info_list):
        for index,part_info in enumerate(part_info_list):
            if self.label==part_info.part_name:
                self.answer=index
                break
class part_struct:
    def __init__(self,data):
        self.centerx=data[0]
        self.centery = data[1]
        self.angel=data[2]
        self.part_name=data[3]
        self.package_name=data[4]

        self.search_radius=None
        self.candi_elements=[]
        self.aroundPart=[]
        self.aroundPad=[]
    def get_around_thing(self,this_index,part_info_list,pad_info_list,radius=50):
        for index,part_info in enumerate(part_info_list):
            if index==this_index:
                continue
            temp_dist=tooslib.get_dist(self.centerx,self.centery,part_info.centerx,part_info.centery)
            if temp_dist<=radius*1.5:
                self.aroundPart.append(index)
        for index,pad_info in enumerate(pad_info_list):
            temp_dist=tooslib.get_dist(self.centerx,self.centery,pad_info.centerx,pad_info.centery)
            if temp_dist<=radius:
                self.aroundPad.append([index,temp_dist])
            # self.aroundPad=sorted(self.aroundPad,key=lambda x:x[1],reverse=False)
        # print self.aroundPad
        # print self.aroundPart
class PCB_Board:
    def __init__(self,part_info_list,pad_info_list):

        pass