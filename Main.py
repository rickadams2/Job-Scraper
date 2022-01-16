from IndeedScraper import IndeedScraper
import pandas as pd

if __name__ == "__main__":
    scraper = IndeedScraper("software", "San Francisco, CA")
    #Initialise dfs
    old_df = pd.DataFrame()
    new_df = pd.DataFrame()

    try:
        print("Entered try")
        old_df = pd.read_excel('job-data.xlsx')
        new_df = scraper.data.append(old_df, ignore_index=True)
        new_df.drop(new_df.columns[[4]], axis=1, inplace=True)
    except:
        print("Entered except")
        new_df = scraper.data

    new_df.to_excel('job-data.xlsx')