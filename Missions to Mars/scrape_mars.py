#!/usr/bin/env python
# coding: utf-8


# ---------------------------
# Import modules ------------
# ---------------------------
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

# ---------------------------
# Initialize browser --------
# ---------------------------
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

#def scrape():
browser = init_browser()

# ---------------------------
# Retrieve headline & summary
# ---------------------------
url = "https://mars.nasa.gov/news/"
browser.visit(url)
time.sleep(2)

news_title = []
news_p = []


html = browser.html
soup = BeautifulSoup(html, "html.parser")
results = soup.find_all("li", class_="slide")
for r in results[0]:
    try: 
        news_title = r.find("div", class_="content_title").get_text()
        news_p = r.find("div", class_="article_teaser_body").get_text()
    except:
        pass
#     print(news_title)
#     print('')
#     print(news_p)

# -----------------------
# Retrieve featured image
# -----------------------
img_site = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(img_site)
browser.links.find_by_partial_text('FULL').click()
browser.links.find_by_partial_href('/spaceimages/details').click()
browser.links.find_by_partial_href('/spaceimages/images/largesize/').click()

# https://splinter.readthedocs.io/en/latest/browser.html#verifying-page-url-with-browser-url
featured_image_url = browser.url

# -----------------------
# Retrieve facts table --
# -----------------------

facts_url ='https://space-facts.com/mars/'
mars_facts = pd.read_html(facts_url)

facts_table = mars_facts[0]
facts_table.to_html('mars_facts.html')

# ------------------------------------------------
# Create dictionary for hemispheres and image urls
# ------------------------------------------------
hemisphere_names = ["Cerberus Hemisphere Enhanced", "Schiaparelli Hemisphere Enhanced", "Syrtis Major Hemisphere Enhanced", "Valles Marineris Hemisphere Enhanced"]
hemisphere_image_urls = []

# hems_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
# browser.visit(hems_url)
# html = browser.html
# soup = BeautifulSoup(html, "html.parser")
# titles = soup.find_all("div", class_="description")
for h in hemisphere_names:
    hems_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hems_url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    browser.links.find_by_partial_text(h).click()
    
    result = {}
    result["title"] = h
    browser.links.find_by_partial_text('Sample').click()
    result["img_url"] = browser.url+".tif/full.jpg"
        
    hemisphere_image_urls.append(result)

    
#     print(hemisphere_image_urls)


#browser.quit()










