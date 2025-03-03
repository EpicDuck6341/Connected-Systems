# Protecol for the webots simulation of the robot

## 1. Introduction
This document describes the protocol for the webots simulation of the robot. The protocol is divided into two parts: the first part describes the communication between the robot and the server, the second part describes the communication between the server and the client.

## 2. Communication between the robot and the server
The communication between the robot and the server is based on a websocket connection. The robot is the client and the server is the server. The robot sends the server data about the current position of the robot and data about any obstacles that the robot has detected. The robot can also send a command to make all active robots stop. The robot will send this information in de form of a JSON object.  

### 2.1 JSON object
#### 2.1.1 Robot position
The robot position is a JSON object with the following structure:
```
{
    "type": "robot_position",
    "robot_name": <robot_id>,
    "x": <x>,
    "y": <y>,
    "obstacles": {
        {
            "x": <x>,
            "y": <y>,
        },
        ...
    }
    
    
}
```
The robot_id is the id of the robot. The x and y are the coordinates of the robot. The cordinates are in squares on the field. The x and y are relative to bottom left corner of the field. The x-axis is pointing to the right and the y-axis is pointing upwards. The robot_id is an integer. The x and y are floats. The obstacles are the obstacles that the robot has detected. This field should be empty if no objects were detected. The obstacles are also JSON objects with the x and y coordinates of the obstacle. The obstacles are also relative to the bottom left corner of the field.

#### 2.1.2 Stop command
The stop command is a JSON object with the following structure:
```
{
    "type": "stop",
    "robot_name": <robot_id>
}
```

### 2.2 Connection
If the robot wants to connect to the server it will send a JSON object with the following structure:
```
{
    "type": "connect",
    "fake" : true, 
    "robot_name": <robot_id>
}
```

## 3. Communication between the server and the client

The communication between the server and the client is based on a websocket connection. The server is the client and the client is the server. The server sends data about the target position of the robots and passes on the stop command to the robots. The server will send this information in de form of a JSON object.

### 3.1 JSON object
#### 3.1.1 Target position
The target position is a JSON object with the following structure:
```
{
    "type": "target_position",
    "robot_name": <robot_id>,
    "x": <x>,
    "y": <y>
}
```

The robot_id is the id of the robot. The x and y are the coordinates of the target position. The cordinates are in squares on the field. The x and y are relative to bottom left corner of the field. The x-axis is pointing to the right and the y-axis is pointing upwards. The robot_id is an integer. The x and y are floats.

#### 3.1.2 Stop command
The stop command is a JSON object with the following structure:
```
{
    "type": "stop";
}
```




