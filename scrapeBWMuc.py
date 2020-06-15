from bs4 import BeautifulSoup
import requests
from datetime import datetime
import os.path

# url to scrape
url = 'https://www.boulderwelt-muenchen-ost.de/'

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

# class tag which contains div with information
crowd_level_tag = soup.find(class_='crowd-level-pointer')

# extract crowd_level which is content of crowd_level_tag's div element
crowd_level_percent = crowd_level_tag.find('div').contents[0]
crowd_level = float(crowd_level_percent.strip('%'))/100

# Get current time
now = datetime.now()
now_string = now.strftime("%Y-%m-%d %H:%M:%S")

# create new csv file if it doesn't exist
file_path = 'crowd_level.csv'
if not os.path.exists(file_path):
    with open(file_path, 'w') as csv_file:
        csv_file.write("time;crowd_level\n")

# Append new data to end of csv file
with open(file_path,'a') as csv_file:
    csv_file.write(f"{now_string};{crowd_level}\n")
