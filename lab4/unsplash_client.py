import requests
from apii import UNSPLASH_API

def get_random_photo_url(query=None):
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_API}",
    }

    # параметры запроса для случайного фото
    params = {
        "count": 1, # запрос на 1 фото
    }

    try:
        url = "https://api.unsplash.com/photos/random"
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status() # исключение для кодов ошибок HTTP (4xx, 5xx)

        data = response.json()
        if isinstance(data, list) and len(data) > 0: 
            photo_info = data[0] # первое фото из списка
            photo_url = photo_info.get('urls', {}).get('regular', '') # URL 
            photographer = photo_info.get('user', {}).get('name', 'Неизвестен') # фотограф
            description = photo_info.get('alt_description', 'Фотография') # описагие 
            return {"url": photo_url, "photographer": photographer, "description": description}
        elif isinstance(data, dict) and 'id' in data: # возвращается один объект, а не список
             photo_info = data
             photo_url = photo_info.get('urls', {}).get('regular', '') # URL
             photographer = photo_info.get('user', {}).get('name', 'Неизвестен') # фотограф
             description = photo_info.get('alt_description', 'Фотография') # описание
             return {"url": photo_url, "photographer": photographer, "description": description}
        else:
            print(f"Ошибка API: Ответ не содержит ожидаемую структуру данных. Ответ: {data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к Unsplash API: {e}")
        return None
    except KeyError as e:
        print(f"Ошибка: Отсутствует ожидаемое поле в ответе API: {e}")
        return None
