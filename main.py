import os
from pathlib import Path
import requests
import random
from dotenv import load_dotenv


def raise_exception_vk(response):
    if 'error' in response:
        error_code = response['error']['error_code']
        error_message = response['error']['error_msg']
        error_message = f'Error [{error_code}]: {error_message}'
        raise requests.exceptions.HTTPError(error_message)


def load_image(path, filename, url, params=None):
    filepath = Path(path) / filename
    response = requests.get(url, params=params)
    response.raise_for_status()
    with filepath.open('wb') as file:
        file.write(response.content)


def fetch_comics(path, comics):
    url = f'https://xkcd.com/{comics}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    filename = f'{comics}.png'
    load_image(path, filename, response['img'])
    return response['alt']


def fetch_last_comic():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    return response['num']


def get_wall_upload_server(vk_token, group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'group_id': group_id,
        'access_token': vk_token,
        'v': '5.131',
    }
    response = requests.post(url, params=payload)
    response.raise_for_status()
    response = response.json()
    raise_exception_vk(response)
    url = response['response']['upload_url']
    return url


def upload_pic_server(path, comics, url):
    with open(f'{path}/{comics}.png', 'rb') as file:
        files = {
            'photo': file,  
        }
        response = requests.post(url, files=files)
    response.raise_for_status()
    response = response.json()
    raise_exception_vk(response)
    server = response['server']
    photo = response['photo']
    vk_hash = response['hash']
    return server, photo, vk_hash


def save_pic_wall(server, photo, vk_hash, vk_token, group_id):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'group_id': group_id,
        'server': server,
        'photo': photo,
        'hash': vk_hash,
        'access_token': vk_token,
        'v': '5.131',
    }
    response = requests.post(url, params=payload)
    response.raise_for_status()
    response = response.json()
    raise_exception_vk(response)
    owner_pic_id = response['response'][0]['owner_id']
    media_id = response['response'][0]['id']
    return owner_pic_id, media_id


def post_pic_wall(pic_message, owner_pic_id, media_id, vk_token, group_id):    
    group_id = int(group_id)
    url = 'https://api.vk.com/method/wall.post'
    payload = {
        'owner_id': -group_id,
        'from_group': 1,
        'message': pic_message,
        'attachments': f'photo{owner_pic_id}_{media_id}',
        'access_token': vk_token,
        'v': '5.131',
    }
    response = requests.post(url, params=payload)
    response.raise_for_status()
    response = response.json()
    raise_exception_vk(response)
    

def main():
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    group_id = os.getenv('GROUP_ID')
    comics = random.randint(1, fetch_last_comic())
    path = 'files'
    Path(path).mkdir(exist_ok=True)
    try:
        pic_message = fetch_comics(path, comics)
        url = get_wall_upload_server(vk_token, group_id)
        server, photo, vk_hash = upload_pic_server(path, comics, url)
        owner_pic_id, media_id = save_pic_wall(server, photo, vk_hash, vk_token, group_id)
        post_pic_wall(pic_message, owner_pic_id, media_id, vk_token, group_id)
    finally:
        file_to_rem = Path(f'{path}/{comics}.png')
        file_to_rem.unlink()
        Path(path).rmdir() 

    
if __name__ == '__main__':
    main()

