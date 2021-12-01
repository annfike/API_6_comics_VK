import os
from pathlib import Path
import pathlib
import requests
import random
from dotenv import load_dotenv


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


def upload_pics_VK(path, pic_message, comics, vk_token, group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer?&v=5.131'
    payload = {
        'group_id': group_id,
        'access_token': vk_token,
    }
    response = requests.post(url, params=payload)
    response.raise_for_status()
    response = response.json()
    url = response['response']['upload_url']

    with open(f'{path}/{comics}.png', 'rb') as file:
        files = {
            'photo': file,  
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
        response = response.json()
        server = response['server']
        photo = response['photo']
        hash = response['hash']

    url = 'https://api.vk.com/method/photos.saveWallPhoto?extended=0&v=5.131'
    payload = {
        'group_id': group_id,
        'server': server,
        'photo': photo,
        'hash': hash,
        'access_token': vk_token,
    }
    response = requests.post(url, params=payload)
    response.raise_for_status()
    response = response.json()
    owner_pic_id=response['response'][0]['owner_id']
    media_id=response['response'][0]['id']
    
    group_id = int(group_id)
    url = 'https://api.vk.com/method/wall.post?extended=1&v=5.131'
    payload = {
        'owner_id': -group_id,
        'from_group': 1,
        'message': pic_message,
        'attachments': f'photo{owner_pic_id}_{media_id}',
        'access_token': vk_token,
    }
    response = requests.post(url, params=payload)
    response.raise_for_status()
    response = response.json()
    file_to_rem = pathlib.Path(f'{path}/{comics}.png')
    file_to_rem.unlink()



def main():
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    group_id = os.getenv('GROUP_ID')
    comics = random.randint(1, 2548)
    path = 'files'
    pathlib.Path(path).mkdir(exist_ok=True)
    pic_message = fetch_comics(path, comics)
    upload_pics_VK(path, pic_message, comics, vk_token, group_id)
    pathlib.Path(path).rmdir() 



if __name__ == '__main__':
    main()


