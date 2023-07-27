from flask import Flask, jsonify, request 
app = Flask(__name__)
import boto3
@app.route('/api/movies',methods=['POST'])
def validate():
    data = request.get_json()
    entityPath = data['path']
    puzzleid = data['puzzleid']
    score = scorePath(entityPath,puzzleid)
    return jsonify({"score": score},200)

def scorePath(entityPath,puzzleid):
    #fetch the optimalpath of the puzzle as well as the difficulty
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Puzzles')
    response = table.get_item(Key={'puzzleid': puzzleid})
    shortestPath = response['Item']['shortestPath']
    distanceFactor = len(entityPath)-shortestPath
    pointA = entityPath.pop(0)
    pointB = entityPath.pop(0)
    score = 0
    notabilityFactor = 0
    baseScore = 1000
    score = notabilityFactor + baseScore - (distanceFactor * 200)
    return score


    