# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 15:46:24 2020

@author: Dining
"""

import pickle
import os
import numpy as np
from sklearn.tree import DecisionTreeRegressor  
from sklearn.neural_network import MLPClassifier
from sklearn import tree
from sklearn import metrics
from sklearn.model_selection import train_test_split

path = os.getcwd()
path = os.path.join(path,"games","RacingCar","log")

allFile = os.listdir(path) # load log file
data_set = []

for file in allFile:
    with open(os.path.join(path,file),"rb") as f:
        data_set.append(pickle.load(f)) # load data in data_set

x = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25])  # feature of nine grid information
y = np.array([0]) # label


for data in data_set: 
    lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]
    PlayerCar_x = []  
    PlayerCar_y = []
    Activity = [] # the label which we give it
    ComputerCar_lane = [] # feature : to record the computer car x
    p_id = 0
    p_coin = -100
    Snece = data['scene_info'][-2]
    for player in (Snece['cars_info']):
        print(player)
        if player['id'] <= 5 and player['coin_nums'] > p_coin:
            p_id = player['id']
    print(p_id)
    for scene_info in data["scene_info"][1:-2:]: # start from the frame 1 
        grid = set()  
        coin_list = set()   
        ComputerCarR_line = []
        ComputerCarR_y = []
        
        for car in scene_info["cars_info"]:
            if car["id"] == p_id:
                PlayerCar_x.append(car["pos"][0])
                PlayerCar_y.append(car["pos"][1])
                p_x = car['pos'][0]
                p_y = car["pos"][1]
                p_v = car["velocity"]
                self_line = car["pos"][0]//70
                grid.add(23)
                if p_x <= 35:
                    grid.add(1)
                    grid.add(6)
                    grid.add(11)
                    grid.add(16)
                    grid.add(21)
                elif p_x >= 595:
                    grid.add(5)
                    grid.add(10)
                    grid.add(15)
                    grid.add(20)
                    grid.add(25)
        for car in scene_info["cars_info"]:
            if car["id"] == p_id:  # the player's car information          
                pass
            else:
                ComputerCarR_line.append(self_line-(car["pos"][0]//70)+2)
                ComputerCarR_y.append(car["pos"][1]-p_y)
        for coin in scene_info["coins"]:
            coin_line = (coin[0]) //70
            x = coin_line - self_line +2
            y = (p_y - coin[1])//80
            if(x>=0 and x<=4 and y>=-1 and y<=4):
                if(y==4):y = 0
                elif(y==3):y = 1
                elif(y==2):y = 2
                elif(y==1):y = 3
                elif(y==0 or y==-1):y = 4
                coin_list.add(5*y+x)
        for i in range(len(ComputerCarR_line)):          
            if ComputerCarR_line[i] == 2:      
                if ComputerCarR_y[i] >= 300 and ComputerCarR_y[i] < 360:
                    grid.add(3)
                elif ComputerCarR_y[i] < 300 and ComputerCarR_y[i] >= 240:
                    grid.add(8)
                elif ComputerCarR_y[i] < 240 and ComputerCarR_y[i] >= 160:
                    grid.add(13)
                elif ComputerCarR_y[i] < 160 and ComputerCarR_y[i] >= 80:
                    grid.add(18)
            if ComputerCarR_line[i] == 0: 
                if ComputerCarR_y[i] >= 300 and ComputerCarR_y[i] < 360:
                    grid.add(1)
                elif ComputerCarR_y[i] < 300 and ComputerCarR_y[i] >= 240:
                    grid.add(6)
                elif ComputerCarR_y[i] < 240 and ComputerCarR_y[i] >= 160:
                    grid.add(11)
                elif ComputerCarR_y[i] < 160 and ComputerCarR_y[i] >= 80:
                    grid.add(16)
                elif ComputerCarR_y[i] < 80 and ComputerCarR_y[i] >= -80:
                    grid.add(21)
            if ComputerCarR_line[i] == 1: 
                if ComputerCarR_y[i] >= 300 and ComputerCarR_y[i] < 360:
                    grid.add(2)
                elif ComputerCarR_y[i] < 300 and ComputerCarR_y[i] >= 240:
                    grid.add(7)
                elif ComputerCarR_y[i] < 240 and ComputerCarR_y[i] >= 160:
                    grid.add(12)
                elif ComputerCarR_y[i] < 160 and ComputerCarR_y[i] >= 80:
                    grid.add(17)
                elif ComputerCarR_y[i] < 80 and ComputerCarR_y[i] >= -80:
                    grid.add(22)
            if ComputerCarR_line[i] == 3: 
                if ComputerCarR_y[i] >= 300 and ComputerCarR_y[i] < 360:
                    grid.add(4)
                elif ComputerCarR_y[i] < 300 and ComputerCarR_y[i] >= 240:
                    grid.add(9)
                elif ComputerCarR_y[i] < 240 and ComputerCarR_y[i] >= 160:
                    grid.add(14)
                elif ComputerCarR_y[i] < 160 and ComputerCarR_y[i] >= 80:
                    grid.add(19)
                elif ComputerCarR_y[i] < 80 and ComputerCarR_y[i] >= -80:
                    grid.add(24)
            if ComputerCarR_line[i] == 4: 
                if ComputerCarR_y[i] >= 300 and ComputerCarR_y[i] < 360:
                    grid.add(5)
                elif ComputerCarR_y[i] < 300 and ComputerCarR_y[i] >= 240:
                    grid.add(10)
                elif ComputerCarR_y[i] < 240 and ComputerCarR_y[i] >= 160:
                    grid.add(15)
                elif ComputerCarR_y[i] < 160 and ComputerCarR_y[i] >= 80:
                    grid.add(20)
                elif ComputerCarR_y[i] < 80 and ComputerCarR_y[i] >= -80:
                    grid.add(25)
        # print(grid)
        if len(grid) == 0:
            Activity.append(0)  # return ["SPEED"]
            # 0 1 2 SPEED, + LEFT , + RIGHT
            # 4 5 6 NONE , LEFT , RIGHT
            # 7 8 9 BRAKE , + LEFT , +RIGHT 
        else:
            if len(coin_list)!=0:
                if (3 in coin_list):
                    if (8 not in grid and 13 not in grid and 18 not in grid):
                        Activity.append(0)
                    else:
                        pass
                elif(8 in coin_list):
                    if (13 not in grid and 18 not in grid):
                        Activity.append(0)
                    else:
                        pass
                elif(13 in coin_list):
                    if (18 not in grid):
                        Activity.append(0)
                    else:
                        pass
            else:
                

        grid_data = [0 for i in range(25)]
        grid_tolist = list(grid)
        coin_tolist = list(coin_list)
        for i in coin_tolist:
            grid_data[i-1] = 999
        for i in grid_tolist:
            grid_data[i-1] = 1  # change grid set into feature's data shape
        
        grid_data = np.array(grid_data).reshape(1,25)

        x = np.vstack((x.reshape(-1,25), np.hstack(grid_data)))
    y = np.hstack((y, np.array(Activity)))
    # stack the feature and label


x = x[1::] #remove [1~25]
y = y[1::] #remove [0]

x_train , x_test,y_train,y_test = train_test_split(x,y,test_size=0.2)

model = tree.DecisionTreeClassifier() 
model.fit(x_train, y_train)    

y_predict = model.predict(x_test)
print(y_predict)
accuracy = metrics.accuracy_score(y_test, y_predict)
print("Accuracy(正確率) ={:8.3f}%".format(accuracy*100))        
    
with open('games/RacingCar/ml/save/decisiontreemodel.pickle', 'wb') as f:
    pickle.dump(model, f)             
    