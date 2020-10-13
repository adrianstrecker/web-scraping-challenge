from splinter import Browser
from bs4 import BeautifulSoup
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
browser = init_browser()


url = "https://mars.nasa.gov/news/"
browser.visit(url)
time.sleep(2)

html = browser.html
soup = BeautifulSoup(html, "html.parser")
results = soup.find_all("div", class_="content_title")
for r in results[1:41]:
    print(r.text)





