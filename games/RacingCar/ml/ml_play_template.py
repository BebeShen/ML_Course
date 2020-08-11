class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0
        self.car_pos = (0,0)
        self.coin_num = 0
        self.argent = 0
        self.other_cars_info = [] # computers cars info
        self.coins_pos = []
        # self.command = []
        self.car_lane = self.car_pos[0] // 70       # lanes 0(0~69) ~ 8(560~639)
        self.lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]  # lanes center
        print("Initial ml script")

    def update(self, scene_info: dict):
        """
        Generate the command according to the received scene information
        |lines|  0  |  1  |  2  |  3  |  4  |
              | -2  | -1  |  0  |  1  |  2  |
        |-----|-----|-----|-----|-----|-----|
              |     |     |     |     |     | 
           0  |  0  |  0  |  0  |  0  |  0  | 300~360 4
           1  |  1  |  1  |  1  |  1  |  1  | 240~300 3
           2  |  2  |  2  |  2  |  2  |  2  | 160~239 2
           3  |  3  |  3  |  3  |  3  |  3  | 80~159 1
           4  |  4  |  4  |  c  |  4  |  4  | 79~-79 0 -1
        """
        def checkcoin(matrix):
            for i in range(5):
                for j in range(5):
                    if matrix[i][j] == 999:
                        return True
            return False
        def checkforward(matrix):
            if(matrix[3][2] == 1):return 2
            for i in range(3):
                if matrix[i][2] == 1:
                    return 1
            return 0
        def count_zero(matrix):
            left = 0
            right = 0
            for i in range(5):
                if(matrix[i][0]==0):left+=1
                if(matrix[i][1]==0):left+=1
                if(matrix[i][3]==0):right+=1
                if(matrix[i][4]==0):right+=1
            return left,right
        def getrow(y):
            if(y==4):return 0
            elif(y==3):return 1
            elif(y==2):return 2
            elif(y==1):return 3
            elif(y==0 or y==-1):return 4
            else:return -1
        def bfs(matrix):
            print(bfs)
            command = []
            Mindis = 999 
            d_x = 0
            d_y = 0
            for i in range(5):
                for j in range(5):
                    if(matrix[i][j]==999):
                        dis = abs(2-j)**2 + abs(4-i)**2
                        if(dis < Mindis):
                            d_x = j
                            d_y = i
            if(d_x > 2):command.append("MOVE_RIGHT")
            elif(d_x < 2):command.append("MOVE_LEFT")
            command.append("SPEED")
            if(matrix[4][3]==1):
                if("MOVE_RIGHT" in command):
                    command.remove("MOVE_RIGHT")
            if(matrix[4][1]==1):
                if("MOVE_LEFT" in command):
                    command.remove("MOVE_LEFT")
            if(matrix[2][2]==1):
                if("SPEED" in command):
                    command.remove("SPEED")
            if(matrix[3][2]==1):
                if("SPEED" in command):
                    command.remove("SPEED")
                command.append("BRAKE")
            if(matrix[3][1]==1):
                if("MOVE_LEFT" in command):
                    command.remove("MOVE_LEFT")
            if(matrix[3][3]==1):
                if("MOVE_RIGHT" in command):
                    command.remove("MOVE_RIGHT")
            if(d_y>=2 and d_x != 2):
                if("SPEED" in command) and (self.car_pos[1]<=450):
                    command.remove("SPEED")
            print(command)
            return command
                
        def go(matrix):
            print(self.argent)
            if (self.argent==-1 or self.argent==1):
                return ["SPEED"]
            if(checkcoin(matrix= matrix)): # go to coin
                return bfs(matrix= matrix)
            else: # normal car
                if(checkforward(matrix= matrix)==2): # BRAKE & find way
                    left , right = count_zero(matrix = matrix)
                    if(left>right):
                        if(matrix[4][1]!=1) and (matrix[3][1]!=1):
                            return ["SPEED","MOVE_LEFT"]
                        else:
                            if(matrix[4][3]!=1) and (matrix[3][3]!=1):
                                return ["MOVE_RIGHT"]
                            else:return ["BRAKE"]
                    else:
                        if(matrix[4][3]!=1) and (matrix[3][3]!=1):
                            return ["MOVE_RIGHT"]
                        else:
                            if(matrix[4][1]!=1) and (matrix[3][1]!=1):
                                return ["SPEED","MOVE_LEFT"]
                            else:return ["BRAKE"]
                elif checkforward(matrix= matrix)==1: # find way
                    left , right = count_zero(matrix = matrix)
                    if(left>right):
                        if(matrix[4][1]!=1) and (matrix[3][1]!=1):
                            return ["SPEED","MOVE_LEFT"]
                        else:
                            if(matrix[4][3]!=1) and (matrix[3][3]!=1):
                                return ["SPEED","MOVE_RIGHT"]
                            else:return ["SPEED"]
                    else:
                        if(matrix[4][3]!=1) and (matrix[3][3]!=1):
                            return ["SPEED","MOVE_RIGHT"]
                        else:
                            if(matrix[4][1]!=1) and (matrix[3][1]!=1):
                                return ["SPEED","MOVE_LEFT"]
                            else:return ["SPEED"]
                else: # no car forward
                    if(self.car_pos[0] < self.car_lane*70 + 35):
                        if (matrix[4][3]!=1):
                            return ["SPEED","MOVE_RIGHT"]
                        else:return ["SPEED"]
                    if(self.car_pos[0] > self.car_lane*70 + 35):
                        if (matrix[4][1]!=1):
                            return ["SPEED","MOVE_LEFT"]
                        else:return ["SPEED"]
                    return ["SPEED"]
                    # if(self.car_pos[0] < self.car_lane*70 + 35):
                    #     if(matrix[4][3]!=1) and (matrix[3][3]!=1):
                    #         return ["SPEED","MOVE_RIGHT"]
                    #     else:
                    #         left , right = count_zero(matrix = matrix)
                    #         if(left>right):
                    #             if(matrix[4][1]!=1) and (matrix[3][1]!=1):
                    #                 return ["SPEED","MOVE_LEFT"]
                    #             else:
                    #                 if(matrix[4][3]!=1) and (matrix[3][3]!=1):
                    #                     return ["SPEED","MOVE_RIGHT"]
                    #                 else:return ["SPEED"]
                    #         else:
                    #             if(matrix[4][3]!=1) and (matrix[3][3]!=1):
                    #                 return ["SPEED","MOVE_RIGHT"]
                    #             else:
                    #                 if(matrix[4][1]!=1) and (matrix[3][1]!=1):
                    #                     return ["SPEED","MOVE_LEFT"]
                    #                 else:return ["SPEED"]
                    # if(self.car_pos[0] > self.car_lane*70 + 35):
                    #     if(matrix[4][1]!=1) and (matrix[3][1]!=1):
                    #         return ["SPEED","MOVE_LEFT"]
                    #     else:
                    #         left , right = count_zero(matrix = matrix)
                    #         if(left>right):
                    #             if(matrix[4][1]!=1) and (matrix[3][1]!=1):
                    #                 return ["SPEED","MOVE_LEFT"]
                    #             else:
                    #                 if(matrix[4][3]!=1) and (matrix[3][3]!=1):
                    #                     return ["SPEED","MOVE_RIGHT"]
                    #                 else:return ["SPEED"]
                    #         else:
                    #             if(matrix[4][3]!=1) and (matrix[3][3]!=1):
                    #                 return ["SPEED","MOVE_RIGHT"]
                    #             else:
                    #                 if(matrix[4][1]!=1) and (matrix[3][1]!=1):
                    #                     return ["SPEED","MOVE_LEFT"]
                    #                 else:return ["SPEED"]
                    # left , right = count_zero(matrix = matrix)
                    # if(left>right):
                    #     if(matrix[4][1]!=1) and (matrix[3][1]!=1):
                    #         return ["SPEED","MOVE_LEFT"]
                    #     else:
                    #         return ["SPEED"]
                    # else:
                    #     if(matrix[4][3]!=1) and (matrix[3][3]!=1):
                    #         return ["SPEED","MOVE_RIGHT"]
                    #     else:
                    #         return ["SPEED"]

        def getans():
            self.argent = 0
            matrix = [[0 for col in range(5)] for row in range(5)] # 5*5 metrix
            
            if len(self.coins_pos) != 0:
                for coin in self.coins_pos:
                    coin_line = (coin[0]) //70
                    x = coin_line - self.car_lane +2
                    y = getrow((self.car_pos[1] - coin[1])//80)
                    if(x>=0 and x<=4 and y>=0 and y<=4):
                        matrix[y][x] = 999
            if len(self.other_cars_info) != 0:
                for car in self.other_cars_info:
                    car_line = (car[0][0]) //70
                    x = car_line - self.car_lane +2
                    y = getrow((self.car_pos[1] - car[0][1])//80)
                    if(x>=0 and x<=4 and y>=0 and y<=4):
                        matrix[y][x] = 1
                        if(x==2 and y==4):
                            if(car[0][0]<self.car_pos[0]):self.argent = -1
                            if(car[0][0]>self.car_pos[0]):self.argent = 1
            if self.car_pos[0] > 525:
                for i in range(5):
                    matrix[i][4] = 1
            if self.car_pos[0] < 105:
                for i in range(5):
                    matrix[i][0] = 1                        
            if self.car_pos[0] < 35:
                for i in range(5):
                    matrix[i][0] = 1
                    matrix[i][1] = 1
            if self.car_pos[0] > 595:
                for i in range(5):
                    matrix[i][4] = 1
                    matrix[i][3] = 1
            matrix[4][2] = 9
            for i in range(5):
                for j in range(5):
                    print("{:>3}".format(int(matrix[i][j])) , end=' ')
                print()
            print()
            
            return go(matrix = matrix)

        if len(scene_info[self.player]) != 0:
            self.car_pos = scene_info[self.player]

        
        # self.car_pos = scene_info[self.player]
        self.other_cars_info = []
        for car in scene_info["cars_info"]:
            if car["id"] == self.player_no:
                self.car_vel = car["velocity"]
                self.coin_num = car["coin_num"]
            else:
                self.other_cars_info.append((car["pos"],car["velocity"]))
        if scene_info.__contains__("coins"):
            self.coins_pos = scene_info["coins"]
        self.car_lane = self.car_pos[0] // 70
        if scene_info["status"] != "ALIVE":
            return "RESET"

        return getans()

    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
        pass
