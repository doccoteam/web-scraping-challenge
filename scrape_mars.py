#Import dependencies needed
import pandas as pd
import os
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pymongo
import requests
from urllib.parse import urlparse


def scrape():
    # NASA Mars News

    url = 'https://mars.nasa.gov/news/'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    print(soup.prettify())


    # Searching for html tag with the latest News Title
    result_title = soup.find('div', class_='content_title').find('a')
    result_title


    # Getting News Title text
    news_title = result_title.text.strip()
    news_title 


    # Searching for html tag with Paragraph Text
    result_text = soup.find('div', class_='rollover_description_inner')
    result_text


  
    # Getting Paragraph text
    news_p=result_text.text.strip()
    news_p


    print(f'The Latest News Title: "{news_title}"')
    print(f'Paragraph Text: "{news_p}"')


    # # JPL Mars Space Images - Featured Image

    # get_ipython().system('pip install selenium')

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)


    html = browser.html
    image_soup = bs(html, 'html.parser')
    image_soup


    print(image_soup.prettify())

    image_result = image_soup.find('img', class_="thumb").get('src')
    featured_image_url = 'https://www.jpl.nasa.gov' + image_result
    print(f'Image URL: {featured_image_url}')


    # browser.quit()


    # # Mars Weather

    # Getting html from target website
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(weather_url)
    weather_soup = bs(response.text, 'html.parser')
    weather_soup


    # Getting weather data
    tweets = weather_soup.find_all("p")
    for t in tweets:
        if 'InSight' in t.text:
            weather = t.text
            break

    print(f'The latest Mars weather tweet: "{weather}"')


    # # Mars Facts

    # Getting facts table from target website 
    mars_facts_url = 'https://space-facts.com/mars/'
    facts_table = pd.read_html(mars_facts_url)
    facts_table[0]


    facts_df = facts_table[0]
    facts_df.columns = ["Facts", "Value"]
    facts_df.set_index(["Facts"])
    facts_df


    # Converting df to HTML
    facts_table_to_html = facts_df.to_html(index=False)
    facts_table_to_html = facts_table_to_html.replace("\n","")
    facts_table_to_html = facts_table_to_html.replace("dataframe","table table-dark table-sm table-striped table-bordered table-responsive-lg")
    facts_table_to_html = facts_table_to_html.replace('border="1"','')
    print(facts_table_to_html.replace("dataframe","table table-dark table-sm table-striped table-bordered table-responsive-lg"))


  
    # Mars Hemispheres


    hemisphere_image_urls = []


    hemisphere_url = ('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    response = requests.get(hemisphere_url)
    hemisphere_soup = bs(response.text, 'html.parser')
    hemisphere_soup


    mars_images = hemisphere_soup.find_all('div', class_="item")
    print(mars_images)


    # Getting relatifs paths for each hemisphere's webpage and appending it to a list
    # Getting full title for each hemispere and appending it to a list
    hms_rel_urls = []
    hms_titles_full = []
    for i in mars_images:
        if i.find('div', class_='description'):
            hms_url = i.find('a')['href']
            hms_rel_urls.append(hms_url)
            hms_title_full = i.find('h3').text
            hms_titles_full.append(hms_title_full)
            
    hms_rel_urls


    # In[26]:


    hms_titles_full


    # Getting domain home url 
    o = urlparse(hemisphere_url)
    url_base = o.scheme + '://' + o.netloc
    url_base

    # Clicking each of the links to the hemispheres in order to find the image url to the full resolution image
    image_urls = []
    for u in hms_rel_urls:
        response = requests.get(url_base + u)
        hms_rel_url_soup = bs(response.text, 'html.parser')    
        for link in hms_rel_url_soup.find_all('a', string = 'Sample'):
            full_img_url = link.get('href')
            image_urls.append(full_img_url)

    image_urls

    hms_titles = []

    # Getting hemisperes titles without the last word 'enhanced'
    for ht in hms_titles_full:
        hms_title = ' '.join(ht.split(' ')[:-1])
        hms_titles.append(hms_title)
    hms_titles


    # Creating an list of dictionaries
    hemisphere_image_urls = [{'title': hmstitle, 'img_url': hmsurl} for hmstitle, hmsurl in zip(hms_titles,image_urls)]
    # return (hemisphere_image_urls)

    mars_data = {
        'latest_title': news_title,
        'latest_paragraph': news_p,
        'image_url': featured_image_url,
        'weather': weather,
        'data_table': facts_table_to_html.replace("dataframe","table table-dark table-sm table-striped table-bordered table-responsive-lg"),
        'hemispheres': hemisphere_image_urls
    }
    print(mars_data)
    return (mars_data)

if __name__=="__main__":
    data = scrape()
    print(data)
