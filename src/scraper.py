"""
Author: Stefano Francesco Pitton
Mail: stefanofrancesco.pitton@gmail.com
Created: 26/10/2020

Description:
------------
Source code to scrape news information from the Urania Basket's website.
"""

# Libraries
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os

# Crate empty DataFrame to store news info
columns_name = ['Title', 'Link', 'Date', 'Summary', 'Thumbnail']
news_df = pd.DataFrame(columns=columns_name)

# Specify the URL with page number as a variable
url = 'http://www.uraniabasket.it/news?page={number}'

number = 1  # initial page number

loop = True  # initialization for starting loop

# While loop to go through all the news pages
while loop:
    # Send a get request to the website and get the text from the response
    response = requests.get(url.format(number=number)).text

    # Parse HTML document
    soup = BeautifulSoup(response, "html.parser")

    # Search for all the first tag <ul> with attribute 'news'
    all_news_filter = {'class': 'news'}
    all_news = soup.find('ul', all_news_filter)

    # Search for all the news to get the total number of the current page
    news = all_news.find_all('li')
    news_number = len(news)  # number of news in current page

    # Loop over all the news inside the current page:
    for n in range(news_number):
        curr_news = news[n]

        # Get information from tag <div> with attribute 'col-sm-8 col-md-8 news-inner'
        info_filter = {"class": "col-sm-8 col-md-8 news-inner"}
        info_news = curr_news.find('div', info_filter)

        # Grab title
        title = info_news.find('h3').a.text

        # Grab link
        link = info_news.find('h3').a['href']

        # Find all paragraphs
        paragraph = info_news.find_all('p')

        # Grab date. We use regex to clean for irrelevant text
        date_ = paragraph[0].text
        date = re.findall('\d{4}-\d{1,2}-\d{1,2}', date_)[0]

        # Grab summary
        summary = paragraph[1].text

        # Grab thumbnail if any
        try:
            url_thumbnail = curr_news.a.img['src']
        except:
            url_thumbnail = ''
            'Thumbnail not present'

        # Update DataFrame with current news
        news_df = news_df.append(pd.DataFrame([[title, link, date, summary, url_thumbnail]],
                                              columns=columns_name), ignore_index=True)
    # Check if current page is last page
    if number > 1:
        if news_number != old_news_number:
            loop = False

    number += 1  # new page
    old_news_number = news_number

# Save the result as CSV
path = os.getcwd()
news_df.to_csv(os.path.join(path, r'../NEWS.csv'))

print('SCRAPING TERMINATED')
