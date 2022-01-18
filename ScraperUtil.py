import pandas as pd


class ScraperUtil:

    # TODO: Doc Comments.

    @staticmethod
    def construct_dataframe(all_jobs):

        print("Type: ", type(all_jobs))
        """Extracts data from list of Job objects, and returns a dataframe."""
        all_job_data = []

        for job in all_jobs:
            job_data = [job.title, job.company_name, job.source, job.link, job.date]
            all_job_data.append(job_data)

        df = pd.DataFrame(all_job_data, columns=['Title', 'Company', 'Source', 'Link', 'Date Posted'])
        df['Applied'] = False
        df['Date Applied'] = ""

        return df

    @staticmethod
    def drop_duplicates(df):
        # TODO: implement this.
        pass



    @staticmethod
    def remove_rows_with_keywords(df, keywords):
        # TODO: Assertions
        delimited_keywords = "(?i)" + str("|".join(keywords)).lower()

        print("delimited_keywords:", delimited_keywords)

        df = df[df["Title"].str.contains(delimited_keywords) == False]
        return df



