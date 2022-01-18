import json

import pandas as pd

from IndeedScraper import IndeedScraper
from LinkedInScraper import LinkedInScraper
from ScraperUtil import ScraperUtil

if __name__ == "__main__":

    # Load search variables from config file.
    with open("config.json", "r") as jsonfile:
        config = json.load(jsonfile)
        print("Read config successfully.")

    search_keywords = config["search_keywords"]
    location = config["location"]
    ignore_keywords = config['ignore_keywords']

    print("search_keywords:", search_keywords)
    print("location:", location)
    print("ignore_keywords:", ignore_keywords)

    all_dfs = []

    # Create scraper objects using variables from config file.

    # Attempt to scrape Indeed.
    indeed = IndeedScraper()
    try:
        indeed.scrape(search_keywords, location)
        indeed.data = ScraperUtil.remove_rows_with_keywords(indeed.data, ignore_keywords)
        print(indeed.data.shape[0], "jobs loaded from Indeed.")
    except Exception as e:
        print("ERROR : " + str(e))

    # Attempt to scrape LinkedIn.
    linkedin = LinkedInScraper()
    #try:
    linkedin.scrape(search_keywords, location)
    linkedin.data = ScraperUtil.remove_rows_with_keywords(linkedin.data, ignore_keywords)
    #except Exception as e:
        #print("ERROR : " + str(e))

    print(linkedin.data.shape[0], "jobs loaded from LinkedIn.")


    all_dfs.append(indeed.data)
    all_dfs.append(linkedin.data)

    old_df = ScraperUtil.construct_dataframe([])
    try:
        old_df = pd.read_excel('job-data.xlsx')
    except:
        print("job-data.xlsx doesn't exist yet. Creating new file.")

    all_dfs.append(old_df)

    new_df = pd.concat(all_dfs)
    new_df.drop_duplicates(keep='last', subset=['Title', 'Company', 'Link'], inplace=True)
    new_df.to_excel('job-data.xlsx', index=False)
