import cv2
import random
import numpy as np
from matplotlib import pyplot as plt
points_num=11
bot=-10.0
top=10.0
points_list=[]
x_list=[]
y_list=[]
sigma=0.25
for i in range(points_num):
    for j in range(points_num):
        x=bot+(top-bot)*1.0/(points_num-1)*(i)+np.random.normal(0,sigma)
        y = bot + (top - bot)*1.0 / (points_num-1) * (j)+np.random.normal(0,sigma)
        points_list.append([x,y])
# points_list=sorted(points_list,key=lambda x:(max(abs(x[0]),abs(x[1])),
#                                              max(abs(abs(x[0]+abs(x[1]))),abs(abs(x[0]-abs(x[1]))))),reverse=True)
points_list=sorted(points_list,key=lambda x:(0.9*max(abs(x[0]),abs(x[1]))+0.1*max(abs(abs(x[0]+abs(x[1]))),abs(abs(x[0]-abs(x[1])))),
                                             0.1 * max(abs(x[0]), abs(x[1]))+0.9*max(abs(abs(x[0]+abs(x[1]))),abs(abs(x[0]-abs(x[1]))))),reverse=True)
print points_list
print np.random.normal(0,5.55)
fig = plt.figure()
plt.title('sigma-0.001-denoise')
for index,point in enumerate(points_list):
    a,b=point
    plt.scatter(a,b,color=(1,0.5,1),alpha=0.5)
    plt.text(a,b, str(index), color=(0.1,0.5,0.5), fontsize=10)
# plt.scatter(box2d[0][0],box2d[0][1],color=(0.1,0.75,0.1),marker='+')
# plt.plot(boundary4points_x,boundary4points_y,color=(0.5,0.24,1))
plt.axis('equal')
plt.show()

