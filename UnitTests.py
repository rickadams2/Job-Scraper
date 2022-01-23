import unittest

import pandas as pd

from ScraperUtil import ScraperUtil


# TODO: Additional unit tests.
class UnitTests(unittest.TestCase):
    def test_remove_rows_with_keywords_1(self):
        data = {'Title': ["Senior Software Engineer", "Lead Software Engineer", "Junior Software Engineer"]}
        df = pd.DataFrame(data)
        print(df)

        df = ScraperUtil.remove_rows_with_keywords(df, ['Senior', 'Lead'])
        print(df)

        assert df.shape[0] == 1


if __name__ == '__main__':
    unittest.main()
