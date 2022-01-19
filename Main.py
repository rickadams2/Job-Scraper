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

    print("search_keywords=", search_keywords)
    print("location=", location)
    print("ignore_keywords=", ignore_keywords)

    all_dataframes = []

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
    linkedin.scrape(search_keywords, location)
    linkedin.data = ScraperUtil.remove_rows_with_keywords(linkedin.data, ignore_keywords)

    print(linkedin.data.shape[0], "jobs loaded from LinkedIn.")

    all_dataframes.append(indeed.data)
    all_dataframes.append(linkedin.data)

    old_dataframe = ScraperUtil.construct_dataframe([])
    try:
        old_dataframe = pd.read_excel('job-data.xlsx')
    except:
        print("job-data.xlsx doesn't exist yet. Creating new file.")

    all_dataframes.append(old_dataframe)

    new_dataframe = pd.concat(all_dataframes)
    length_before = new_dataframe.shape[0]
    new_dataframe.drop_duplicates(keep='last', subset=['Title', 'Company', 'Source', 'Date Posted'], inplace=True)
    length_after = new_dataframe.shape[0]
    total_duplicates = length_before - length_after
    print("Total duplicates dropped:", total_duplicates)
    new_dataframe.to_excel('job-data.xlsx', index=False)
