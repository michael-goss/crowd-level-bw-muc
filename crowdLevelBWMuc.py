from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.dates as dts
import matplotlib.pyplot as plt
import requests
import os.path

def scrapeBWCrowdLevel():
    # url to scrape
    url = 'https://www.boulderwelt-muenchen-ost.de/'

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # class tag which contains div with information
    crowd_level_tag = soup.find(class_='crowd-level-pointer')

    # extract crowd_level which is content of crowd_level_tag's div element
    crowd_level_percent = crowd_level_tag.find('div').contents[0]
    crowd_level = float(crowd_level_percent.strip('%'))/100
    return crowd_level


def saveToFile(file_path, crowd_level):
    # Get current time
    now = datetime.now()
    now_string = now.strftime("%Y-%m-%d %H:%M:%S")

    # create new csv file if it doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, 'w') as csv_file:
            csv_file.write("time;crowd_level\n")

    # Append new data to end of csv file
    with open(file_path,'a') as csv_file:
        csv_file.write(f"{now_string};{crowd_level}\n")


def plotData(file_path, plot_path):
    data = pd.read_csv(file_path, sep=";")

    # Convert date strings to datetime objects
    data['time'] = pd.to_datetime(data['time'], format="%Y-%m-%d %H:%M:%S")
    # Convert datetime objects to matplotlib format
    data['dates'] = dts.date2num(data['time'])

    fig, ax = plt.subplots()
    l, = ax.plot_date(data['dates'], data['crowd_level'], linestyle='-', marker='x', ms=3, mec=(1,0,0,0.5), mfc=(1,0,0,0.5))
    ax.grid(True)
    ax.grid(color='b', ls='-.', lw=0.25)
    ax.set_ylim([-.01,1.01])


    hours = dts.HourLocator(interval = 6)
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(dts.DateFormatter('%Y-%m-%d %H:%M'))
    plt.xticks(rotation=90)
    plt.title("Crowd Level in Munich East Boulderwelt")
    plt.xlabel("Date")
    plt.ylabel("Crowd Level")

    plt.tight_layout()
    plt.savefig(plot_path)

# -------------------- MAIN -----------------------------------------------
def main():
    file_path = 'crowd_level.csv'
    plot_path = 'crowd_level.svg'

    crowd_level = scrapeBWCrowdLevel()
    saveToFile(file_path, crowd_level)
    plotData(file_path, plot_path)


if __name__ == "__main__":
    main()
