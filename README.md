# Job-Scraper

A tool which automatically collects job information from search results and outputs them into an Excel spreadsheet. All duplicate jobs are automatically
filtered from the output. 

The scraper collects jobs from Indeed and LinkedIn. The scraper uses BeautifulSoup and Selenium to collect job information. 

Users can choose their own search parameters by editing 'config.json'. Users can specify their own keywords, locations, and keywords to ignore.

The scraper requires 'webdriver.exe' to be present in the project's directory. Please download a [webdriver](https://chromedriver.chromium.org/)
which is compatible with your version of Google Chrome. 

The scraper collects jobs which were advertised within last 24 hours. The project can be automated using tools such as Windows Task Scheduler.
 
 
