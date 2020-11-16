# import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
import time

# News title & paragraph scraping
def mars_news():

    executable_path = {"executable_path": "C:\\Users\\home\\Downloads\\tmp\\chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

    # visiting Mars News site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # waiting for Splinter to load the content of the site
    time.sleep(3)

    html = browser.html
    soup = bs(html, "html.parser")

    # Parsing results html with BeautifulSoup
    # try & except handling
    try:

        # scraping the Latest news title & its paragraph
        title = soup.find_all("div", class_="content_title")
        news_title = title[1].text.strip()
        news_paragraph = soup.find("div", class_="article_teaser_body").text

    except AttributeError:
        return None, None

    # closing browser after scraping
    browser.quit()

    # returning variables news_title and news_paragraph
    return news_title, news_paragraph

# featured image scraping
def featured_img():

    executable_path = {"executable_path": "C:\\Users\\home\\Downloads\\tmp\\chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)


    # visiting jpl site
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(1)

    # using Splinter to go to site and click Button with class name full_image
    # <footer> <a id="full_image" class="button fancybox">FULL IMAGE</footer>
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    # using Splinter to find "More Info" button and click it
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    # parsing results html with BeautifulSoup
    html = browser.html
    image_soup = bs(html, "html.parser")

    img = image_soup.select_one("figure.lede a img")

    # try & except handling
    try:
        img_url = img.get("src")
    except AttributeError:
        return None
    # combine with the base url
    img_url = f"https://www.jpl.nasa.gov{img_url}"

    # closing browser after scraping
    browser.quit()

    return img_url

# Mars facts scraping
def mars_facts():
    # using Pandas to read the table
    # try & except handling
    try:
        facts_df = pd.read_html("https://space-facts.com/mars/")[0]
    except BaseException:
        return None
    facts_df.columns=["Description", "Value"]
    #df.set_index("Description", inplace=True)

    # returning table in html format
    return facts_df.to_html(index=False)

# Hemisphere scraping
def hemisphere():

    executable_path = {"executable_path": "C:\\Users\\home\\Downloads\\tmp\\chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

    # visiting the site
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    # creating an empty list to strore result
    hemi_img_urls = []

    # acquiring a list of all the Hemisphere (product)
    products = browser.find_by_css("a.product-item h3")

    # looping through list of the Hemisphere to get title, url pair value
    for item in range(len(products)):
        hemisphere = {}

        browser.find_by_css("a.product-item h3")[item].click()
        time.sleep(1)
        # finding Sample image tag & get <href>
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]

        # finding Hemisphere title and storing into dictionary
        hemisphere["title"] = browser.find_by_css("h2.title").text

        # adding item to list
        hemi_img_urls.append(hemisphere)

        # going backward to the previous page
        browser.back()

    # closing browser after scraping
    browser.quit()

    # returning results
    return hemi_img_urls

# main web scraping
def scrape_data():

    # calling function to display latest news title and its paragraph
    news_title, news_paragraph = mars_news()

    # calling function to scrape featured image
    img_url = featured_img()

    # calling mars_facts function
    facts = mars_facts()

    # calling hemisphere function
    hemisphere_image_urls = hemisphere()

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": img_url,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
    }

    # returning results
    return data