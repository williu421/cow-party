#############################
# Sockets Server Demo
# by Rohan Varma
# adapted by Kyle Chin
#############################

import socket
import threading
from queue import Queue

HOST = "128.237.184.128" # put your IP address here if playing on multiple computers
PORT = 50009 #kind of like the channel, change it around if things aren't working maybe 
BACKLOG = 2 #the number of people that can join 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST,PORT))
server.listen(BACKLOG)
#the above 3 lines create the socket, connect to host and port, and listens for/accepts users until backlog filled 
print("looking for connection")

def handleClient(client, serverChannel, cID, clientele):#handles client messages 
  client.setblocking(1)
  msg = ""
  while True:
    try:
      msg += client.recv(10).decode("UTF-8")
      command = msg.split("\n")
      while (len(command) > 1):
        readyMsg = command[0]
        msg = "\n".join(command[1:])
        serverChannel.put(str(cID) + " " + readyMsg)
        command = msg.split("\n")
    except:
      # we failed
      return

def serverThread(clientele, serverChannel): #delivers messages to clients 
  while True:
    msg = serverChannel.get(True, None)
    print("msg recv: ", msg)
    msgList = msg.split(" ")
    senderID = msgList[0]
    instruction = msgList[1]
    details = " ".join(msgList[2:])
    if (details != ""):
      for cID in clientele:
        if cID != senderID:
          sendMsg = instruction + " " + senderID + " " + details + "\n"
          clientele[cID].send(sendMsg.encode())
          print("> sent to %s:" % cID, sendMsg[:-1])
    print()
    serverChannel.task_done()

clientele = dict()
playerNum = 0
#creates a dict of users

serverChannel = Queue(100) #maximum of 100 messages held in server at once 
threading.Thread(target = serverThread, args = (clientele, serverChannel)).start()
#creates server thread, handles incoming messages and relays to other clients, continually runs serverThread  

names = ["Player1", "Player2"]

while True: #allows us to add new players 
  client, address = server.accept()
  # myID is the key to the client in the clientele dictionary
  myID = names[playerNum]
  print(myID, playerNum)
  for cID in clientele:
    print (repr(cID), repr(playerNum))
    clientele[cID].send(("newPlayer %s\n" % myID).encode())
    client.send(("newPlayer %s\n" % cID).encode())
  clientele[myID] = client
  client.send(("myIDis %s \n" % myID).encode())
  print("connection recieved from %s" % myID)
  threading.Thread(target = handleClient, args = 
                        (client ,serverChannel, myID, clientele)).start()
  playerNum += 1

