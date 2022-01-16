from IndeedScraper import IndeedScraper
import pandas as pd

if __name__ == "__main__":
    scraper = IndeedScraper("software", "San Francisco, CA")
    old_df = pd.DataFrame()
    try:
        old_df = pd.read_excel('job-data.xlsx')
    except:
        old_df = pd.DataFrame(columns=['Title', 'Company', 'Link', 'Date'])

    new_df = scraper.data.append(old_df, ignore_index = True)
    new_df.drop(new_df.columns[[4]], axis=1, inplace=True)
    new_df.to_excel('job-data.xlsx')