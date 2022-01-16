import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd
from Job import Job
from datetime import date


class IndeedScraper:

    data = pd.DataFrame()

    def __init__(self, job_title, job_location):
        url = self.construct_url(job_title, job_location)
        job_divs = self.get_all_job_divs(url)
        jobs = self.construct_job_objects(job_divs)
        self.data = self.construct_dataframe(jobs)

    def construct_url(self, job_title, job_location):
        """Constructs an Indeed url using the provided variables and returns it."""
        url_vars = {'q': job_title,
                    'l': job_location,
                    'radius': '15',
                    'explvl': 'entry_level',
                    'sort': 'date',
                    'limit': '50',
                    'fromage': 'last'
                    }
        url = ('https://www.indeed.com/jobs?' + urllib.parse.urlencode(url_vars))
        print(url)
        return url

    def get_all_job_divs(self, url):
        """Retrieves html from provided url. Returns the important html containing all job information."""
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        all_divs = soup.find_all(class_ = "jobtitle turnstileLink")
        return all_divs


    def construct_job_objects(self, job_divs):
        """Returns a list of Job objects using the information provided within the html."""
        all_jobs = []

        """
        NOTES FOR NEXT TIME.
        <a> tag surrounds slider container. first get list of <a> links from mosaic-provider-jobcards,
        then get other info from child element, 'slider container'.   
        """


        for i, job_div in enumerate(job_divs):
            # Extract relevant information.

            title = job_div.find('h2', class_='jobTitle').text.strip()
            company_name = job_div.find('span', class_="companyName").text.strip()
            link = "https://indeed.com" + job_div.find("a")["href"]
            date = date.today()
            # Create a new Job object.
            all_jobs.append(Job(title, company_name, link, date))

        print("Created", len(all_jobs), "job objects.")
        return all_jobs

    def construct_dataframe(self, all_jobs):
        """Extracts data from list of Job objects, and returns a dataframe."""
        all_job_data = []

        for job in all_jobs:
            job_data = [job.title, job.company_name, job.link, job.date]
            all_job_data.append(job_data)

        df = pd.DataFrame(all_job_data, columns=['Title', 'Company', 'Link', 'Date'])
        print("Done")
        return df













