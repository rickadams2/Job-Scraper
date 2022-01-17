from IndeedScraper import IndeedScraper
import pandas as pd

from LinkedInScraper import LinkedInScraper

if __name__ == "__main__":

    all_dfs = []

    indeed = IndeedScraper("software", "San Francisco, CA")
    all_dfs.append(indeed.data)

    linkedin = LinkedInScraper()
    all_dfs.append(linkedin.data)

    old_df = None
    try:
        old_df = pd.read_excel('job-data.xlsx')
    except:
        old_df = pd.DataFrame([], columns=['Title', 'Company', 'Source', 'Link', 'Date'])

    all_dfs.append(old_df)

    new_df = pd.concat(all_dfs)
    new_df.drop_duplicates(keep='last', subset=['Link'], inplace=True)

    new_df.to_excel('job-data.xlsx', index = False)