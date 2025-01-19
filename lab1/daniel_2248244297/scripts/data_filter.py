import os
import csv
from bs4 import BeautifulSoup

# Create a directory for processed data 
output_dir = "../data/processed_data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read the web_data.html file
input_file = "../data/raw_data/web_data.html"
if not os.path.exists(input_file):
    print(f"Error: {input_file} not found.")
    exit()

with open(input_file, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Filter and extract market banner data
print("Filtering Market Banner data...")
market_data = []
market_cards = soup.find_all("a", class_="MarketCard-container")

for card in market_cards:
    symbol = card.find("span", class_="MarketCard-symbol").text.strip() if card.find("span", class_="MarketCard-symbol") else None
    stock_position = card.find("span", class_="MarketCard-stockPosition").text.strip() if card.find("span", class_="MarketCard-stockPosition") else None
    change_pct = card.find("span", class_="MarketCard-changesPct").text.strip() if card.find("span", class_="MarketCard-changesPct") else None
    if symbol and stock_position and change_pct:
        market_data.append([symbol, stock_position, change_pct])

if market_data:
    market_data_file = os.path.join(output_dir, "market_data.csv")
    with open(market_data_file, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Symbol", "Stock Position", "Change Percentage"])
        writer.writerows(market_data)
    print(f"Market data stored in {market_data_file}")
else:
    print("No market data found.")

# Filter and extract Latest News data
print("Filtering Latest News data...")
news_data = []
news_items = soup.find_all("li", class_="LatestNews-item")

for item in news_items:
    timestamp = item.find("time", class_="LatestNews-timestamp").text.strip() if item.find("time", class_="LatestNews-timestamp") else None
    title = item.find("a", class_="LatestNews-headline").text.strip() if item.find("a", class_="LatestNews-headline") else None
    link = item.find("a", class_="LatestNews-headline")["href"] if item.find("a", class_="LatestNews-headline") else None
    if timestamp and title and link:
        news_data.append([timestamp, title, link])

if news_data:
    news_data_file = os.path.join(output_dir, "news_data.csv")
    with open(news_data_file, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Timestamp", "Title", "Link"])
        writer.writerows(news_data)
    print(f"News data stored in {news_data_file}")
else:
    print("No news data found.")

print("Processing complete.")
