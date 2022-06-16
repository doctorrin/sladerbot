from selenium import webdriver

d = webdriver.Chrome()
d.get('https://www.slader.com/textbook/9780538497817-stewart-calculus-7th-edition/523/exercises/1/')
d.find_element_by_class_name('icon-sort-down').click()

all_exercises = d.find_element_by_class_name('ex-chiclet--flex')
for i in all_exercises:
    print(i.text)
