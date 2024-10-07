import datetime
from pprint import pprint
import requests

from config import open_weather_token


def get_weather(city, open_weather_token):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        # pprint(data)

        city = data["name"]
        cur_weather = data["main"]["temp"]

        print(f"***{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}***\nПогода в городе: {city}\nТемпература: {cur_weather}°C")

    except Exception as ex:
        print(ex)
        print("Проверьте название города")


def get_for_4_days(city, open_weather_token):
    try:
        r = requests.get(
            f"https://pro.openweathermap.org/data/2.5/forecast/hourly?q={city}&appid={open_weather_token}"
        )
        data = r.json()
        pprint(data)

        # city = data["name"]
        # cur_weather = data["main"]["temp"]
        #
        # print(f"***{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}***\nПогода в городе: {city}\nТемпература: {cur_weather}°C")

    except Exception as ex:
        print(ex)
        print("Проверьте название города")


def main():
    city = input("Введите город: ")
    # get_weather(city, open_weather_token)
    get_for_4_days(city, open_weather_token)


if __name__ == "__main__":
    main()
