# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import lxml.html as lh
import pandas as pd
import re
import time

def scrape():
    # Open borowser
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome",**executable_path, headless=False)


    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news'
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url3 = 'https://twitter.com/marswxreport?lang=en'
    url4 = 'https://space-facts.com/mars/'
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Requests of the URLs
    news_request = requests.get(url)
    #spaceimages_request = requests.get(url2)
    #twitter_request = requests.get(url3)
    #facts_request = requests.get(url4)
    #hemisphere_request = requests.get(url5)

    # First scrapping
    news_request.text
    news = bs(news_request.text, "html.parser")

    ##Get the Title of the page
    TITLE = news.find("title")
    TITLE = TITLE.get_text().replace('\n', '').strip()


    ##Get the title of the first news
    content_title = news.find(class_="content_title")
    news_title = content_title.get_text().replace('\n', '').strip()

    ## Get the description of the first news.
    rollover_description_inner = news.find(class_="rollover_description_inner")
    news_p = rollover_description_inner.get_text().replace('\n', '').strip()


    # Second Scrapping
    browser.visit(url2)
    browser.find_by_id('full_image').click()
    html = browser.html
    soup = bs(html,"html.parser")

    featured_image_url = soup.find("article",class_="carousel_item").get('style')
    featured_image_url = featured_image_url.split("'")[1]
    featured_image_url = f"https://www.jpl.nasa.gov{featured_image_url}"

    # Third Scraping
    browser.visit(url3)
    time.sleep(6)
    html = browser.html
    soup = bs(html,"html.parser")

    mars_weather = soup.find(text=re.compile('InSight'))

    #mars_weather = soup.find_all(class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    #mars_weather = mars_weather[23].text

    # Fourth Scraping
    tables = pd.read_html(url4)
    tables[0]
    HTML_TABLE = tables[0].to_html()
    HTML_TABLE = bs(HTML_TABLE, "html.parser")


    # Fifth Scraping
    browser.visit(url5)
    browser.find_by_tag('h3')[0].click()
    html = browser.html
    soup = bs(html,"html.parser")

    ##First image data
    url5_1 = soup.find_all('li')
    url5_11 = url5_1[0]
    url5_11 = url5_11.a["href"]
    url5_12 = soup.find('h2',class_="title").text

    ##Second image data
    browser.visit(url5)
    browser.find_by_tag('h3')[1].click()
    html = browser.html
    soup = bs(html,"html.parser")
    url5_2 = soup.find_all('li')
    url5_21 = url5_2[0]
    url5_21 = url5_21.a["href"]
    url5_22 = soup.find('h2',class_="title").text

    ##Third image data
    browser.visit(url5)
    browser.find_by_tag('h3')[2].click()
    html = browser.html
    soup = bs(html,"html.parser")
    url5_3 = soup.find_all('li')
    url5_31 = url5_3[0]
    url5_31 = url5_31.a["href"]
    url5_32 = soup.find('h2',class_="title").text

    ##Fourth image data
    browser.visit(url5)
    browser.find_by_tag('h3')[3].click()
    html = browser.html
    soup = bs(html,"html.parser")
    url5_4 = soup.find_all('li')
    url5_41 = url5_4[0]
    url5_41 = url5_41.a["href"]
    url5_42 = soup.find('h2',class_="title").text


    hemisphere_image_urls = [
        {"title": url5_11, "img_url": url5_12},
        {"title": url5_21, "img_url": url5_22},
        {"title": url5_31, "img_url": url5_32},
        {"title": url5_41, "img_url": url5_42},
    ]

    listings = {}
    listings["title"] = TITLE
    listings["newsH"] = news_title
    listings["newsP"] = news_p
    listings["featuredImg"] = featured_image_url
    listings["weather"] = mars_weather
    #listings["HTMLtable"] = HTML_TABLE
    #listings["HemisphereDic"] = hemisphere_image_urls
    listings["url5_11"] = url5_11
    listings["url5_12"] = url5_12
    listings["url5_21"] = url5_21
    listings["url5_22"] = url5_22
    listings["url5_31"] = url5_31
    listings["url5_32"] = url5_32
    listings["url5_41"] = url5_41
    listings["url5_42"] = url5_42

    browser.quit()
    return listings

