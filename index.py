from bs4 import BeautifulSoup as bs
import urllib2

try:
    import json
except ImportError:
    import simplejson as json

#total attedance class for NBA 2014

class attendance:

	def __init__(self):
		self.url = "http://espn.go.com/nba/attendance/_/year/2013"

	def getUrl(self):
		"""
		
		A setter for thr url
		
		"""

		return self.url

	def getData(self):
		"""

		Getting the Actual Data from the Espn Url

		"""
		
		results = urllib2.urlopen(self.url)
		soup = bs(results)
		data = [str(i.get_text()) for i in soup.find_all("td")]
		actual_data = data[17:] #everything before the 17th element is useless data

		return actual_data

	def getOnlyNums(self):
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

	def getTeams(self):
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

	def sanitizeData(self):
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

	def getAttendance(self):
		"""

		Get the total attendance for each team

		"""

		attendance = []

		for i in self.sanitizeData():
			if i != "76ers":
				if int(i) > 500000:
					attendance.append(i)

		return attendance

	def organizeData(self):
		"""

		Pass of the data into a dictionary so later on I can convert into a JSON file

		"""

		data = {
				"Teams" : self.getTeams(),
				"Attendance": self.getAttendance()
				}

		return data

#end of the main class

def main():
	"""

	The main method for running the whole class
	Will print out a json dictionary for the team names and Total Attendance

	"""

	atteOBJ = attendance() #object
	data = atteOBJ.organizeData() #the dictionary data
	
	with open('data.json', 'w') as outfile:
  		json.dump(data, outfile)

if __name__ == '__main__':
	main()