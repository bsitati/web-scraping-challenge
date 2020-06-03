# Dependencies
import os
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from pprint import pprint
import cssutils


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    scrape_mars = {}   
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
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

    scrape_mars['news_title'] = news_title
    scrape_mars['news_p'] = news_p
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

    front_url = soup.find('a').get('href')

    featured_image_url = front_url + back_url

    # featured_image_url.append(featured_image_url)

    scrape_mars['featured_image_url'] = featured_image_url
    #--------------------------
    #fact table
    url = "https://space-facts.com/mars/"
    html = requests.get(url)
    # soup = BeautifulSoup(html, 'html.parser')
    soup = BeautifulSoup(html.text, 'html.parser')

    tb = soup.find_all('table', class_='tablepress tablepress-id-p-mars')

    facts_df = pd.read_html(url)
        
    # fact_html = facts_df[0].to_html('factMars.html')
    scrape_mars['fact_html'] = facts_df[0]

    #--------------------------
    # Mars Hemispheres

    import re
    hemisphere_image_urls =[]

    image_url1 = {}
    url1 ='https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced' 
    html = requests.get(url1)
    # soup = BeautifulSoup(html, 'html.parser')
    soup = BeautifulSoup(html.text, 'html.parser')

    title1 = soup.find('h2', class_='title')
    title1 = title1.text

    img_url1 = soup.find("li").find('a')['href']

    image_url1['title']=title1
    image_url1['img_url']=img_url1

    hemisphere_image_urls.append(image_url1)
        
        #append to dictionary 
    image_url2 = {}
    url2 ='https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced' 

    html = requests.get(url2)
    # soup = BeautifulSoup(html, 'html.parser')
    soup = BeautifulSoup(html.text, 'html.parser')

    title2 = soup.find('h2', class_='title')
    title2 = title2.text

    img_url2 = soup.find("li").find('a')['href']

    image_url2['title']=title2
    image_url2['img_url']=img_url2

    hemisphere_image_urls.append(image_url2)  

        #-------------------
    image_url3 = {}
    url3 ='https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced' 

    html = requests.get(url3)
    # soup = BeautifulSoup(html, 'html.parser')
    soup = BeautifulSoup(html.text, 'html.parser')

    title3 = soup.find('h2', class_='title')
    title3 = title3.text

    img_url3 = soup.find("li").find('a')['href']

    image_url3['title']=title3
    image_url3['img_url']=img_url3

    hemisphere_image_urls.append(image_url3)

    #-------------------------------------
    image_url4 = {}
    url4 ='https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced' 

    html = requests.get(url4)
    # soup = BeautifulSoup(html, 'html.parser')
    soup = BeautifulSoup(html.text, 'html.parser')

    title4 = soup.find('h2', class_='title')
    title4 = title4.text

    img_url4 = soup.find("li").find('a')['href']

    #add to list
    image_url4['title']=title4
    image_url4['img_url']=img_url4

    hemisphere_image_urls.append(image_url4)
    #-------------------------------

    scrape_mars['hemisphere_image_urls'] = hemisphere_image_urls
    # scrape_mars.append(hemisphere_image_urls)


    
    #----------------------------------

    #return scrape_mars

    return scrape_mars_data