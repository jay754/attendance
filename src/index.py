from bs4 import BeautifulSoup as bs
import urllib2
import requests

try:
    import json
except ImportError:
    import simplejson as json

#total attedance class for NBA 2014

class Attendance:

    def __init__(self):
        self.url = "http://espn.go.com/nba/attendance/_/year/2013"
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
            return http_status
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

        nums = []

        for i in self.getData():
            j = i.replace(" ", "")
            if j.isalpha():
                pass
        else:
            nums.append(j)

        return nums

    def get_teams(self):
        """
        Returns all the teams in order from the most fans that attenended the games
        This is method was a little broken had to manually insert 76ers into the array
        """

        names = []

        for i in self.getData():
            j = i.replace(" ", "")
            if j.isalpha():
                names.append(j)

        names.insert(16, "76ers")

        return names

    def sanitize_data(self):
        """
        Had to sanitize the numbers, because all of them contained commas, and decimals.
        You have to do this in order to convert from a String to an Integer
        """

        attendance = []

        for i in self.getOnlyNums():
            striped_comma = i.replace(",", "")
            striped_decimal = striped_comma.replace(".", "")
            attendance.append(striped_decimal)

        return attendance

    def get_attendance(self):
        """
        Gets the total attendance for each team
        """

        attendance = []

        for i in self.sanitizeData():
            if i is not "76ers":
                if int(i) > 500000:
                    attendance.append(i)

        return attendance

    def organizeData(self):
        """
        Pass of the data into a dictionary so later on I can convert into a JSON file
        """

        data = {"Teams" : self.getTeams(),
                "Attendance": self.getAttendance()}

        return data

# def main():
#     """
#     The main method for running the whole class
#     Will print out a json dictionary for the team names and Total Attendance
#     """

#     atteOBJ = attendance() #object
#     data = atteOBJ.organizeData() #the dictionary data

#     with open('data.json', 'w') as outfile:
#         json.dump(data, outfile)

if __name__ == '__main__':
    attaOBJ = Attendance()
    print attaOBJ.check_request("http://espn.go.com/nba/attendance/_/year/2013")
    print attaOBJ.get_data()