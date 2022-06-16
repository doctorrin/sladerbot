import telebot
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time

token = '1400590046:AAGeZ3lInya-fALxKl9vXvpy3uGmuZcpA0A'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Welcome to slader.com!\nHere you can find all the solutions for your problems!')
    bot.send_message(chat_id, 'Tell me the name of the book, please.')
    bot.send_message(chat_id, 'After selecting, click on the command /chapters')


@bot.message_handler(commands=['chapters'])
def chapter(message):
    chat_id = message.chat.id
    driver2 = webdriver.Chrome()
    driver2.get(open('url.txt').read())
    chapters = driver2.find_elements_by_class_name('toc-item')
    keyboard2 = telebot.types.InlineKeyboardMarkup()

    for j in range(len(chapters)):
        keyboard2.add(telebot.types.InlineKeyboardButton(text=chapters[j].text, callback_data=f'Chapters + {j}'))
    bot.send_message(chat_id, 'Choose the necessary chapter:', reply_markup=keyboard2)
    bot.send_message(chat_id, 'After selecting, click on the command /paragraphs')
    driver2.close()

@bot.callback_query_handler(func=lambda call: call.data.startswith('Chapters'))
def chaptercall(call):
    with open('chapter.txt', 'w') as f3:
        f3.write(call.data[-2:])

@bot.message_handler(commands=['paragraphs'])
def paragraph(message):
    chat_id = message.chat.id
    driver2 = webdriver.Chrome()
    driver2.get(open('url.txt').read())
    chapters = driver2.find_elements_by_class_name('toc-item')
    chapters[int(open('chapter.txt').read())].click()
    groups = chapters[int(open('chapter.txt').read())].find_elements_by_class_name('exercise-group')
    keyboard3 = telebot.types.InlineKeyboardMarkup()

    for k in range(len(groups)):
        keyboard3.add(telebot.types.InlineKeyboardButton(text=groups[k].text, callback_data=f'Paragraphs + {k}'))
    with open('paragraph_urls.txt', 'w') as f4:
        for i in range(len(groups)):
            f4.write('https://www.slader.com' + groups[i].get_attribute('data-url') + '\n')

    bot.send_message(chat_id, 'Choose the necessary paragraph:', reply_markup=keyboard3)
    bot.send_message(chat_id, 'After selecting, click on the command /exercises')
    driver2.close()

@bot.callback_query_handler(func=lambda call: call.data.startswith('Paragraphs'))
def callparagraph(call):
    with open('paragraph_urls.txt', 'r') as f5:
        group_url = f5.readlines()[int(call.data[-2:])]
        with open('paragraph_url.txt', 'w') as f6:
            f6.write(group_url)

@bot.message_handler(commands=['exercises'])
def exercise(message):
    chat_id = message.chat.id

    driver3 = webdriver.Chrome()
    driver3.get(open('paragraph_url.txt').read()+'exercises/1/')
    (driver3.find_element_by_class_name('exercises-by-group')).click()
    exercises = driver3.find_elements_by_class_name('ex-chiclet ')

    keyboard4 = telebot.types.InlineKeyboardMarkup(row_width=10)
    for l in range(len(exercises)):
        keyboard4.add(telebot.types.InlineKeyboardButton(text=exercises[l].text, callback_data=f'Exercises + {l}'))
    with open('exs_urls.txt', 'w') as f7:
        for i in range(len(exercises)):
            f7.write(exercises[i].get_attribute('href') + '\n')
    bot.send_message(chat_id, 'Choose the necessary exercise:', reply_markup=keyboard4)
    bot.send_message(chat_id, 'After selecting, click on the command /solution')

    driver3.close()

@bot.callback_query_handler(func=lambda call: call.data.startswith('Exercises'))
def callexercise(call):
    with open('exs_urls.txt', 'r') as f8:
        ex_url = f8.readlines()[int(call.data[-2:])]
        with open('ex_url.txt', 'w') as f9:
            f9.write(ex_url)

@bot.message_handler(commands=['solution'])
def sol(message):
    chat_id = message.chat.id
    driver4 = webdriver.Chrome()
    driver4.get(open('ex_url.txt').read())
    section = driver4.find_element_by_class_name('contents ')
    imgs = section.find_elements_by_class_name('image-reg')

    links = []
    for img in imgs:
        link = img.get_attribute('src')
        links.append(link)

    for i in range(len(links)):
        img_data = requests.get(links[i]).content
        bot.send_photo(chat_id, img_data)
    bot.send_message(chat_id, 'Thanks a lot! I will wait for you again🥺')

@bot.message_handler(content_types=['text'])
def book(message):
    chat_id = message.chat.id
    users_book = message.text

    driver = webdriver.Chrome()
    driver.get('https://www.slader.com/')
    search = driver.find_element_by_name('search_query')
    search.send_keys(users_book)
    search.send_keys(Keys.RETURN)
    time.sleep(10)
    load_more = driver.find_element_by_class_name('ais-InfiniteHits-loadMore')
    load_more.click()
    time.sleep(10)

    books = driver.find_elements_by_class_name('ais-InfiniteHits-item')
    with open('urls.txt', 'w') as f:
        for book in books:
            f.write(book.find_element_by_class_name('Textbook__hit').get_attribute('href') + '\n')
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in range(len(books)):
        keyboard.add(telebot.types.InlineKeyboardButton(text=books[i].text, callback_data=f'Textbook + {i}'))

    bot.send_message(chat_id, 'Choose your book from the list below:', reply_markup=keyboard)
    driver.close()

@bot.callback_query_handler(func=lambda call: call.data.startswith('Textbook'))
def callbook(call):
    with open('urls.txt', 'r') as f1:
        url = f1.readlines()[int(call.data[-1])]
        with open('url.txt', 'w') as f2:
            f2.write(url)

bot.polling()
