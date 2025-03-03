import tkinter as tk
import websocket
import ssl
import json
import threading
import queue

root = tk.Tk()
root.title("Connected Systems GUI")
root.geometry("750x900")
newPos = []
squares = []
entry_boxes = []
dots = []
obstacles = []
q = queue.Queue()

bgColor = "#121212"
color1 = "#ff5555"
color2 = "#ffee55"
color3 = "#55ffaa"
stopColor = "#ff5555"

websocketsServer = "ws://ryanstestserver.nl/"
ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
ws.connect(websocketsServer)
ws.send(json.dumps({
    "type": "connect",
    "gui": "true",
    "robot_name": "RAT?"
}))

def createSquare(xPos,yPos, robotName, color):
    square = tk.Canvas(root, width=100, height=100, bg=color)
    squares.append(square)
    square.place(x=xPos, y=30)
    square.create_text(50, 30, text=robotName, fill="black", font=("Arial", 12))
    square.create_text(50, 60, text="Position", fill="black", font=("Arial", 11))
    newPos.append(square.create_text(35, 80, text="X:", fill="black", font=("Arial", 10)))
    newPos.append(square.create_text(65, 80, text="Y:", fill="black", font=("Arial", 10)))



def sendCoordinates(x, y):
    ws.send(json.dumps({
        "type": "gui_pos",
        "x": x,
        "y": y
    }))

def updatePos():
    while True:
        jsondata = json.loads(ws.recv())
        if q.qsize() == 0:
            q.put(jsondata)

def updater():
    if q.qsize() > 0:
        jsondata = q.get()
        name = jsondata["robot_name"]
        x = jsondata["x"]
        y = jsondata["y"]
        obstacles = jsondata["obstacles"]
        for obstacle in obstacles:
            obx = int(obstacle["x"])
            oby = int(obstacle["y"])
            if obx >= 0 and oby >= 0:
                if obx < 10 and oby < 10:
                    print(obx,oby)
        if name == "MINI RAT":
            squares[0].itemconfigure(newPos[4], text="X:" + str(x))
            squares[0].itemconfigure(newPos[5], text="Y:" + str(y))
            adjustBotPosition(0, x, y)
        if name == "MEDIUM RAT":
            squares[1].itemconfigure(newPos[2], text="X:" + str(x))
            squares[1].itemconfigure(newPos[3], text="Y:" + str(y))
            adjustBotPosition(1, x, y)
        if name == "MEGA RAT":
            squares[2].itemconfigure(newPos[0], text="X:" + str(x))
            squares[2].itemconfigure(newPos[1], text="Y:" + str(y))
            adjustBotPosition(2, x, y)
        for obstacle in obstacles:
            placeObstacle(obx,oby)

    root.after(5000, updater)

def createCheckboard():
    checkboard = tk.Frame(root, width=600, height=600, bg=bgColor)
    checkboard.place(x=50, y=200)

    for row in range(10):
        for col in range(10):
            color = color1 if (row + col) % 2 == 0 else color2
            square = tk.Canvas(checkboard, width=60, height=60, bg=color)
            square.grid(row=row, column=col)

def placeBot(x, y):
    x=x*65+55
    y =787 -y*65
    square = tk.Canvas(root, width=50, height=50, bg='purple')
    square.place(x=x, y=y)
    dots.append((square, x, y))

def placeObstacle(x, y):
    x = x * 65 + 55
    y = 787 - y * 65
    square = tk.Canvas(root, width=50, height=50, bg='black')
    square.place(x=x, y=y)

def adjustBotPosition(bot_index, new_x, new_y):
    x = new_x * 65 + 55
    y = 787 - new_y * 65
    square, _, _ = dots[bot_index]
    square.place(x=x, y=y)
    dots[bot_index] = (square, x, y)

entry_x = tk.Entry(root, width=5)
entry_y = tk.Entry(root, width=5)
entry_boxes.append((entry_x, entry_y))
entry_x.place(x=170, y=140)
entry_y.place(x=220, y=140)
send_button = tk.Button(root, text="Send", width=5,command=lambda: sendCoordinates(entry_x.get(), entry_y.get()))
send_button.place(x=190, y=165)

root.configure(bg=bgColor)
createSquare(50, 30, "MiniRat", color1)
createSquare(160, 30, "MediumRat", color2)
createSquare(270, 30, "MegaRat", color3)
createCheckboard()

placeBot(0,0)
placeBot(0,0)
placeBot(0,0)

stop_button = tk.Button(root, text="Stop", bg=stopColor, fg="black", width=10, height=2,command=ws.send(json.dumps({"type": "stop"})))
stop_button.place(x=63, y=140)

update_thread = threading.Thread(target=updatePos)
update_thread.start()

root.after(1, updater)

root.mainloop()
