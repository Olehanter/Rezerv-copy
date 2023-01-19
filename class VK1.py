with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()
import time
import requests
from pprint import pprint

# token = ''
import pandas as pd
import numpy as np
import sys
import json
import requests
from setting import TOKEN


class Yandex:
    host = 'https://cloud-api.yandex.net/'

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}

    def create_folders(self, ):
        uri = 'v1/disk/resources/'
        url = self.host + uri
        headers = self.get_headers()
        params = {'path': '/test_folder'}
        response = requests.put(url, headers=headers, params=params)
        print(response.json())
        print(f'Статус: {response.status_code}')

    def upload_from_internet(self, file_name, file_url):
        uri = 'v1/disk/resources/upload/'
        url = self.host + uri
        params = {'path': f'/test_folder/{file_name}', 'url': file_url}
        response = requests.post(url, headers=self.get_headers(), params=params)
        # print(response.json())
        # print(f'Статус: {response.status_code}')
        # if response.status_code == 202:
        #     print('Загрузка успешна')


ya = Yandex(TOKEN)


class VKUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def search_groups(self, q, sorting=0):
        group_search_url = self.url + 'groups.search'
        group_search_params = {
            'q': q,
            'sort': sorting,
            'count': 300
        }
        req = requests.get(group_search_url, params={**self.params, **group_search_params}).json()
        # print(req)
        return req['response']['items']

    def search_groups_exp(self, q, sorting=0):
        group_search_ext_url = self.url + 'groups.getById'
        target_groups = self.search_groups(q, sorting)
        target_groups_ids = ",".join([str(group['id']) for group in target_groups])

        group_info_params = {
            'group_ids': target_groups_ids,
            'field': 'members_count, activity, description'
        }
        req = requests.get(group_search_ext_url, params={**self.params, **group_info_params}).json()
        # print(req)
        return req['response']

    def get_follower(self, user_id=None):
        f_url = self.url + 'users.getFollowers'
        f_params = {
            'count': 10,
            'user_id': user_id
        }
        res = requests.get(f_url, params={**self.params, **f_params}).json()
        pprint(res)
        # return res['response']

    def get_groups(self, user_id=None):
        gr_url = self.url + 'users.getFollowers'
        gr_params = {
            'count': 100,
            'user_id': user_id,
            'extended': 1,
            'fields': 'members_count'
        }
        res = requests.get(gr_url, params={**self.params, **gr_params}).json()
        # pprint(res)
        return res['response']

    def get_news(self, query):
        group_url = self.url + 'newsfeed.search'
        group_params = {
            "q": query,
            'count': 150
        }
        newsfeed_df = pd.DataFrame()
        while True:
            result = requests.get(group_url, params={**self.params, **group_params})
            time.sleep(0.33)
            newsfeed_df = pd.concat([newsfeed_df, pd.DataFrame(result.json()['response']['items'])])
            if 'next_from' in result.json()['response']:
                group_params['start_from'] = result.json()['response']['next_from']
            else:
                break
        return newsfeed_df

    def search_photos(self, user_id=None, count=8):
        url = self.url + 'photos.get'
        ph_params = {'owner_id': user_id,
                     'album_id': 'profile',
                     'rev': 0,
                     'extended': 1,
                     'count': count
                     }
        respon = requests.get(url, params={**self.params, **ph_params}).json()
        # pprint(respon)
        data_foto = []
        for el in respon['response']['items']:
            size_foto = {'s': 1, 'm': 2, 'o': 3, 'p': 4, 'q': 5, 'r': 6, 'x': 7, 'y': 8, 'z': 9, 'w': 10}
            file_url = max(el['sizes'], key=lambda x: size_foto[x['type']])

            name_like = str(el['likes']['count'])
            name_data = f'{name_like}_{el["date"]}'
            for key, val in file_url.items():
                if key == 'url':
                    file_url = val
                    break
            # print(file_url)
            ya.upload_from_internet(name_data, file_url)
            data_foto.append({'file_name': f'{name_data}.jpg', 'size': f'{el["sizes"][-1]["type"]}'})
        # pprint(data_foto)
        return data_foto


vk_client = VKUser(token, '5.131')
# pprint(vk_client.search_groups('python'))
# pprint(vk_client.search_groups_exp('python'))
# print(pd.DataFrame(vk_client.search_groups_exp('python')))
# vk_client.get_follower('1')
# pprint(vk_client.get_groups())
# vk_client.photo_log_size()
# pprint(vk_client.get_news('акация'))
pprint(vk_client.search_photos())
