
Задание на курсовой проект «Резервное копирование» первого блока «Основы языка программирования Python».
Возможна такая ситуация, что мы хотим показать друзьям фотографии из социальных сетей, но соц. сети могут быть недоступны по каким-либо причинам. Давайте защитимся от такого.
Нужно написать программу для резервного копирования фотографий с профиля(аватарок) пользователя vk в облачное хранилище Яндекс.Диск.
Для названий фотографий использовать количество лайков, если количество лайков одинаково, то добавить дату загрузки.
Информацию по сохраненным фотографиям сохранить в json-файл.

Задание:
Нужно написать программу, которая будет:

Получать фотографии с профиля. Для этого нужно использовать метод photos.get.
Сохранять фотографии максимального размера(ширина/высота в пикселях) на Я.Диске.
Для имени фотографий использовать количество лайков.
Сохранять информацию по фотографиям в json-файл с результатами.
Обратите внимание: токен для ВК можно получить выполнив инструкцию.

Входные данные:
Пользователь вводит:

id пользователя vk;
токен с Полигона Яндекс.Диска. Важно: Токен публиковать в github не нужно!
Выходные данные:
json-файл с информацией по файлу:
    [{
    "file_name": "34.jpg",
    "size": "z"
    }]
Измененный Я.диск, куда добавились фотографии.​​
Обязательные требования к программе:
Использовать REST API Я.Диска и ключ, полученный с полигона.
Для загруженных фотографий нужно создать свою папку.
Сохранять указанное количество фотографий(по умолчанию 5) наибольшего размера (ширина/высота в пикселях) на Я.Диске

https://disk.yandex.ru/d/WS4dWbSdYpoUxg
https://disk.yandex.ru/d/JvCnL7ORP6mnqA
Необязательные требования к программе:

 ВНИМАНИЕ! фотографии копируются  на Ядиск в папку"Photo". Необходимо создать её, если изначально не было.

 Дошлифовка программы согласно рекомендациям
 1. строка 121-125 - чтобы пользователь мог вводить как id, так и screen_name – при любом сценарии все должно работать корректно
 2. строка 83 - даты стоит перевести в человеческий формат
 3. исправлен - в итоговой версии не должно быть несоответствий PEP8
 4. создан  файл зависимостей- requirement.txt
 5. строка 96-97 - сохранение json-файла с информацией по загруженным фото
 6. строка 5,7,8,108,109 - токены можно  читать не их py-файла , а из специальных файлов-конфигурации, подошел ini формат.