from bs4 import BeautifulSoup as bs
import urllib2
import requests

try:
    import json
except ImportError:
    import simplejson as json

#total attedance class for NBA 2014

class Attendance:

    def __init__(self, url=None):
        self.url = url
        self.data = []

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
        """
        Had to Get only numbers data for the total attendance.
        All the data wasn't only numbers. So I had to filter out the Team names and only keep the numbers
        """

        if self.get_data() is not None:
            nums = [i.replace(" ", "") for i in self.get_data() if not i.isalpha()]
        
        return nums

    def get_teams(self):
        """
        Returns all the teams in order from the most fans that attenended the games
        This is method was a little broken had to manually insert 76ers into the array
        """

        if self.get_data() is not None:
            names = [i.replace(" ", "") for i in self.get_data() if i.isalpha()]

        names.insert(16, "76ers")

        return names

    def sanitize_data(self):
        """
        Had to sanitize the numbers, because all of them contained commas, and decimals.
        You have to do this in order to convert from a String to an Integer
        """

        if self.get_nums() is not None:
            striped_comma = [i.replace(",", "") for i in self.get_nums()]
            attendance = [i.replace(".", "") for i in striped_comma]

        return attendance

    def get_attendance(self):
        """
        Gets the total attendance for each team
        """

        attendance = []

        if self.sanitize_data( is not None:
            for i in self.sanitize_data():
                if i != "76ers":
                    if int(i) > 500000:
                        attendance.append(i)

        return attendance

    def organize_data(self):
        """
        Pass of the data into a dictionary so later on I can convert into a JSON file
        """

        data = {"Teams" : self.get_teams(),
                "Attendance": self.get_attendance()}

        return data

def main():
    """
    The main method for running the whole class
    Will print out a json dictionary for the team names and Total Attendance
    """

    atteOBJ = attendance() #object
    data = atteOBJ.organizeData()

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

if __name__ == '__main__': main()