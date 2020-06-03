# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests


# def init_browser():
#     # @NOTE: Replace the path with your actual path to the chromedriver
#     # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
#     executable_path = {"executable_path": "chromedriver"}
#     return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    scrape_mars = {}   
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Retrieve page with the requests module
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    # results are returned as an iterable list
    results = soup.find('div', class_="features")
    # Find titles
    
    for result in results.findAll('div', attrs={'class':'content_title'}):
#     print(div.find('a')['href'])
        news_title = result.find_all("a")[0].string
#     print(news_title)

    scrape_mars['titles'] = news_title
    #----------------------------------
    #paragraphs
    
    for result in results.find_all('div', class_='rollover_description_inner'):
        news_p = result.text
        paragraphs.append(news_p)
    
    scrape_mars['paragraphs'] = paragraphs

    #JPL Mars Space Images - Featured Image
    # URL of page to be scraped
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    # Retrieve page with the requests module
    response = requests.get(url)
    #-----------------------------------
    #
    
    import cssutils

    # browser.visit(url)
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    html = requests.get(url)
    # soup = BeautifulSoup(html, 'html.parser')
    soup = BeautifulSoup(html.text, 'html.parser')

    # results = soup.find_all('article', class_='carousel_item').find()

    #featured_image_url = results.find('span', class_='text')

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
    import pandas as pd
    url = "https://space-facts.com/mars/"
    html = requests.get(url)
    # soup = BeautifulSoup(html, 'html.parser')
    soup = BeautifulSoup(html.text, 'html.parser')

    tb = soup.find_all('table', class_='tablepress tablepress-id-p-mars')

    facts_df = pd.read_html(url)
        
    facts_df[0]

    fact_html = facts_df[0].to_html('factMars.html')
    
    scrape_mars['fact_html'] = fact_html

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

    return scrape_mars
