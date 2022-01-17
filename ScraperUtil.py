import pandas as pd


class ScraperUtil:

    @staticmethod
    def construct_dataframe(all_jobs):
        """Extracts data from list of Job objects, and returns a dataframe."""
        all_job_data = []

        for job in all_jobs:
            job_data = [job.title, job.company_name, job.source, job.link, job.date]
            all_job_data.append(job_data)

        df = pd.DataFrame(all_job_data, columns=['Title', 'Company', 'Source', 'Link', 'Date'])

        return df
