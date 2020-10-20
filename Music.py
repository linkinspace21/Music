from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as soup
import time
import sqlite3

connection = sqlite3.connect('music.db')
cur = connection.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS music (Title TEXT, Artist TEXT, Views TEXT, Posted TEXT)''')

driver = webdriver.Chrome('C:/bin/chromedriver.exe')
driver.get('https://www.youtube.com')
driver.maximize_window()
search = driver.find_element_by_name('search_query')
search.send_keys('Chill Masters')
search.send_keys(Keys.RETURN)
try:
    link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Chill Masters")))
    link.click()
    uploads = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Uploads")))
    uploads.click()
    test = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "items")))
    time.sleep(5)
except:
    driver.quit()
for i in range(20):
    driver.execute_script('window.scrollBy(0, 1800)')
    time.sleep(3)
time.sleep(5)
allvids = driver.find_elements_by_id('details')
for vid in allvids:
    title = vid.find_element_by_id('video-title').text
    print(title)
    views = vid.find_element_by_xpath('.//*[@id="metadata-line"]/span[1]').text
    view = views.split()[0]
    print(views)
    days = vid.find_element_by_xpath('.//*[@id="metadata-line"]/span[2]').text
    print(days)
    title_artist = title.split('-')
    try:
        cur.execute('''INSERT INTO music (Title, Artist, Views, Posted) VALUES (?, ?, ?, ?)
        ''', (title_artist[0], title_artist[1], view, days))
    except:
        cur.execute('''INSERT INTO music (Title, Artist, Views, Posted) VALUES (?, ?, ?, ?)
        ''', (title_artist[0], None, view, days))
connection.commit()
driver.quit()
