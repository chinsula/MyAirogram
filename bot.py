import datetime

import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import tg_bot_token, open_weather_token, proxy_url

# bot = Bot(token=tg_bot_token, proxy=proxy_url) # комментируем при запуске с локальной машины
bot = Bot(token=tg_bot_token) # комментируем при запуске с онлайн-сервера
dp = Dispatcher(bot)
list = []

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды!")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        mes_repl = (f"***{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}***\n"
                            f"Погода в населенном пункте: {city}\nТемпература: {cur_weather}C° {wd}\n"
                            f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                            f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                            )
        await message.reply(f"***{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}***\n"
                            f"Погода в населенном пункте: {city}\nТемпература: {cur_weather}C° {wd}\n"
                            f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                            f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                            )

        # Запись логов
        f = open(f"@{message.from_user.username}_log.txt", 'a', encoding='UTF-8')
        # f = open('' + str(message.chat.id) + '_log.txt', 'a', encoding='UTF-8')
        f.write(f"@{message.from_user.username}: {message.text}\n"
                f"@ChinsulaBot: {mes_repl}\n")
        f.close()

    except:
        await message.reply("Проверьте название города")


if __name__ == '__main__':
    executor.start_polling(dp)
    print(list)
