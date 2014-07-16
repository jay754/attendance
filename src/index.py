from bs4 import BeautifulSoup as bs
from Exceptions import *

import json
import urllib2
import requests


class Attendance(object):

    def __init__(self, url=None):
        self.url = url

    def get_url(self):
        """
        A setter for thr url
        """

        return self.url

    def check_request(self, url):
        """
        To check the http status of the url
        """

        return requests.get(url).status_code

    def get_data(self):
        """
        Getting the Actual Data from the Espn Url
        """

        http_status = self.check_request(self.url)

        if http_status is None:
            return None
        elif http_status is not None and http_status == 200:
            soup = bs(urllib2.urlopen(self.url))
            data = [str(i.get_text()) for i in soup.find_all("td")]
            return data[17:]
        else:
            return -1

    def get_nums(self):

        if self.get_data() is not None:
            nums = [i.replace(" ", "") for i in self.get_data() if not i.isalpha()]
        
        return nums

    def get_teams(self):

        if self.get_data() is not None:
            names = [i.replace(" ", "") for i in self.get_data() if i.isalpha()]

        names.insert(16, "76ers")

        return names

    def sanitize_data(self):

        if self.get_nums() is not None:
            striped_comma = [i.replace(",", "") for i in self.get_nums()]
            attendance = [i.replace(".", "") for i in striped_comma]

        return attendance

    def get_attendance(self):

        attendance = set()

        if self.sanitize_data() is not None:
            for i in self.sanitize_data():
                if i not "76ers":
                    if int(i) > 500000:
                        attendance.add(i)

        return attendance

    def organize_data(self):

        if self.get_teams() not None:
            teams = self.get_teams()

        if self.get_attendance() not None:
            attendance = self.get_attendance()

        data = dict(
                "Teams" : teams,
                "Attendance": attendance
                )

        return data

def main():
    try:
        atteOBJ = attendance()
        data = atteOBJ.organizeData()
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
    except:
        raise JsonError

if __name__ == '__main__': main()