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

    # ---------------------------
    # Retrieve headline & summary
    # ---------------------------
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)


    # Assistance from Benjamin Alford
    mars_info = {}

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find("li", class_="slide")
    for r in results:
        try: 
            mars_info = {}
            mars_info["news_title"] = r.find("div", class_="content_title").get_text()
            mars_info["news_p"] = r.find("div", class_="article_teaser_body").get_text()
            
        except:
            break


    


    # -----------------------
    # Retrieve featured image
    # -----------------------
    img_site = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_site)
    browser.links.find_by_partial_text('FULL').click()
    browser.links.find_by_partial_href('/spaceimages/details').click()
    browser.links.find_by_partial_href('/spaceimages/images/largesize/').click()

    # https://splinter.readthedocs.io/en/latest/browser.html#verifying-page-url-with-browser-url
    mars_info["featured_image_url"] = browser.url


    # -----------------------
    # Retrieve facts table --
    # -----------------------
    table={}
    facts_url ='https://space-facts.com/mars/'
    mars_facts = pd.read_html(facts_url)

    facts_table = mars_facts[0]
    mars_info["facts_table"] = facts_table.to_html(header=False, index=False, classes="table-striped")
    

    

    # ------------------------------------------------
    # Create dictionary for hemispheres and image urls
    # ------------------------------------------------
    hemisphere_image_urls = []
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

    for h in hemisphere_names:
        hems_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hems_url)
        time.sleep(1)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        browser.links.find_by_partial_text(h).click()
            
        result = {}
        result["title"] = h
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        result["img_url"] = soup.find("div", class_="downloads").find("a")["href"]
        hemisphere_image_urls.append(result)
    mars_info["cerberus"] = hemisphere_image_urls[0]
    mars_info["schia"] = hemisphere_image_urls[1]
    mars_info["syr"] = hemisphere_image_urls[2]
    mars_info["valles"] = hemisphere_image_urls[3]

    # mars_info["hemispheres"] = hemisphere_image_urls

    browser.quit()

    return mars_info

