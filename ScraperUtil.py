import pandas as pd


class ScraperUtil:

    @staticmethod
    def construct_dataframe(all_jobs):
        """Extracts data from list of Job objects, and returns a dataframe."""
        all_job_data = []

        # Here we create a list of lists. each nested list represents one row in the dataframe.
        for job in all_jobs:
            job_data = [job.title, job.company_name, job.source, job.link, job.date]
            all_job_data.append(job_data)

        # Create the dataframe with the above information.
        dataframe = pd.DataFrame(all_job_data, columns=['Title', 'Company', 'Source', 'Link', 'Date Posted'])

        # Add additional rows to the dataframe, containing default values.
        dataframe['Applied'] = False
        dataframe['Date Applied'] = ""

        return dataframe

    @staticmethod
    def remove_rows_with_keywords(dataframe, keywords):
        """
        Removes all rows from a given DataFrame where the title contains any of the provided keywords.
        Returns the filtered DataFrame.
        """

        # First we convert the list of keywords into a delimited string. The string
        # is a regex in the form "(?i)keyword1|keyword2|...|keyword3".
        # (?i) ensures the contains() function is case-insensitive.

        delimited_keywords = "(?i)" + str("|".join(keywords)).lower()

        total_rows_before = dataframe.shape[0]
        # Selects all rows that don't match the above regex.
        dataframe = dataframe[dataframe["Title"].str.contains(delimited_keywords) == False]
        total_rows_after = total_rows_before - dataframe.shape[0]
        total_rows_removed = total_rows_before - total_rows_after
        print(total_rows_removed, "duplicate rows were removed from dataframe.")

        #Return the filtered dataframe.
        return dataframe



