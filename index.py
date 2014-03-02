from bs4 import BeautifulSoup as bs
import urllib2

try:
    import json
except ImportError:
    import simplejson as json

#total attedance class

class attendance:

	def __init__(self):
		self.url = "http://espn.go.com/nba/attendance/_/year/2013"

	def getUrl(self):
		return self.url

	def getData(self):
		results = urllib2.urlopen(self.url)
		soup = bs(results)
		data = [str(i.get_text()) for i in soup.find_all("td")]
		actual_data = data[17:]

		return actual_data

	def getOnlyNums(self):
		nums = []

		for i in self.getData():
			
			j = i.replace(" ", "")

			if j.isalpha():
				pass
			else:
				nums.append(j)

		return nums

	def getTeams(self):
		names = []

		for i in self.getData():
			j = i.replace(" ", "")
			if j.isalpha():
				names.append(j)

		names.insert(16, "76ers")

		return names

	def sanitizeData(self):
		attendance = []

		for i in self.getOnlyNums():
			striped_comma = i.replace(",", "")
			striped_decimal = striped_comma.replace(".", "")
			attendance.append(striped_decimal)

		return attendance

	def getAttendance(self):
		attendance = []

		for i in self.sanitizeData():
			if i != "76ers":
				if int(i) > 500000:
					attendance.append(i)

		return attendance

	def organizeData(self):

		data = {
				"Teams" : self.getTeams(),
				"Attendance": self.getAttendance()
				}

		return data

#end of the main class

def main():
	atteOBJ = attendance()
	data = atteOBJ.organizeData()
	#json_data = ""

	#json_data += "{"

	#print data["Teams"]

	'''for i in data["Teams"]:
		json_data += "Team:" + i + "\n"

	for i in data["Attendance"]:
		json_data += "Attendance:" + i + "\n"'''

	#json_data += "}"

	#str(json_data)
	with open('data.json', 'w') as outfile:
  		json.dump(data, outfile)
if __name__ == '__main__':
	main()