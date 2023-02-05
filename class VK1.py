import time
import requests
from pprint import pprint
import json
import configparser  # импортируем библиотеку

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")  # читаем конфиг


class Yandex:
    host = 'https://cloud-api.yandex.net/'

    def __init__(self, token):
        self.token = token
        self.folder_name = 'Photo'

    def get_headers(self):
        return {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}

    def create_folders(self, folder_name):
        uri = 'v1/disk/resources/'
        url = self.host + uri
        headers = self.get_headers()
        # count_folder += 1
        self.folder_name = folder_name
        params = {'path': f'/{self.folder_name}'}
        response = requests.put(url, headers=headers, params=params)
        print(response.json())
        # print(f'Статус: {response.status_code}')
        return self.folder_name

    def upload_from_internet(self, file_name, file_url):
        uri = 'v1/disk/resources/upload/'
        url = self.host + uri
        params = {'path': f'/{self.folder_name}/{file_name}', 'url': file_url}
        response = requests.post(url, headers=self.get_headers(), params=params)
        # print(response.json())
        # print(f'Статус: {response.status_code}')
        # if response.status_code == 202:
        #     print('Загрузка успешна')


class VKUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, tokenVK, version):
        self.params = {
            'access_token': tokenVK,
            'v': version
        }

    def search_groups(self, q, sorting=0):
        group_search_url = self.url + 'groups.search'
        group_search_params = {
            'q': q,
            'sort': sorting,
            'count': 10
        }
        req = requests.get(group_search_url, params={**self.params, **group_search_params}).json()
        # print(req)
        return req['response']['items']

    def search_photos(self, user_id=None, count=6):
        # self.user_id = input('user_id = ')
        url = self.url + 'photos.get'
        ph_params = {'owner_id': user_id,
                     'album_id': 'profile',
                     'rev': 0,
                     'extended': 1,
                     'count': count
                     }
        respon = requests.get(url, params={**self.params, **ph_params}).json()
        pprint(respon)
        data_foto = []
        s = []
        for el in respon['response']['items']:
            size_foto = {'s': 1, 'm': 2, 'o': 3, 'p': 4, 'q': 5, 'r': 6, 'x': 7, 'y': 8, 'z': 9, 'w': 10}
            file_url = max(el['sizes'], key=lambda x: size_foto[x['type']])

            name_like = str(el['likes']['count'])
            s.append(str(el['likes']))
            time_string = time.strftime("%d%m_%Y_%H%M", time.localtime(el["date"]))
            name_data = f'{name_like}'
            if name_like in s:
                name_data = f'{name_like}_{time_string}'

            for key, val in file_url.items():
                if key == 'url':
                    file_url = val
                    break
            # print(file_url)
            ya.upload_from_internet(name_data, file_url)
            data_foto.append({'file_name': f'{name_data}.jpg', 'size': f'{el["sizes"][-1]["type"]}'})
        # pprint(data_foto)
        with open('data_photos.json', 'w') as write_f:
            json.dump(data_foto, write_f, indent=2)
        return data_foto


# ya = Yandex(TOKEN)
# vk_client = VKUser(tokenVK, '5.131')
# print(ya.create_folders(input('Folder name? :')))
# pprint(vk_client.search_photos())

if __name__ == '__main__':
    print(config["VK"]["tokenVK"])
    TOKEN = config["YA"]["TOKEN"]
    tokenVK = config["VK"]["tokenVK"]
    print(TOKEN)
    vk_client = VKUser(tokenVK, '5.131')
    ya = Yandex(TOKEN)
    pprint(
        'ВНИМАНИЕ \nфотографии копируются  на Ядиск в папку "Photo" \n Необходимо создать её, если изначально не было')
    while True:
        comand = input('     Введите команду \n f - создать папку, p -загрузить фото из VK или q -выход: ')
        if comand == 'f':
            print(ya.create_folders(input('Folder name? :')))

        elif comand == 'p':
            n = input('Желаете изменить id_user и кол-во фото?\n да-Введите- "y", если нет-Введите- "n": ')
            if n == 'y':
                user_id = input('user_id = ')
                count = int(input('count_foto= '))
                pprint(vk_client.search_photos(user_id, count))
            elif n == 'n':
                pprint(vk_client.search_photos())
            else:
                print('________Неверная команда')

        elif comand == 'q':
            print('Goodbye')
            break
