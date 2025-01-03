from datetime import datetime

import requests


def get_current_global_time():
    try:
        # Отправляем GET-запрос к API WorldTimeAPI
        response = requests.get("http://worldtimeapi.org/api/ip")
        response.raise_for_status()  # Проверяем, успешен ли запрос

        # Парсим JSON-ответ
        data = response.json()

        # Извлекаем поле "datetime"
        unixtime = data.get("unixtime")

        if not unixtime:
            print("Поле 'unixtime' не найдено в ответе.")
            return None

        return float(unixtime)

    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при запросе к API: {e}")
        return None