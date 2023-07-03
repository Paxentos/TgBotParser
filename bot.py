import requests
import telebot
from bs4 import BeautifulSoup as b

bot = telebot.TeleBot('')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Привет! Я бот-парсер, я могу найти для вас мангу(манхву). Для этого введите название манги или манхвы')

@bot.message_handler(content_types=['text'])
def parser(message):
    URL = 'https://mangalib.me/manga-list?name=' + message.text
    bot.send_message(message.chat.id,'Ищу мангу или манхву по запросу: ' + message.text)
    r =requests.get(URL)
    soup = b(r.text,'html.parser')
    manga = soup.find_all('a', class_='media-card')
    for link in manga:
        url = link['href']
        r =requests.get(url)
        soup = b(r.text,'html.parser')
    #поиск названия манги и постера
        name_manga = soup.find('div', class_='media-name__main')
        try:
            img = soup.find("div", class_="media-sidebar__cover paper")
            img1 = img.find("img")
            img1 = img1['src']
            bot.send_photo(message.chat.id,img1,f'Название: {name_manga.text}' + f'\nСсылка на сайт: {url}')
        except AttributeError:
            continue
        if manga.index(link) == 4:
            break
    bot.send_message(message.chat.id,'Вот список, который мне удалось найти')
bot.polling()
