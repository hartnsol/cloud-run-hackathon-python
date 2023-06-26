
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

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)
turns = ['L', 'R']

#My CONST / Global Vars
FIRERANGE = 3
lastMove = None
prefEnemy = None

@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"

@app.route("/", methods=['POST'])
def move():
    request.get_data()
    logger.info(request.json)
    
    # TODO add your implementation here to replace the random response
    data = request.json
    
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

    print(myUrl, " ", dimsX, " ", dimsY, " ", FIRERANGE)
    print(myX, " ", myY, " ", myDir, " ", myScore)
    
    def isInFront(myUrl,myX,myY,myDir,states,range):
        for enemy in states:
            if enemy != myUrl:
                logger.info(enemy)
                enemyState = states[enemy]
                if myDir == "N":
                    logger.info("N")
                    if myX == enemyState["x"]:
                        if myY > enemyState["y"] >= myY - range:
                            return enemy
                elif myDir == "S":
                    logger.info("S")
                    if myX == enemyState["x"]:
                        if myY + range >= enemyState["y"] > myY:
                            return enemy
                elif myDir == "E":
                    logger.info("E")
                    if myY == enemyState["y"]:
                        if myX + range >= enemyState["x"] > myX:
                            return enemy
                elif myDir == "W":
                    logger.info("W")
                    if myY == enemyState["y"]:
                        if myX > enemyState["x"] >= myX - range:
                            return enemy
        return False

    if iWasHit:
        if isInFront(myUrl,myX,myY,myDir,states,1) != False:
            logger.info("Got hit, move forward")
            lastMove = "F"
        else:
            logger.info("Got hit, turn")
            lastMove = turns[random.randrange(len(turns))]
    else:
        prefEnemy = isInFront(myUrl,myX,myY,myDir,states,FIRERANGE)
        if prefEnemy != False:
            #THROW
            logger.info("preferred enemy")
            lastMove = "T"
        elif lastMove != "F" and lastMove != "T":
            #Boundary Check, don't go into boundary
            if myX == dimsX - 1 and myDir == "E":
                if myY < dimsY / 2:
                    lastMove = "R"
                else:
                    lastMove = "L"
            elif myX == 1 and myDir == "W":
                if myY < dimsY / 2:
                    lastMove = "L"
                else:
                    lastMove = "R"
            elif myY == 1 and myDir == "N":
                if myX < dimsX / 2:
                    lastMove = "R"
                else:
                    lastMove = "L"
            elif myY == dimsY - 1 and myDir == "S":
                if myX < dimsX / 2:
                    lastMove = "L"
                else:
                    lastMove = "R"
            else:
                lastMove = "F"
        else:
            lastMove = turns[random.randrange(len(turns))]

    return lastMove
    
    #return turns[random.randrange(len(turns))]

if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
  
