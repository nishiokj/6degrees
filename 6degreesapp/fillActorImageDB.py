import json
import boto3
import requests
s3 = boto3.client('s3')
def create_obj(bucket_name,obj_name):
    s3n = boto3.resource('s3')
    s3n.Object('entity-list-6degrees',obj_name).put(Body='')
def get_actor_image_urls(api_key):
    # Setup S3 client
    # Get entity list from S3
    create_obj('entity-list-6degrees','actor_id_url_map.json')
    entity_list_obj = s3.get_object(Bucket='entity-list-6degrees', Key='cinema-entities.json')
    entity_list = json.loads(entity_list_obj['Body'].read().decode('utf-8'))

    # New dictionary to store actor IDs and their image URLs
    id_url_map = {}

    for name,id in entity_list.items():
        # Fetch actor details from TMDB API
        try:
            response = requests.get(f'https://api.themoviedb.org/3/person/{id}/images?api_key={api_key}')
            data = response.json()
            if data:
                id_url_map[id] = f'https://image.tmdb.org/t/p/w185{data["profiles"][0]["file_path"]}'
        except Exception:
            print(f'Error fetching data for entity {name,id}')
            continue
        # Construct image URL and add it to the dictionary
        
    # Write the new map back to S3
    s3.put_object(Body=json.dumps(id_url_map), Bucket='entity-list-6degrees', Key='actor_id_url_map.json')

    print("Successfully written id-url map to S3")

# Call function
APIKEY = '97e7f2d04e54e178c11c12a8523d9f05'
get_actor_image_urls(APIKEY)
