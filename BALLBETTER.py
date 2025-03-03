from controller import Supervisor, Camera
import websocket, ssl
import json
import sys

# Create a robot instance
supervisor = Supervisor()

robot_node = supervisor.getFromDef("MEGA_RAT")
sensorUp = supervisor.getDevice("sensorUp")
sensorDown = supervisor.getDevice("sensorDown")
sensorLeft = supervisor.getDevice("sensorLeft")
sensorRight = supervisor.getDevice("sensorRight")

robotName = "MEGA RAT"
websocketsServer = "ws://ryanstestserver.nl/" #"ws://192.168.1.190:8001/"

init_trans = robot_node.getField('translation').getSFVec3f()

#Websocket
ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
ws.connect(websocketsServer)
ws.send(json.dumps({
    "type": "connect",
    "fake": "true",
    "x": init_trans[0],
    "y": init_trans[1],
    "robot_name": robotName
    }))
    
    



sensorUp.enable(100)
sensorDown.enable(100)
sensorLeft.enable(100)
sensorRight.enable(100)

while supervisor.step(500) != -1:
    initial_translation = robot_node.getField('translation').getSFVec3f()
    objectList = []
    print(initial_translation)
    if sensorUp.getValue() == 0:
        #print("UP")
        objectList.append({"x" : initial_translation[0], "y" : initial_translation[1]+1})
        
    if sensorDown.getValue() == 0:
        #print("DOWN")
        objectList.append({"x" : initial_translation[0], "y" : initial_translation[1]-1})        
        
    if sensorLeft.getValue() == 0:
        #print("LEFT")
        objectList.append({"x" : initial_translation[0]-1, "y" : initial_translation[1]})        
    
    if sensorRight.getValue() == 0:
        #print("RIGHT")
        objectList.append({"x" : initial_translation[0]+1, "y" : initial_translation[1]})
    

    
    print(objectList)  
   
        
    ws.send(json.dumps({
        "type": "robot_position",
        "robot_name": robotName,
        "x": initial_translation[0],
        "y": initial_translation[1],
        "obstacles": objectList
        }))
    jsondata = json.loads(ws.recv())
    if jsondata['robot_name'] == robotName:
        new_translation = [jsondata["x"], jsondata["y"], initial_translation[2]]

        
        robot_node.getField('translation').setSFVec3f(new_translation) 