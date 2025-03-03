

import asyncio
import json
import websockets
from aStar import aStarSearch
import random
from time import sleep

gridHeight = 10
gridWidth = 10
grid = [[0 for i in range(gridHeight)] for j in range(gridWidth)]
robots = {}
clones = {}
gui = {}
targets = [[4,9], [4,9]]
stop = [0]



def calc_targets():
    counter = 0
    for clone in clones:
        target = targets[counter]
        counter +=1
        clones[clone]["target"] = target
    
        
            

async def connect(json_data, websocket):
    ''' 
    This function is called when a robot tries to first connect to the server.
    It checks or the robot is a actual robot or a clone in Webots and saves the connection.

    Parameters:
        json (dict): The json data send by the robot.
        websocket (WebSocketServerProtocol): The connection to the robot.

    Returns:
        None
    '''
    try:
        id = json_data["robot_name"]
        try:
            test = json_data["gui"]
            if test:
                gui[id] = {'connection' : websocket}
                print("gui connected to the api")
                return

        except KeyError:
            pass
        fake = json_data["fake"]
        if fake:
            x = json_data["x"]
            y = json_data["y"]
            clones[id] = {'connection' : websocket, 'pos' : [x,y], 'next' : [0,0], 'target' : [0,0]}
            calc_targets()
            print("clone "+ str(id) +  " connected to the api")
        else:
            robots[id] = {'connection' : websocket}
            print("robot "+ str(id) +  " connected to the api")
    except KeyError:
        print("invalid connect")


def calculate_path(robotName):
    
    '''
    This function calculates the next position for a robot to move to.

    Parameters:
        robotName (string): The name of the robot.

    Returns:
        list: The next position for the robot to move to in the form [x,y].
    '''
    currentPos = clones[robotName]["pos"]
    targetPos = clones[robotName]["target"]
    target = aStarSearch(grid, currentPos, targetPos)

    for clone in clones:
        if clones[clone]["next"] == target:
            target = currentPos
        if clones[clone]["pos"] == target:
            if clones[clone]["next"] == currentPos:
                calc_targets()
            target = currentPos

    return target

    
    

async def get_robot_position(websocket, data):
   
    try:
        print(data)
        Name = data["robot_name"]
        obstacles = data["obstacles"]
        x = data["x"]
        y = data["y"]
        
        for users in gui:
            await gui[users]["connection"].send(json.dumps(data))

        if websocket == clones[Name]["connection"]:
            clones[Name]["pos"] = [x,y]
            
            for obstacle in obstacles:
                obx = int(obstacle["x"])
                oby = int(obstacle["y"])
                if obx >= 0 and oby >= 0:
                    if obx < gridWidth  and oby < gridHeight:
                        print(str(obx) + "test"+ str(oby))
                        grid[int(obstacle["x"])][int(obstacle["y"])] = 1
            
            
            newPos = calculate_path(Name)
            clones[Name]["next"] = newPos

            jsonData = {
                "type": "target_position",
                "robot_name": Name,
                "x": newPos[0],
                "y": newPos[1]
            }
            
            try:
                if robots[Name]:
                    await robots[Name]["connection"].send(json.dumps(jsonData))
            except KeyError:
                pass

            await websocket.send(json.dumps(jsonData))
    except KeyError:
        
        print("invalid get_robot_position")




async def handler(websocket):
    print("new connection")
    
    
    while True:
        try:
            message = await websocket.recv()
        except websockets.exceptions.ConnectionClosedOK:
            print("connection closed")
            break
        json_data = json.loads(message)
       

        if json_data["type"] == "connect":
            await connect(json_data, websocket)

        elif json_data["type"] == "robot_position": 
            if stop[0] == 0:
                await get_robot_position(websocket, json_data)

        elif json_data["type"] == "stop":
            print("stop")
            if stop[0] == 0:
                stop[0] += 1
            else:
                stop[0] -= 1
            
            
                
        
        


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())