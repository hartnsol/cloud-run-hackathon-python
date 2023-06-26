
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

@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"

@app.route("/", methods=['POST'])
def move():
    request.get_data()
    logger.info(request.json)
    
    # TODO add your implementation here to replace the random response
    data = request.json
    
    #CONST
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
    lastMove = None

    print(myUrl, " ", dimsX, " ", dimsY, " ", FIRERANGE)
    print(myX, " ", myY, " ", myDir, " ", myScore)

    if iWasHit:
        print("I got hit!")
    else:
        print("Not hit...")
    
    def isInFront(myUrl,myX,myY,myDir,states):
        for enemy in states:
            if enemy != myUrl:
                print(enemy)
                enemyState = states[enemy]
                if myDir == "N":
                    print("N")
                    if myX == enemyState["x"]:
                        if myY > enemyState["y"] >= myY - FIRERANGE:
                            return enemy
                elif myDir == "S":
                    print("S")
                    if myX == enemyState["x"]:
                        if myY + FIRERANGE >= enemyState["y"] > myY:
                            return enemy
                elif myDir == "E":
                    print("E")
                    if myY == enemyState["y"]:
                        if myX + FIRERANGE >= enemyState["x"] > myX:
                            return enemy
                elif myDir == "W":
                    print("W")
                    if myY == enemyState["y"]:
                        if myX > enemyState["x"] >= myX - FIRERANGE:
                            return enemy
        return False
    
    
    prefEnemy = isInFront(myUrl,myX,myY,myDir,states)
    if prefEnemy != False:
        #THROW
        print(prefEnemy)
        lastMove = "T"
    elif lastMove != "F" & lastMove != "T":
        lastMove = "F"
    else:
        lastMove = turns[random.randrange(len(turns))]

    return lastMove
    
    #return turns[random.randrange(len(turns))]

if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
  
