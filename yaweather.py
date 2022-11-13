import json

import requests as req
from geopy import geocoders
import urllib.request

condit = {
	'облачно с прояснениями': 'weather-partly-cloudy',
	'малооблачно' : 'weather-partly-cloudy',
	'ясно' : 'weather-sunny',
	'пасмурно' : 'weather-cloudy',
	'морось' : 'weather-rainly',
	'небольшой дождь' : 'weather-rainy',
	'дождь' : 'weather-pouring',
	'умеренно сильный' : 'weather-pouring',
	'сильный дождь' : 'weather-pouring',
	'длительный сильный дождь' : 'weather-pouring',
	'ливень' : 'weather-pouring',
	'дождь со снегом' : 'weather-snowy-heavy',
	'небольшой снег' : 'weather-snowy',
	'снег' : 'weather-snowy',
	'снегопад' : 'weather-snowy',
	'град' : 'weather-hail',
	'гроза' : 'weather-lightning',
	'дождь с грозой' : 'weather-lightning-rainy',
	'гроза с градом' : 'weather-lightning-rainy',
}

def city_location (city_name:str):
    cities= {'Астрахань':[46.3497, 48.0408],'Москва':[55.7522, 37.6156]}

    return cities[city_name]



def yandex_weather(latitude, longitude, token_yandex: str):
    url_yandex = f'http://api.weather.yandex.ru/v2/informers/?lat={latitude}&lon={longitude}&lang=ru_RU'

    yandex_req = req.get(url_yandex, headers={'X-Yandex-API-Key': token_yandex}, verify=False)
    conditions = {'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями',
                  'overcast': 'пасмурно', 'drizzle': 'морось', 'light-rain': 'небольшой дождь',
                  'rain': 'дождь', 'moderate-rain': 'умеренно сильный', 'heavy-rain': 'сильный дождь',
                  'continuous-heavy-rain': 'длительный сильный дождь', 'showers': 'ливень',
                  'wet-snow': 'дождь со снегом', 'light-snow': 'небольшой снег', 'snow': 'снег',
                  'snow-showers': 'снегопад', 'hail': 'град', 'thunderstorm': 'гроза',
                  'thunderstorm-with-rain': 'дождь с грозой', 'thunderstorm-with-hail': 'гроза с градом'
                  }
    conditions_icons = {'clear': 'weather-sunny', 'partly-cloudy': 'weather-partly-cloudy', 'cloudy': 'weather-partly-cloudy',
                  'overcast': 'weather-cloudy', 'drizzle': 'weather-rainly', 'light-rain': 'weather-rainly',
                  'rain': 'weather-pouring', 'moderate-rain': 'weather-pouring', 'heavy-rain': 'weather-pouring',
                  'continuous-heavy-rain': 'weather-pouring', 'showers': 'weather-pouring',
                  'wet-snow': 'weather-snowy-rainy', 'light-snow': 'weather-snowy', 'snow': 'weather-snowy',
                  'snow-showers': 'weather-snowy-heavy', 'hail': 'weather-hail', 'thunderstorm': 'weather-lightning',
                  'thunderstorm-with-rain': 'weather-lightning-rainy', 'thunderstorm-with-hail': 'weather-lightning-rainy'
                  }

    wind_dir = {'nw': 'северо-западный', 'n': 'северный', 'ne': 'северо-восточный', 'e': 'восточный',
                'se': 'юго-восточный', 's': 'южный', 'sw': 'юго-западный', 'w': 'западный', 'с': 'штиль'}

    wind_class = {'nw': 'C-З', 'n': 'С', 'ne': 'С-В', 'e': 'В',
                 'se': 'Ю-В', 's': 'Ю', 'sw': 'Ю-З', 'w': 'З', 'с': 'Ш'}

    wind_icon = {'nw': 'arrow-top-left', 'n': 'arrow-top', 'ne': 'arrow-top-rigth', 'e': 'arrow-rigth',
                'se': 'arrow-bottom-rigth', 's': 'arrow-down', 'sw': 'arrow-bottom-left', 'w': 'arrow-left', 'с': 'windsock'}



    yandex_json = json.loads(yandex_req.text)


    current_wind = yandex_json['fact']['wind_dir']

    yandex_json['fact']['wind_dir'] = wind_dir[current_wind]
    yandex_json['fact']['wind_class'] = wind_class[current_wind]
    yandex_json['fact']['wind_icon'] = wind_icon[current_wind]

    current_condition = yandex_json['fact']['condition']

    yandex_json['fact']['condition'] = conditions[current_condition]
    yandex_json['fact']['condition_icon'] = conditions_icons[current_condition]


    yandex_json['fact'].pop('icon')
    yandex_json['fact'].pop('pressure_pa')

    current_temp = yandex_json['fact']['temp']

    if current_temp > 0:
        current_temp = f'+{str(current_temp)}\u00b0'
    elif current_temp == 0:
        current_temp = '0\u00b0'
    else:
        current_temp = f'-{str(current_temp)}\u00b0'

    yandex_json['fact']['temp'] = current_temp

    current_wind_speed = yandex_json['fact']['wind_speed']
    yandex_json['fact']['wind_speed'] = f'{str(current_wind_speed)} м/с'

    current_pressure_mm = yandex_json['fact']['pressure_mm']
    yandex_json['fact']['pressure_mm'] = f'{str(current_pressure_mm)} мм.рт.с'

    current_humidity = yandex_json['fact']['humidity']
    yandex_json['fact']['humidity'] = f'{str(current_humidity)} %'





    return yandex_json

