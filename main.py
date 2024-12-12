# import zipfile # включить при использовании proxy
# import re #включить при использовании proxy

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import fake_useragent
import telebot
import csv

from settings import token, id_channel, id_channel_for_logs, link, delay


# настройка бота
bot = telebot.TeleBot(token)

# # вводим прокси
# PROXY_HOST = '185.111.24.31'
# PROXY_PORT = '8000'
# PROXY_USER = 'fdyrQf'
# PROXY_PASS = 'G7eMxA'

# подменяем user-agent
user_agent = fake_useragent.UserAgent(min_percentage=1.2).random

opts = webdriver.ChromeOptions()
opts.add_argument('user-agent=' + user_agent)

opts.add_argument('--headless') # запуск в фоновом режиме
opts.add_argument("--disable-blink-features=AutomationControlled")
opts.add_argument('--no-sandbox') # убирает ошибку запуска в headless режиме на сервере

opts.add_argument("window-size=2560×1600")

driver = webdriver.Chrome(options=opts)


while True:

    # загружаем ссылки из csv
    filename = 'links.csv'
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        existing_rows = list(reader)

    try:
        driver.implicitly_wait(5)          # ожидание появление элемента в секундах

        # проверить анонимность:
        # driver.get("https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html")
        # driver.get("https://2ip.ru/")
        # time.sleep(200)

        #  ссылка на страницу поиска
        driver.get(link) # заходим на сайт
        time.sleep(5)
        driver.save_screenshot(f'screenshots/screenshot_cian'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'.png')
        bot.send_message(id_channel_for_logs, text=f'⚡️⚡️⚡️ СТАРТ ЦИАН ⚡️⚡️⚡️\n{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')

        # ищем объявления
        ssilki = driver.find_elements(By.CLASS_NAME, value='_93444fe79c--link--VtWj6')

        for ssilka in ssilki:

            # проверяем есть ли строка в файле, если нет то записываем ссылку
            def write_to_csv(filename, data):

                if [data] not in existing_rows:
                    with open(filename, mode='a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow([data])
                    print(data, '--', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    bot.send_message(id_channel, text=data) # отправляем через бота в канал
                    time.sleep(5)

                else:
                    print('строка уже существует', '--', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


            data = ssilka.get_attribute('href')
            write_to_csv(filename, data)


    except Exception as ex:
        print(ex)
        bot.send_message(id_channel_for_logs, text=f'⚡️⚡️⚡️ Ошибка ⚡️⚡️⚡️\n{ex}')

    time.sleep(delay * 60)

