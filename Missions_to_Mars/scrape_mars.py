# Dependencies
import os
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from pprint import pprint
import cssutils
import re


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "c:/Users/c2c/Documents/GitHub/web-scraping-challenge/Missions_to_Mars/chromedriver.exe"}
    # executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    scrape_mars_data ={}
    url = 'https://mars.nasa.gov/news/'
    browser = init_browser()

    browser.visit(url)
    time.sleep(5)
    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')
    # results are returned as an iterable list
    results = soup.find_all('li', class_='slide')
    # Find titles
        
    news_title = results[0].find('div', class_='content_title').text
    news_p = results[0].find('div', class_='rollover_description_inner').text
    # if (news_title and news_p):
    #     print(news_title)
    #     print(news_p)

    scrape_mars_data['news_title'] = news_title
    scrape_mars_data['news_p'] = news_p
    #----------------------------------
    #JPL Mars Space Images - Featured Image 
    #
    
   
    # browser.visit(url)
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    html = requests.get(url)
    # soup = BeautifulSoup(html, 'html.parser')
    soup = BeautifulSoup(html.text, 'html.parser')

    div_style = soup.find('article')['style']
    style = cssutils.parseStyle(div_style)
    url = style['background-image']

    back_url = url.replace('url(', '').replace(')', '')    # or regex/split/find/slice etc.

    # front_url = soup.find('a').get('href')
    front_url = "https://www.jpl.nasa.gov"

    featured_image_url = front_url + back_url

    # featured_image_url.append(featured_image_url)

    scrape_mars_data['featured_image_url'] = featured_image_url
    #--------------------------
    #fact table
    url = "https://space-facts.com/mars/"
    html = requests.get(url)
    # soup = BeautifulSoup(html, 'html.parser')
    soup = BeautifulSoup(html.text, 'html.parser')

    tb = soup.find_all('table', class_='tablepress tablepress-id-p-mars')

    df = pd.read_html(url)[0]
    df.columns = ['Description', 'Value']

    # facts_df.columns =  ['Description', 'Value']
            
    fact_html = df.to_html(classes = 'table-stripped')

    scrape_mars_data['fact_html'] = fact_html

    # --------------------------
    # Mars Hemispheres

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser = init_browser()

    browser.visit(url)
    time.sleep(5)
    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    hemispheres = soup.find_all('div', class_='item')
    # Create list to be populated with list
    
    hemisphere_image_urls = []
    #iterate through hemisphere pages
    fore_link = 'https://astrogeology.usgs.gov'

    for x in hemispheres:
        #try:
        #find link to page
        href = x.find('a', class_='itemLink product-item')['href']
        title = x.find('div', class_='description').find('h3').text
        
    #     print(fore_link + href)
        browser.visit(fore_link+href)
        html = browser.html

        soup = BeautifulSoup(html, 'html.parser')
    #     print(result)
        
        image = soup.find('div', class_='downloads')
        image_link = image.find('a')["href"]
        
                        
        hemisphere_temp = {}
        hemisphere_temp["title"] = title
        hemisphere_temp["href"] =image_link
        
        
        hemisphere_image_urls.append(hemisphere_temp)

        scrape_mars_data['hemisphere_image_urls'] = hemisphere_image_urls
            #return scrape_mars

    return scrape_mars_data
