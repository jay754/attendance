from Exceptions import *

from bs4 import BeautifulSoup as bs
import json
import urllib2
import requests

class Attendance(object):

    def __init__(self):
        self.url = "http://espn.go.com/nba/attendance//year/2013"

    def check_request(self, url):
        return requests.get(url).status_code

    def get_data(self):
        http_status = self.check_request(self.url)
        soup = bs(urllib2.urlopen(self.url), "html.parser")
        data = [str(i.get_text()) for i in soup.find_all("td")]

        if http_status is not None and http_status == 200:
            return data[17:]
        elif http_status != 200:
            raise Exception("error with getting data")
        else:
            return None

    def get_nums(self):
        if self.get_data() is not None: nums = [i.replace(" ", "") \
                           for i in self.get_data() if not i.isalpha()]

        return nums

    def get_teams(self):
        if self.get_data() is not None: names = [i.replace(" ", "") \
                           for i in self.get_data() if i.isalpha()]

        names.insert(16, "76ers")
        return names

    def sanitize_data(self):
        striped_comma = [i.replace(",", "") for i in self.get_nums()]
        attendance = [i.replace(".", "") for i in striped_comma]
        return attendance

    def get_attendance(self):
        attendance = set()
        for i in self.sanitize_data():
            if i is not "76ers" and int(i) > 500000:
                attendance.add(i)

        return attendance

    def organize_data(self):
        if self.get_teams() is not None:
            teams = self.get_teams()

        if self.get_attendance() is not None:
            attendance = self.get_attendance()

        data = {"Teams" : teams,
                "Attendance": attendance}

        return data
