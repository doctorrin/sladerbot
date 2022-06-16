from selenium import webdriver
import requests
import telebot

bot = telebot.TeleBot('1461520280:AAGd8k7Es-V5a6XgDb-eRCNl2VKCCUdatTk')

driver = webdriver.Chrome()
driver.get('https://www.slader.com/textbook/9781285740621-stewart-calculus-8th-edition/')
chapters = driver.find_elements_by_class_name('toc-item')
#for chapter in chapters:
#    print(chapter.text)
print(chapters[13].text)
chapters[13].click()
table = chapters[13].find_element_by_class_name('toc-item-expanded')
#print(table.text)
sections = table.find_elements_by_class_name('exercise-group')
#for section in sections:
#    print(section.get_attribute('data-url'))
url2 = sections[4].get_attribute('data-url')
#sections[4].click()
driver.close()
driver2 = webdriver.Chrome()
driver2.get('https://www.slader.com'+url2)
#exercises = driver2.find_element_by_class_name('list-item exercise-in-group-item')
#print(exercises)
exercises = driver2.find_elements_by_xpath("//div[contains(@class, 'list-item exercise-in-group-item')]")
url3 = exercises[7].get_attribute('data-url')
print(url3)

driver2.close()
driver3 = webdriver.Chrome()
driver3.get('https://www.slader.com'+url3)
section = driver3.find_element_by_xpath("//section[contains(@class, 'solutions-list reloadable')]")
imgs = section.find_elements_by_xpath("//img[contains(@class, 'image-reg')]")

links = []
for img in imgs:
    link = img.get_attribute('src')
    links.append(link)
print(links)

for i in range(len(links)):
    img_data = requests.get(links[i]).content
    with open(f'solution{i}.jpg', 'wb') as f:
        f.write(img_data)
@bot.message_handler(commands=['start'])
def start_message(message):
    chatId = message.chat.id
    bot.send_message(chatId, 'Welcome!')
@bot.message_handler(content_types=['text'])
def send_message(message):
    chatId = message.chat.id
    text = message.text.lower()
    print(text)
    if text == 'sol':
        for i in range(len(links)):
            bot.send_photo(chatId, links[i])
    else:
        bot.send_message(chatId, 'cho nada')

bot.polling()