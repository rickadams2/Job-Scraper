from IndeedScraper import IndeedScraper
import pandas as pd
import json
from configparser import ConfigParser
from LinkedInScraper import LinkedInScraper
from ScraperUtil import ScraperUtil

if __name__ == "__main__":

    # Load search variables from config file.
    with open("config.json", "r") as jsonfile:
        config = json.load(jsonfile)
        print("Read config successfully.")

    search_term = config["search_term"]
    print("search_term:", search_term)
    location = config["location"]
    print("location:", location)
    ignore_keywords = config['ignore_keywords']
    print("ignore_keywords:", ignore_keywords)

    all_dfs = []

    # Create scraper objects using variables from config file.

    # Attempt to scrape Indeed.
    indeed = None
    try:
        indeed = IndeedScraper(search_term, location)
        print(indeed.data.shape[0], "jobs loaded from Indeed.")
    except Exception as e:
        print("ERROR : " + str(e))

    # Attempt to scrape LinkedIn.
    linkedin = None
    try:
        linkedin = LinkedInScraper()
        print(linkedin.data.shape[0], "jobs loaded from LinkedIn.")
    except Exception as e:
        print("ERROR : " + str(e))

    all_dfs.append(indeed.data)
    all_dfs.append(linkedin.data)

    old_df = None
    try:
        old_df = pd.read_excel('job-data.xlsx')
    except:
        old_df = ScraperUtil.construct_dataframe([])

    all_dfs.append(old_df)

    new_df = pd.concat(all_dfs)
    print("Rows before dropping duplicates:", new_df.shape[0])
    new_df.drop_duplicates(keep='last', subset=['Title', 'Company', 'Link'], inplace=True)
    print("Rows after dropping duplicates:", new_df.shape[0])
    new_df.to_excel('job-data.xlsx', index=False)
