from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# set up ChromeDriver and Chromium
options = Options()
options.add_argument("--headless")  
service = Service('/usr/bin/chromedriver')

# WebDriver
driver = webdriver.Chrome(service=service, options=options) 

# Load
driver.get("https://www.cnbc.com/world/?region=world")
time.sleep(5)

# get page
page_source = driver.page_source

soup = BeautifulSoup(page_source, 'html.parser')

# find div
market_banner = soup.find('div', id='market-data-scroll-container', class_='MarketsBanner-marketData')
latest_news = soup.find('ul', class_='LatestNews-list')

if market_banner and latest_news:
    with open("../data/raw_data/web_data.html", "w", encoding="utf-8") as file:
        file.write(str(market_banner))
        file.write(str(latest_news))
    print("raw_data.html saved successfully!")
else:
    print("No matching element found.")

driver.quit()
