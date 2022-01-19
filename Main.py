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
    experience = config['experience'].lower()
    if experience != "junior" or experience != "mid" or experience != "senior":
        print("Warning: Experience value in 'config.json' is invalid. please choose either 'Junior', 'Mid', "
              "or 'Senior'. Jobs of all experience levels will be included in this search.")

    print("search_keywords=", search_keywords)
    print("location=", location)
    print("ignore_keywords=", ignore_keywords)
    print("experience=", experience)

    all_dataframes = []

    # Attempt to scrape Indeed.
    indeed = IndeedScraper()
    try:
        indeed.scrape(search_keywords, location, experience)
        indeed.data = ScraperUtil.remove_rows_with_keywords(indeed.data, ignore_keywords)
        print(indeed.data.shape[0], "jobs loaded from Indeed.")
    except Exception as e:
        print("Error loading jobs from Indeed: " + str(e))

    # Attempt to scrape LinkedIn.
    linkedin = LinkedInScraper()
    try:
        linkedin.scrape(search_keywords, location, experience)
        linkedin.data = ScraperUtil.remove_rows_with_keywords(linkedin.data, ignore_keywords)
    except Exception as e:
        print("Error loading jobs from LinkedIn: " + str(e))

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


