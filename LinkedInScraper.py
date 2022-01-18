from selenium import webdriver
from bs4 import BeautifulSoup
import time
import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd

from ScraperUtil import ScraperUtil
from Job import Job
from datetime import date
import time
from selenium import webdriver

# TODO: LinkedInScraper implements Scraper
# TODO: Doc Comments.

class LinkedInScraper:

    data = pd.DataFrame()
    def __init__(self):
        url = self.construct_url("Software Engineer", "San Francisco Bay Area")
        page_source = self.load_entire_page(url)
        jobs = self.construct_job_objects(page_source)
        self.data = ScraperUtil.construct_dataframe(jobs)

    # TODO: Update method so url is changed according to provided variables.
    def construct_url(self, job_title, job_location):
        return "https://www.linkedin.com/jobs/search?keywords=Software&location=San%20Francisco%20Bay%20Area&locationId=&geoId=90000084&f_TPR=r86400&f_E=1%2C2&position=1"

    def load_entire_page(self, url):
        web_driver = webdriver.Chrome("./chromedriver")
        web_driver.get(url)

        no_of_jobs = int(web_driver.find_element_by_css_selector('h1 > span').get_attribute('innerText'))
        print(no_of_jobs, "jobs expected to be loaded from LinkedIn.")

        # Scroll page slowly to ensure all jobs are loaded into HTML doc.
        self.scroll_page(web_driver)

        job_lists = web_driver.find_element_by_class_name('jobs-search__results-list')
        jobs = job_lists.find_elements_by_tag_name('li')  # return a list

        # TODO: Fix bug where not all jobs are being loaded from linkedin
        print(len(jobs), "jobs loaded from LinkedIn.")

        job_src = web_driver.page_source
        soup = BeautifulSoup(job_src, 'html.parser')
        return soup

    def scroll_page(self, web_driver):
        """Automatically scrolls the webpage slowly, to ensure all job information is loaded into the html."""
        # Help from:
        # https://medium.com/analytics-vidhya/using-python-and-selenium-to-scrape-infinite-scroll-web-pages-825d12c24ec7

        web_driver.maximize_window()
        time.sleep(5)
        scroll_pause_time = 2
        screen_height = web_driver.execute_script("return window.screen.height;")  # get the screen height of the web
        i = 1

        while True:
            # scroll one screen height each time
            web_driver.execute_script(
                "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
            i += 1
            time.sleep(scroll_pause_time)
            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = web_driver.execute_script("return document.body.scrollHeight;")
            # Break the loop when the height we need to scroll to is larger than the total scroll height

            if (screen_height) * i > scroll_height:
                try:
                    web_driver.find_element_by_xpath("/html/body/div[1]/div/main/section[2]/button").click()
                except:
                    break



    def construct_job_objects(self, page_source):
        # TODO: Assertions
        all_jobs = []
        job_titles = []
        company_names = []
        links = []

        # Get list of job titles and add them to the list.
        job_title_html = page_source.find_all(
            'h3', {'class': 'base-search-card__title'})

        for title in job_title_html:
            job_titles.append(title.text.strip())

        # Get list of company names and add them to the list.
        company_names_html = page_source.find_all(
            'h4', {'class': 'base-search-card__subtitle'})

        for name in company_names_html:
            company_names.append(name.text.strip())
            links.append(name.find('a')['href'])

        # Create job objects using saved information.
        for i in range(len(job_titles)):
            all_jobs.append(Job(job_titles[i], company_names[i], "LinkedIn", links[i], date.today()))

        print("Created", len(all_jobs), "Job objects.")
        return all_jobs









