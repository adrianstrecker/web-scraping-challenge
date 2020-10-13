from splinter import Browser
from bs4 import BeautifulSoup
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    listings = []
    listing = {}

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all("li", class_="slides")
    for r in results :
	print(result("div", class_="content_title").text)
        
	try:
            listing = {} # class ! This was the problem, I needed to reset the listing dictionary,  it was trying to insert the same item over and over
            listing["headline"] = i.find("a", class_="result-title").get_text()
            listing["price"] = i.find("span", class_="result-price").get_text()
            listing["hood"] = i.find("span", class_="result-hood").get_text()
            listing["img_url"] = i.find("div", class_="swipe").find("img")["src"]
            listings.append(listing)
        except:
           pass

    browser.quit()

    return listings

