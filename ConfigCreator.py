from configparser import ConfigParser

#Get the configparser object
config_object = ConfigParser()

#Assume we need 2 sections in the config file, let's call them USERINFO and SERVERCONFIG
config_object["SEARCH_SETTINGS"] = {
    "Search_Term": "Software Engineer",
    "Location": "San Francisco, CA"
}

config_object["IGNORE_KEYWORDS"] = {
    "Keywords": ["Senior", "Lead"]
}

#Write the above sections to config.ini file
with open('config.ini', 'w') as conf:
    config_object.write(conf)