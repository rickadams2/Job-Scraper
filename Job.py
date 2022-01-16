class Job:
    title = ""
    company_name = ""
    link = ""
    date = ""

    def __init__(self, title="N/A", company_name="N/A", link="N/A", date="N/A"):
        self.title = title
        self.company_name = company_name
        self.link = link
        self.date = date

    def __str__(self):
        return str({"title" : self.title,
                    "company_name" : self.company_name,
                    "link" : self.link, "date" : self.date
                    })
