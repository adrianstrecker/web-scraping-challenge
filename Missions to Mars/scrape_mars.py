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

def scrape():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)
    mars_info = []
    news_title = []
    news_p = []
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find("li", class_="slide")

    for r in results:
        try: 
            mars = {}
            mars["news_title"] = r.find("div", class_="content_title").get_text()
            mars["news_p"] = r.find("div", class_="article_teaser_body").get_text()
            mars_info.append(mars)

        except:
            pass
    # return mars_info
    #     print(news_title)
    #     print('')
    #     print(news_p)



    # -----------------------
    # Retrieve featured image
    # -----------------------
    featured_image_url = {}
    img_site = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_site)
    browser.links.find_by_partial_text('FULL').click()
    browser.links.find_by_partial_href('/spaceimages/details').click()
    browser.links.find_by_partial_href('/spaceimages/images/largesize/').click()

    # https://splinter.readthedocs.io/en/latest/browser.html#verifying-page-url-with-browser-url
    featured_image_url["featured_image_url"] = browser.url
    mars_info.append(featured_image_url)
    

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
    hemisphere_names = []
    hems_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hems_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    titles = soup.find_all("div", class_="description")
    for t in titles:
        try:
            result = []
            result = t.find("h3").get_text()
            hemisphere_names.append(result)
        except:
            pass
    # return hemisphere_names

    
    hemisphere_image_urls = []


    for h in hemisphere_names:
        try:
            hems_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
            browser.visit(hems_url)
            time.sleep(2)
            html = browser.html
            soup = BeautifulSoup(html, "html.parser")
            browser.links.find_by_partial_text(h).click()
            
            result = {}
            result["title"] = h
            browser.links.find_by_partial_text('Sample').click()
            result["img_url"] = browser.url+".tif/full.jpg"
                
            mars_info.append(result)
        except:
            pass

    browser.quit()
    return mars_info

#     print(hemisphere_image_urls)


#browser.quit()










