import os
import sys
from string import atoi
import pdb
from UserList import UserList

class Course:
	"""represents the course object that will be stored in the quarter object"""
	# name - string: course name
	# units - int: number of units
	# difficulty - int: difficuly of course
	# preReqs - list: list of the course's pre-requisite courses as strings
	# quartersOffered - list of the abbreviation of quarters offered
	# quarterTaken - quarter that the course is taken
	def __init__(self, name, units = 0, difficulty = 0, preReqs = [], quartersOffered = [], quarterTaken = None, yearTaken = None):
		"""inits a course object""" 
		self.name = name
		self.units = units	
		self.difficulty = float(difficulty)
		self.quartersOffered = quartersOffered
		self.quarterTaken = quarterTaken
		self.yearTaken = yearTaken
		self.preReqs = preReqs
		self.priority= 0

	def returnName(self):
		"""returns the course's name"""
		return self.name

	def returnDifficulty(self):
		""" returns course difficulty """ 
		return self.difficulty

	def returnUnits(self):
		"""returns the course's units"""
		return self.units
	
	def returnQuarter(self):
		"""returns the quarter in which the course was taken"""
		return self.quarterTaken

	def setQuarter(self, quarter):
		"""sets the quarter the course is taken"""
		self.quaterTaken = quarter

	def returnYear(self):
		"""returns the year the course was taken"""
		return self.yearTaken

	def setYear(self, year):
		"""sets the year the course is taken"""
		self.year = year

	def returnPreReqs(self):
		return self.preReqs
	
	def returnPriority(self):
		"""returns the course priority score"""
		return self.priority

	def setPriority(self, priority):
		"""sets the courses priority"""
		self.priority = priority

	def setQuarterTaken(self, quarter):
		"""sets the quarter taken 'A', 'W', 'Sp', 'S', 'None'"""
		self.quarterTaken = quarter
	
	def printCourse(self):
		""" prints a course object """
		print "course name = %s, units = %d, difficulty = %d, preReqs = %s quarters = %s priority = %d" % \
		(self.name, self.units, self.difficulty, self.preReqs, self.quartersOffered, self.priority) 	

class Quarter(UserList):
	"""represents the quarter object that will be stored in the schedule object"""
	# quarter - string: quarter name 'A', 'W', 'Sp', 'S'
	# year - int: year
	# courses - list: of courses as Course objects in quarter 
	def __init__(self, quarter, year, courses = [], currentDifficulty = 0):
		"""inits the quarter object"""
		UserList.__init__(self)
		self.quarter = quarter
		self.year = year
		
		# keeps track of the current difficulty of the quarter
		self.currentDifficulty = currentDifficulty
	
	def inQuarter(self, course):
		"""returns True if a course is a quarter and False if the course is not the quarter"""
		# course - Course: course  
		name = course.name.lower() 
		filteredList = filter(lambda x: name == x.name.lower(), self)
		return filteredList

	def addCourse(self, course):
		# course - Course: course
		"""adds a course to the quarter"""
		if not self.inQuarter(course):
			course.setQuarter(self.quarter)
			course.setYear(self.year)
			self.append(course)
			self.changeDifficulty(course.returnDifficulty())
			print "%s was added to %s quarter of %d" % (course.name, self.quarter, self.year)
		else:
			print "%s is already in %s quarter of %d. It was not added." % (course.name, self.quarter, self.year)
		
	def removeCourse(self, course):
		# course - Course: course
		"""removes a course from the quarter"""
		if self.inQuarter(course):
			course.setQuarter(None)
			course.setYear(None)
			self.remove(course)
			self.changeDifficulty(-1 * course.returnDifficulty())
			print "%s was removed from %s quarter of %d" % (course.name, self.quarter, self.year)
		else:
			print "%s is not in %s quarter of %d. It cannot be removed." % (course.name, self.quarter, self.year) 

	def changeDifficulty(self, update):
		"""change the difficulty of the quarter by adding an update"""
		self.currentDifficulty += update

	def returnDifficulty(self):
		return self.currentDifficulty

	def returnDifficulty(self):
		"""returns the quarter's difficulty"""
		return self.currentDifficulty
	
	def returnQuarter(self):
		"""returns the quarter's quarter 'A', 'W', 'Sp', 'S'"""
		return self.quarter

	def returnYear(self):
		"""returns the quarter's year"""
		return self.year	

	def printQuarter(self):
		"""prints the quarter object"""
		print "quarter = %s, year = %d, courses = %s, current difficulty = %g" % \
		(self.quarter, self.year, ", ".join(["%s" % (c.name) for c in self]), self.currentDifficulty)

class CourseList(UserList):
	"""defines a list of courses"""
	def __init__(self, fileName):
		"""inits the course list object"""
		UserList.__init__(self)
		self.file = fileName
		self.num = 0
		self.totalDifficulty = 0

	def parseCourse(self, line):
		"""parses line from file to create and return a course"""
		args = line.split()
		name = args[0]	
		quartersOffered = args[1].split(':')
		units = atoi(args[2])
		diff = atoi(args[3])
		preReqs = args[4].split(',')
		if preReqs[0].lower() == 'none':
			preReqs = []
		course = Course(name, units, diff, preReqs, quartersOffered)
		return course
	
	def loadCourses(self):
		"""loads the courses from the file to the course list"""
		fsock = open(self.file, 'r', 0)
		while (True):
			line = fsock.readline()
			if line == "": break
			course = self.parseCourse(line)
			self.append(course)
			self.totalDifficulty += course.returnDifficulty()
			self.num += 1
	
	def removeCourse(self, courseName):
		"""removes the specified course from the course list"""
		course = filter(lambda x: x.name.lower() == courseName.lower(), self)
		if course:
			self.totalDifficulty += 1 * course.returnDifficulty()
			self.num -= 1
			self.remove(course)

	def returnTotalDifficulty(self):
		"""returns the total difficulty of the courselist"""
		return self.totalDifficulty

	def returnNum(self):
		"""returns the number of courses in the course list"""
		return self.num

	def isPreReq(self, course1, course2):
		"""returns True if course1 is a preReq of course2"""
		return course1.returnName() in course2.returnPreReqs()
		
	def calculatePriority(self, course):
		"""recursively calculates the priority of a course"""
		priority = 0
		for c in self:
			if self.isPreReq(course, c):
				priority += 1
				priority += self.calculatePriority(c)
		return priority

	def setPriority(self):
		"""sets the priority of all the courses in the courselist"""
		for c in self: c.setPriority(self.calculatePriority(c))

	def sortCourses(self):
		"""sorts the courses in the course list, 
		by descending priority, ascending difficulty, ascending units """
		self.setPriority()
		self.sort(key = lambda x: (-x.returnPriority(), x.returnDifficulty(), x.returnUnits()))

	def printCourseList(self):
		print "..................................Printing Course List..............................."
		# print "CourseList: %s" % (", ".join(["%s" % (c.name) for c in self]))
		# print "total difficulty = %d" % self.totalDifficulty
		# verbose course list printing
		for c in self:
			c.printCourse() 		
		print "..................................Printed Course List................................."
	
class Schedule(UserList):
	"""the final object that represents a full 4 year schedule"""
	# numYears - number of years to plan for 
	# quartersNotUsed - string delimited by ':' indicating quarters not used
	# example '{S : [1, 2, 3, 4]}' - all summer quarters aren't used  
	# coursesTakeFileName - file name of courses taken
	# courseList - list of all courses to be taken
	# current 
	def __init__(self, numYears, quartersNotUsed, coursesTakenFileName, courseList, currentQuarter):
		"""inits the parameters and objects in the schedule object"""
		UserList.__init__(self)
		self.numYears = numYears
		self.quartersNotUsed = quartersNotUsed

		# A - Autumn/Fall, W - Winter, Sp - Spring S - Summer
		self.quarters = quarterAbbrev = ['A', 'W', 'Sp', 'S']
		
		# keeps track of courses added to the schedule
		self.coursesTaken = []

		# the list of courses to be assigned to the quarters
		self.courseList = courseList

		# file name of courses taken so that they can be loaded into  their respective quarters
		self.coursesTakenFileName = coursesTakenFileName
		
		# sets the total difficulty
		self.totalDifficulty = courseList.returnTotalDifficulty()

		# inits the difficulty upper bound
		self.difficultyUpperBound = float(courseList.returnTotalDifficulty()/courseList.returnNum())

		# quarter to start planning {quarter : q, year : y}
		self.start = currentQuarter
	
	def quarterIsNotUsed(self, q, i):
		"""takes in a quarter and a year and determines if that quarter is not used"""
		if q in self.quartersNotUsed:
			if i + 1 in self.quartersNotUsed[q]:
				return True
		return False 
	
	def loadQuarters(self):
		"""loads the quarters that shall be used in course scheduling"""
		for i in range(0, self.numYears):
			for q in self.quarters: 
				if not self.quarterIsNotUsed(q, i):
					quarter = Quarter(q, i + 1)
					self.append(quarter)	
	
	def changeDifficultyUpperBound(self, update):
		"""changes difficulty upper bound by adding the update"""
		self.difficultyUpperBound += update
	
	def parseCourse(self, line):
		"""parse course already taken"""
		args = line.split()
		name = args[0]
		year = atoi(args[1])
		quarter = args[2]
		diff = args[3]
		course = Course(name, difficulty = diff, quarterTaken = quarter, yearTaken = year)
		return course

	def findQuarter(self, quarter, year):
		"""find quarter course should be assigned to"""
		quarter = filter(lambda q: q.returnYear() == year and q.returnQuarter() == quarter, self)
		if quarter:
			return quarter[0]
		return None

	def addCourse(self, course):
		"""adds course to schedule"""
		quarter = self.findQuarter(course.returnQuarter(), course.returnYear())
		if quarter != None:
			quarter.addCourse(course)
			self.coursesTaken.append(course)	
		else:
			print 'The quarter was not found and %s was not added' % (course.name)

	def isCourseTaken(self, name):
		"""returns True if the course is taken"""
		course = filter(lambda c: c.returnName().lower() == name, self.coursesTaken)
		if course:
			return True
		return False

	def loadClassesAlreadyTaken(self):
		"""loads courses that have already been taken into the schedule"""
		fsock = open(self.coursesTakenFileName, 'r', 0)
		while (True):
			line = fsock.readline()
			if line == "": break
			course = self.parseCourse(line)
			self.addCourse(course)

	def returnIndexOfQuartersToPlan(self):
		"""returns the index of the list of quarters in which planning will be done"""
		year = self.start['year']
		quarter = self.start['quarter']
		for i in range(0, len(self)):
			if self[i].returnYear() == year and self[i].returnQuarter() == quarter: 
				return i

	def preReqTaken(self, course):
		"""returns true if the courses' preReq's have been taken"""
		pass
	
	def priorityBasedScheduling(self, indexFirstQuarter):
		"""algorithm that shedules courses whose priorities > 0"""
		pass

	def difficultyBasedScheduling(self, indexFirstQuarter):
		"""algorithm that places the courses in the least difficult quarter"""
		pass
			
	def runAlgo(self):
		"""runs the course scheduling algorithm"""
		indexFirstQuarter = self.returnIndexOfQuartersToPlan()
		self.difficultyUpperBound = self.totalDifficulty/(len(self) - indexFirstQuarter)
		print "This is the initial difficulty bound %f" % self.difficultyUpperBound 
		self.priorityBasedScheduling(indexFirstQuarter)

	def printSchedule(self):
		"""prints the course schedule"""
		print "----------------------------------Printing Schedule----------------------------------------"
		for quarter in self:
			quarter.printQuarter()
		print "----------------------------------Printed Schedule------------------------------------------"

def createCourseList(coursesToTakeFileName):
	"""returns the course list to be used in the schedule"""
	courseList = CourseList(coursesToTakeFileName)
	courseList.loadCourses()
	courseList.sortCourses()
	courseList.printCourseList()
	return courseList

def setupSchedule(numYears, quartersNotUsed, coursesTakenFileName, courseList, start):
	"""returns the schedule ready to be worked on by the algorithm"""
	schedule = Schedule(numYears, quartersNotUsed, coursesTakenFileName, courseList, start)
	schedule.loadQuarters()
	schedule.loadClassesAlreadyTaken()
	print "----------------------------------Printing Initial Schedule----------------------------------"
	schedule.printSchedule()
	print "----------------------------------Printed Original Schedule----------------------------------"	
	return schedule	

def test(coursesToTakeFileName, coursesTakenFileName):
	courseList = createCourseList(coursesToTakeFileName)
	schedule = setupSchedule(4 , {'S': [1, 2, 3, 4]}, coursesTakenFileName, courseList, {'quarter': 'W', 'year': 3})
	schedule.runAlgo()

def main(argv):
	test(argv[0], argv[1])
	print "SCHEDULING DONE"
	print "----------------------------------------------------------------------------------------------------------------------------"

if __name__ == "__main__":
	main(sys.argv[1:])
