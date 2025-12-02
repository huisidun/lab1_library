import requests
from apii import UNSPLASH_API

def get_random_photo_url(query=None):
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_API}",
    }

    params = {
        "count": 1, # запрос на 1 фото
    }
    if query:
        params["query"] = query

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

def search_photos_by_query(query):
    if not query:
        print("Ошибка: Запрос для поиска не может быть пустым.")
        return None 

    headers = {
        "Authorization": f"Client-ID {UNSPLASH_API}",
    }

    params = {
        "query": query,
        "per_page": 1, 
        "page": 1
    }

    try:
        url = "https://api.unsplash.com/search/photos"
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        photos = data.get('results', [])

        if not photos:
            print(f"Ошибка API: Не найдено фотографий по запросу '{query}'.")
            return None # если список пуст None

        # берется ток первое фото
        photo_info = photos[0] 
        photo_url = photo_info.get('urls', {}).get('regular', '')
        photographer = photo_info.get('user', {}).get('name', 'Неизвестен')
        description = photo_info.get('alt_description', 'Фотография')

        if photo_url: # проверка есть URL у первого фото
             return {"url": photo_url, "photographer": photographer, "description": description}
        else:
             print(f"Ошибка API: Первое найденное фото не содержит URL.")
             return None


    except requests.exceptions.RequestException as e:
        print(f"Ошибка при поиске по Unsplash API: {e}")
        return None # при ошибке None
    except KeyError as e:
        print(f"Ошибка: Отсутствует ожидаемое поле в ответе API при поиске: {e}")
        return None