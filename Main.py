import json
import sys
import threading

import pandas as pd

from IndeedScraper import IndeedScraper
from LinkedInScraper import LinkedInScraper
from ScraperUtil import ScraperUtil


def run_search(json_file_name):
    """Collects job listings that match the parameters stored in the provided json file."""

    # Attempt to load the json file. If it isn't successful, close the program.
    try:
        search_keywords, location, ignore_keywords, experience = load_json(json_file_name)
    except:
        return

    # Store just the file name, not the file extension. This is useful for creating a new Excel file.
    file_name = json_file_name.split('.')[0]
    all_dataframes = [scrape_indeed(search_keywords, location, ignore_keywords, experience),
                      scrape_linkedin(search_keywords, location, ignore_keywords, experience)]

    # Stores the search results within an Excel file.
    store_in_excel_file(file_name, all_dataframes)


def load_json(json_file_name):
    # Load search variables from config file.
    try:
        with open(json_file_name, "r") as jsonfile:
            config = json.load(jsonfile)

            # Save all search parameters as variables.
            search_keywords = config["search_keywords"]
            location = config["location"]
            ignore_keywords = config['ignore_keywords']
            experience = str(config['experience'].lower())

            # Warn the user if they haven't provided a valid experience parameter.
            if experience not in ["junior", "mid", "senior"]:
                print(
                    "Warning: Experience value in", json_file_name,
                    " is invalid. please choose either 'Junior', 'Mid', "
                    "or 'Senior'. Jobs of all experience levels will be included in this search.")

            # Print a summary of the search parameters.
            print("Read config successfully.")
            print("search_keywords=", search_keywords)
            print("location=", location)
            print("ignore_keywords=", ignore_keywords)
            print("experience=", experience)
            return search_keywords, location, ignore_keywords, experience
    except Exception as e:
        raise ValueError("Error, could not load ", json_file_name, str(e))


def scrape_indeed(search_keywords, location, ignore_keywords, experience):
    """Instantiates and calls scrape() method on a LinkedInScraper object.
    returns the dataframe stored in the object once the search is complete."""

    indeed = IndeedScraper()
    try:
        indeed.scrape(search_keywords, location, ignore_keywords, experience)
        print(indeed.data.shape[0], "jobs loaded from Indeed.")
        return indeed.data
    except Exception as e:
        print("Error loading jobs from Indeed: " + str(e))
        return ScraperUtil.construct_dataframe([])  # Return an empty dataframe.


def scrape_linkedin(search_keywords, location, ignore_keywords, experience):
    """Instantiates and calls scrape() method on an IndeedScraper object.
        returns the dataframe stored in the object once the search is complete."""

    linkedin = LinkedInScraper()
    try:
        linkedin.scrape(search_keywords, location, ignore_keywords, experience)
        print(linkedin.data.shape[0], "jobs loaded from LinkedIn.")
        return linkedin.data

    except Exception as e:
        print("Error loading jobs from LinkedIn: " + str(e))
        return ScraperUtil.construct_dataframe([])  # Return an empty dataframe.


def store_in_excel_file(file_name, all_dataframes):
    """Stores all job listings in an Excel file. If the file exists, new listings are added to the existing file.
    Otherwise, a new Excel file is created."""
    master_dataframe = ScraperUtil.construct_dataframe([])

    try:
        master_dataframe = pd.read_excel(file_name + '.xlsx')
    except:
        print(file_name + ".xlsx doesn't exist yet. Creating new file.")

    all_dataframes.append(master_dataframe)

    new_dataframe = pd.concat(all_dataframes)
    length_before = new_dataframe.shape[0]
    new_dataframe.drop_duplicates(keep='last', subset=['Title', 'Company', 'Source', 'Date Posted'], inplace=True)
    length_after = new_dataframe.shape[0]
    total_duplicates = length_before - length_after
    print("Total duplicates dropped:", total_duplicates)
    new_dataframe.to_excel(file_name + '.xlsx', index=False)


if __name__ == "__main__":

    total_args = len(sys.argv) - 1
    all_threads = []

    if total_args == 0:
        print("Error: No arguments provided. Please provide one or more config file names as arguments.")
    else:
        for i in range(total_args):
            arg = str(sys.argv[i + 1])
            all_threads.append(threading.Thread(target=run_search, args=(arg,)))

        for thread in all_threads:
            thread.start()

        for thread in all_threads:
            thread.join()
