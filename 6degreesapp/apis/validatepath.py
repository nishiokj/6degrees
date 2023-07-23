from flask import Flask, jsonify, request 
app = Flask(__name__)

@app.route('/api/movies',methods=['GET'])
def validate():
    data = request.get_json()
    entityPath = data['path']
    puzzleid = data['puzzleid']
    score = scorePath(entityPath,puzzleid)
    if score == -1:
        valid = False
    else:
        valid = True
    
    return jsonify({"isValid": valid, "score": score},200)

def scorePath(entityPath,puzzleid):
    #fetch the optimalpath of the puzzle as well as the difficulty
    distanceFactor = len(entityPath)-len(optimalPath)
    pointA = entityPath.pop(0)
    pointB = entityPath.pop(0)
    score = 0
    notabilityFactor = 0
    baseScore = 1000
    while(entityPath):
        if not validConnection(pointA,pointB):
            return -1
        pointA = pointB
        pointB = entityPath.pop(0)
    score = notabilityFactor + baseScore - (distanceFactor * 200)
    return score

def validConnection(pointA,pointB):
    