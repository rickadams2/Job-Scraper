import urllib
from datetime import date

import requests
from bs4 import BeautifulSoup

from Job import Job
from ScraperUtil import ScraperUtil


# TODO: IndeedScraper implements Scraper
# TODO: Doc Comments.
class IndeedScraper:

    def __init__(self):
        self.data = ScraperUtil.construct_dataframe(all_jobs = [])

    def scrape(self, search_keywords, job_location):
        url = self.construct_url(search_keywords, job_location)
        job_divs = self.get_all_job_divs(url)
        jobs = self.construct_job_objects(job_divs)
        self.data = ScraperUtil.construct_dataframe(jobs)

    def construct_url(self, search_keywords, job_location):
        """Constructs an Indeed url using the provided variables and returns it."""

        # Create a dictionary mapping each variable in the url to a value.
        url_vars = {'q': search_keywords,
                    'l': job_location,
                    'radius': '15',
                    'explvl': 'entry_level',
                    'sort': 'date',
                    'limit': '50',
                    'fromage': '1'
                    }

        # Construct and return the url.
        url = ('https://www.indeed.com/jobs?' + urllib.parse.urlencode(url_vars))

        print("Sourcing Indeed data from:", url)
        return url

    def get_all_job_divs(self, url):
        """Retrieves html from provided url. Returns the important html containing all job information."""
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        job_divs = soup.find_all(class_ = lambda value: value and value.startswith("tapItem fs-unmask result"))
        return job_divs

    def construct_job_objects(self, job_divs):
        """Returns a list of Job objects using the information provided within the html."""
        all_jobs = []

        for job_div in job_divs:
            # Extract relevant information.

            # We are stripping the "new" from the front of the title.
            title = job_div.find('h2', class_='jobTitle').text.strip()[3:]
            company_name = job_div.find('span', class_="companyName").text.strip()
            link = "https://indeed.com" + job_div["href"]
            job_date = date.today()

            # Create a new Job object.
            all_jobs.append(Job(title, company_name, "Indeed", link, job_date))

        print("Created", len(all_jobs), "job objects from Indeed.")
        return all_jobs
