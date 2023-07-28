from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
import json
import logging
import os 
import openai
app = Flask(__name__)
CORS(app)
logger = logging.getLogger(__name__)
# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.log')

c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

@app.route('/')
def home():
    openai.api_key=os.getenv("OPEN_AI_KEY")
    words = "Generate a vibrant, high resolution backdrop that is highly creative yet cohesive" 
    response = openai.Image.create(prompt=words,n=1,size="1024x1024",                               )
    return response['data'][0]['url']
@app.route('/fetchCards', methods=['GET'])
def get_Cards():
    logger.info("Inside get_Cards")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Entities')
    date_key = request.args.get('date')
    category_key = request.args.get('category')
    print(category_key)
    print(date_key)
    if date_key is None:
        return jsonify({'error': 'Missing key parameter'}), 400

    try:
        response = table.get_item(Key={'date':category_key+'-'+date_key})
        print(response['Item'])
        if 'Item' in response:
            return jsonify(response['Item'])
        else:
            return jsonify({'error': 'Entity not found'}), 404
    except Exception as e:
        return jsonify({'error': 'shit not working'}), 500



@app.route('/fetchEntity', methods=['GET'])
def get_entity():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Entities')
    entity_id = request.args.get('entityID')
    if entity_id is None:
        return jsonify({'error': 'Missing entityID parameter'}), 400

    try:
        response = table.get_item(Key={'id': entity_id})

        if 'Item' in response:
            return jsonify(response['Item'])
        else:

            return jsonify({'error': 'Entity not found'}), 404
    except Exception as e:
        logger.error("An error occurred:", exc_info=True)
        return jsonify({'error': str(e)}), 500
    
@app.route('/get_image_url/<id>', methods=['GET'])
def get_image_url(id):
    # Setup S3 client
    s3 = boto3.client('s3')

    # Get id-url map from S3
    id_url_map_obj = s3.get_object(Bucket='entity-list-6degrees', Key='actor_id_url_map.json')
    id_url_map = json.loads(id_url_map_obj['Body'].read().decode('utf-8'))

    # Look up the URL for the given ID
    url = id_url_map.get(id)
    # If we found a URL, return it; otherwise, return an error message
    if url:
        return jsonify({'id': id, 'url': url})
    else:
        return jsonify({'error': f'No image URL found for ID {id}'}), 404
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

if __name__ == '__main__':
    app.run(debug=True)