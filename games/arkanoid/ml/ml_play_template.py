"""
The template of the main script of the machine learning process
"""
# based_rule 
import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)
ball_x = []
ball_y = []
def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False     #有無發球 需保留，不可刪除！！！
    
    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()     
    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()
        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False
            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()     #重新開始
            continue

        # 3.3. Put the code here to handle the scene information
        
        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            ball_served = True
        else:
            ball_x[len(ball_x):] = [scene_info.ball[0]]
            ball_y[len(ball_y):] = [scene_info.ball[1]]
            # bricks = scene_info.bricks
            platform_x = scene_info.platform[0] + 20
            platform_y = scene_info.platform[1]

            if(len(ball_x) <= 1):
                comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            elif(ball_y[-1] > ball_y[-2] and ball_y[-1] > 150): # 150~200
                mode = 0
                if(ball_x[-1]-ball_x[-2]==7):
                    mode = 0    #球的速度(7,7)
                elif(ball_x[-1]-ball_x[-2]==10):
                    mode = 1    #球的速度(10,7)
                dx = platform_y - ball_y[-1]
                # 以牆壁為反彈預判降落位置，於第4關不作用：第4關為碰撞磚塊
                if(ball_x[-1] + dx > 200 and ball_x[-1] > ball_x[-2]):
                    dx = 200 - (ball_x[-1] + dx - 200)
                    des_x = dx
                elif(ball_x[-1] - dx < 0 and ball_x[-1] < ball_x[-2]):
                    dx = 0 - (ball_x[-1] - dx)
                    des_x = dx
                else:
                    if(ball_x[-1] > ball_x[-2]):
                        des_x = ball_x[-1] + dx
                    else:
                        des_x = ball_x[-1] - dx
                if(platform_x < des_x-5 and platform_y - ball_y[-1] >= 14):
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                elif(platform_x > des_x+5 and platform_y - ball_y[-1] >= 14):
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                else:
                    if(ball_x[-1] > ball_x[-2]):    #切球
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                    elif(ball_x[-1] < ball_x[-2]):
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    else:
                        comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            else:   #球往上，板子跟著跑
                comm.send_instruction(scene_info.frame, PlatformAction.NONE)
