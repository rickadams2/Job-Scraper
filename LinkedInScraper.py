import time
import urllib
from datetime import date

from bs4 import BeautifulSoup
from selenium import webdriver

from Job import Job
from ScraperUtil import ScraperUtil


# TODO: LinkedInScraper implements Scraper
# TODO: Doc Comments.

class LinkedInScraper:

    def __init__(self):
        self.data = ScraperUtil.construct_dataframe(all_jobs=[])

    def scrape(self, search_keywords, job_location, ignore_keywords, experience):

        url = self.construct_url(search_keywords, job_location, experience)
        soup = self.get_entire_page_soup(url)
        all_job_divs = self.get_job_divs(soup)
        jobs = self.construct_job_objects(all_job_divs)
        self.data = ScraperUtil.construct_dataframe(jobs)
        self.data = ScraperUtil.remove_rows_with_keywords(self.data, ignore_keywords)

    def construct_url(self, search_keywords, job_location, experience):
        """Constructs a LinkedIn url using the provided variables and returns it."""
        experience_switch = self.experience_switch(experience)

        # Create a dictionary mapping each variable in the url to a value.
        url_vars = {'keywords': search_keywords,
                    'location': job_location,
                    'locationId': "",
                    'geoId': "",
                    'f_TPR': 'r86400',  # Ensures job listings are from the last 24 hours.
                    'f_E': experience_switch,
                    'position': '1'
                    }

        # Construct and return the url.
        url = ('https://www.linkedin.com/jobs/search?' + urllib.parse.urlencode(url_vars))
        print("Sourcing LinkedIn data from:", url)
        return url

    def experience_switch(self, experience):
        """Converts the provided experience string to its corresponding experience url var."""
        if experience == "junior":
            return "1,2"
        elif experience == "mid":
            return "3,4"
        elif experience == "senior":
            return "5,6"
        else:
            return ""

    def get_entire_page_soup(self, url):
        """Create and return a soup object from LinkedIn once the entire page is loaded."""
        # Create a web driver from the provided link.
        web_driver = webdriver.Chrome("./chromedriver")
        web_driver.get(url)

        # Read and print the header text which shows how many jobs match our search query.
        no_of_jobs = web_driver.find_element_by_css_selector('h1 > span').get_attribute('innerText')
        print(no_of_jobs, "jobs expected to be loaded from LinkedIn.")

        # Scroll page slowly to ensure all jobs are loaded into HTML doc.
        self.scroll_page(web_driver)

        # Once the entire page is loaded, we can extract the page source and return it.
        job_src = web_driver.page_source
        soup = BeautifulSoup(job_src, 'html.parser')
        return soup

    def scroll_page(self, web_driver):
        """
        Automatically scrolls the webpage one screen at a time,
        to ensure all job information is loaded into the html.

        Help from:
        https://medium.com/analytics-vidhya/using-python-and-selenium-to-scrape-infinite-scroll-web-pages-825d12c24ec7
        """

        # Maximise window so there are no hidden elements.
        web_driver.maximize_window()

        # Wait 5 seconds for the page to load completely.
        time.sleep(5)
        scroll_pause_time = 1  # The amount of time before the page is scrolled by one screen.
        screen_height = web_driver.execute_script("return window.screen.height;")  # get the screen height of the web
        total_screens_scrolled = 1

        while True:
            # scroll one screen height each time
            web_driver.execute_script(
                "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height,
                                                                  i=total_screens_scrolled))
            total_screens_scrolled += 1
            time.sleep(scroll_pause_time)
            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = web_driver.execute_script("return document.body.scrollHeight;")
            # Break the loop when the height we need to scroll to is larger than the total scroll height

            if (screen_height * total_screens_scrolled) > scroll_height:
                try:
                    web_driver.find_element_by_xpath("/html/body/div[1]/div/main/section[2]/button").click()
                    time.sleep(scroll_pause_time)
                except:
                    break

    def get_job_divs(self, soup):
        """Returns all 'li' divs, as they contain job information."""
        job_divs = soup.find('ul', class_="jobs-search__results-list").find_all('li')
        return job_divs

    def construct_job_objects(self, job_divs):
        """Calls create_job_from_div() on all job_divs, then returns a list of Job objects."""
        all_jobs = []

        for job_div in job_divs:
            job = self.create_job_from_div(job_div)
            all_jobs.append(job)

        print("Created", len(all_jobs), "Job objects.")
        return all_jobs

    def create_job_from_div(self, job_div):
        """Attempts to extract all information from job_div to create job object.
        If any expected tags are missing, the missing field is represented as 'N/A'. """

        # Attempt to extract each piece of information.
        try:
            job_title = job_div.find('h3', {'class': 'base-search-card__title'}).text.strip()
        except:
            job_title = "N/A"
        try:
            company_name = job_div.find('h4', {'class': 'base-search-card__subtitle'}).text.strip()
        except:
            company_name = "N/A"
        try:
            link = job_div.find('a', {'class': "base-card__full-link"})['href']
        except:
            link = "N/A"

        # All information possible extracted. Return the new Job object.
        return Job(job_title, company_name, "LinkedIn", link, str(date.today()))
