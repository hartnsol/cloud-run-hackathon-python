
# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
import random
from flask import Flask, request
#import math

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)
turns = ['L', 'R']

@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"

@app.route("/", methods=['POST'])
def move():
    request.get_data()
    logger.info(request.json)
    
    # TODO add your implementation here to replace the random response
    data = request.json

    # My CONST / Global Vars
    global lastMove    
    #global prefEnemy
    #global closestEnemy
    FIRERANGE = 3

    myUrl = data["_links"]["self"]["href"]
    dims = data["arena"]["dims"]
    dimsX = dims[0]
    dimsY = dims[1]
    states = data["arena"]["state"]
    myState = states[myUrl]
    myX = myState["x"]
    myY = myState["y"]
    myDir = myState["direction"]
    iWasHit = myState["wasHit"]
    myScore = myState["score"]

    #def calculateDistance(x1, y1, x2, y2):
    #    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2) 

    def isInFront(myUrl,myX,myY,myDir,states,range):
    #    closestDist = float('inf')

        for enemy in states:
            if enemy != myUrl:
                #logger.info(enemy)
                enemyState = states[enemy]
                if myDir == "N":
                    #logger.info("N")
                    if myX == enemyState["x"]:
                        if myY > enemyState["y"] >= myY - range:
                            return enemy
                elif myDir == "S":
                    #logger.info("S")
                    if myX == enemyState["x"]:
                        if myY + range >= enemyState["y"] > myY:
                            return enemy
                elif myDir == "E":
                    #logger.info("E")
                    if myY == enemyState["y"]:
                        if myX + range >= enemyState["x"] > myX:
                            return enemy
                elif myDir == "W":
                    #logger.info("W")
                    if myY == enemyState["y"]:
                        if myX > enemyState["x"] >= myX - range:
                            return enemy
                
                # distance = calculateDistance(myX, myY, enemyState["x"], enemyState["y"])
                # if distance < closestDist:
                #     closestDist = distance
                #     closestEnemy = enemy
        return ""

    def checkBound():
        thisTurn = ""
        if myX >= dimsX - 1 and myDir == "E":
            if myY < dimsY / 2:
                thisTurn = "R"
            else:
                thisTurn = "L"
        elif myX <= 1 and myDir == "W":
            if myY < dimsY / 2:
                thisTurn = "L"
            else:
                thisTurn = "R"
        elif myY <= 1 and myDir == "N":
            if myX < dimsX / 2:
                thisTurn = "R"
            else:
                thisTurn = "L"
        elif myY >= dimsY - 1 and myDir == "S":
            if myX < dimsX / 2:
                thisTurn = "L"
            else:
                thisTurn = "R"
        logger.info(thisTurn)
        return thisTurn

    # def turnToClosest():
    #     enemyState = states[closestEnemy]
    #     if myDir == "N":
    #         if enemyState["direction"] == "N" or enemyState["direction"] == "S"
    #                 return enemy
    #     elif myDir == "S":
    #         if myX == enemyState["x"]:
    #             if myY + range >= enemyState["y"] > myY:
    #                 return enemy
    #     elif myDir == "E":
    #         if myY == enemyState["y"]:
    #             if myX + range >= enemyState["x"] > myX:
    #                 return enemy
    #     elif myDir == "W":
    #         if myY == enemyState["y"]:
    #             if myX > enemyState["x"] >= myX - range:
    #                 return enemy

    #     return

    if iWasHit == True:
        if isInFront(myUrl,myX,myY,myDir,states,1) == "":
            logger.info("Got hit, move forward")
            lastMove = "F"
        else:
            logger.info("Got hit, but blocked, turn")
            if lastMove != "R" and lastMove != "L":
                for enemy in states:
                    if enemy != myUrl:
                        enemyState = states[enemy]
                        if myDir == "N" and enemyState["x"] - 1 == myX:
                            lastMove = "L"
                        elif myDir == "S" and enemyState["x"] + 1 == myX:
                            lastMove = "L"
                        elif myDir == "E" and enemyState["y"] - 1 == myY:
                            lastMove = "L"
                        elif myDir == "W" and enemyState["y"] + 1 == myY:
                            lastMove = "L"
                if lastMove != "L":
                    lastMove = "R"
            #else keep turning the same direction
    else:
        prefEnemy = isInFront(myUrl,myX,myY,myDir,states,FIRERANGE)
        if prefEnemy != "":
            #THROW
            lastMove = "T"
        elif lastMove != "F" and lastMove != "T":
            #Boundary Check, don't go into boundary
            logger.info("turned, no one in front, forward")
            lastMove = checkBound()
            if lastMove == "":
                lastMove = "F"
        else:
            logger.info("forwarded, no one in front, turn")
            lastMove = checkBound()
            if lastMove == "":
                lastMove = turns[random.randrange(len(turns))]
    
    logger.info(lastMove)
    return lastMove
    
    #return turns[random.randrange(len(turns))]

if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
  
