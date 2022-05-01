from django.shortcuts import render
from django.http import HttpResponse, Http404
from .db_utils import run_statement
from .forms import *
import hashlib



# Create your views here.


# starting page of the system. every user will be directed here so that s/he can login 
def index(request):

	if request.session:
		request.session.flush()

	isFailed=request.GET.get("fail",False)
	loginForm=UserLoginForm()
	context = {
		'login_form' : loginForm,
	}

	return render(request, 'webapi/index.html', context)


### LOGIN CHECKS AND RESULTS WILL BE HANDLED:

# check whether the given parameters match an admin in the system and welcome the admin and show what s/he can do
def adminLogin(request):
	username = request.POST.get('username', False)
	password = request.POST.get('password', False)

	psw = hashlib.sha256(password.encode('utf-8')).hexdigest() # passwords will be hold as encoded

	# get rows whose username and password are the same as input taken  index page. since username is PK, this query will return at most 1 instance 
	result = run_statement(f"SELECT username FROM databasemanager WHERE username='{username}' AND password='{psw}';") 
																													


	# create admin forms to send the frontend
	add_student = addStudentForm()
	add_instructor = addInstructorForm()
	student = studentForm()
	update_title = updateTitleForm()
	courses_of_instructor = coursesOfInstructorForm()
	average_grade = averageGradeForm()

	# create a dictionary for all forms used in adminHomePage with correct keys
	context = {
		'add_student_form': add_student,
		'add_instructor_form': add_instructor,
		'delete_student_form': student,
		'update_title_form':update_title,
		'grades_of_student_form': student,
		'courses_of_instructor_form': courses_of_instructor,
		'average_grade_form': average_grade,
	}


	if result[0][0]==username: # if we have user with that username and password, operation options will not be shown otherwise
		return render(request, 'webapi/adminHomePage.html', context)
	else: 
		return render(request, 'webapi/adminOperationFail.html')


# check whether the given parameters match an instructor in the system and welcome the instructor and show what s/he can do
def instructorLogin(request):
	username = request.POST.get("username", False)
	password = request.POST.get("password", False)
	psw = hashlib.sha256(password.encode("utf-8")).hexdigest() #passwords will be hold as encoded

	# get rows whose username and password are the same as input taken  index page. since username is PK, this query will return at most 1 instance 
	result = run_statement(f"SELECT username FROM instructor WHERE username='{username}' AND password='{psw}';")

	# create instructor forms to send the frontend
	available_classroom = availableClassroomsForm()
	add_course = openCourseForm()
	add_prereq = addPrereqForm()
	view_enrolled = viewEnrolledStudentsForm()
	update_coursename = updateCourseNameForm()
	grade_student = gradeStudentForm()

	# create a dictionary for all forms used in adminHomePage with correct keys
	context = {
		'available_classrooms_form':available_classroom,
		'open_course_form':add_course,
		'add_prereq_form':add_prereq,
		'enrolled_students_form':view_enrolled,
		'update_course_name_form':update_coursename,
		'grade_student_form':grade_student,
		'username':username,
		'password':psw,
	}

	if result[0][0]==username: # if we have a user with that username and password, operation options will not be shown otherwise
		return render(request, "webapi/instructorHomePage.html", context)
	else:
		return HttpResponseRedirect(reverse('webapi:index'))


# check whether the given parameters match an student in the system and welcome the student and show what s/he can do
def studentLogin(request):
	username = request.POST.get("username", False)
	password = request.POST.get("password", False)
	psw = hashlib.sha256(password.encode("utf-8")).hexdigest() # passwords will be hold as encoded

	# get rows whose username and password are the same as input taken  index page. since username is PK, this query will return at most 1 instance 
	result = run_statement(f"SELECT username, studentId FROM student WHERE username='{username}' AND password='{psw}';")

	# create student forms to send the frontend
	add_course = addCourseForm()
	find_courses_keyword = findCoursesKeywordForm()
	filter_courses = filterCoursesForm()

	if result[0][0]==username: # if we have a user with that username and password, operation options will not be shown otherwise
		# create a dictionary for all forms used in adminHomePage with correct keys
		context	= {
			'student_id':result[0][1],
			'results':result,
			'add_course_form':add_course,
			'find_courses_keyword_form':find_courses_keyword,
			'filter_courses_form': filter_courses,
		}

		return render(request, "webapi/studentHomePage.html", context)
	else:
		return render(request, "webapi/adminOperationFail.html")



### ADMIN OPERATIONS WILL BE HANDLED


# adds a student to the database if everything is correct
def addStudent(request):
	
	# take parameters taken in the adminHomePage in order to create a student record in the system	
	username = request.POST.get('username', False)
	password = request.POST.get('password', False)
	name = request.POST.get('name', False)
	surname = request.POST.get('surname', False)
	email = request.POST.get('email', False)
	courses = request.POST.get('courses', False)
	student_id = request.POST.get('student_id', False)
	gpa = request.POST.get('gpa', False)
	completed_credits = request.POST.get('completed_credits', False)
	department_id = request.POST.get('department_id', False)


	psw = hashlib.sha256(password.encode('utf-8')).hexdigest() # passwords will be hold as encoded

	try: # if the query throws an exception, the user will be warned in a way that will not scare him/her

		# since we are creating a record for a student, "insert"ion is done. the order of the given values should be the same as the order that rows are hold.
		result = run_statement(f"INSERT INTO student VALUES ('{username}', '{psw}', '{name}', '{email}', '{surname}', '{department_id}', {student_id}, {completed_credits}, {gpa});")
		return render(request, 'webapi/adminOperationSuccessful.html')

	except:
		return render(request, "webapi/adminOperationFail.html")


# adds an instructor to the database if everything is correct
def addInstructor(request):

	# take parameters taken in the adminHomePage in order to create an instructor record in the system	
	username = request.POST.get('username', False)
	password = request.POST.get('password', False)
	name = request.POST.get('name', False)
	surname = request.POST.get('surname', False)
	email = request.POST.get('email', False)
	department_id = request.POST.get('department_id', False)
	title = request.POST.get('title', False)

	psw = hashlib.sha256(password.encode('utf-8')).hexdigest() # passwords will be hold as encoded

	try: # if the query throws an exception, the user will be warned in a way that will not scare him/her

		# since we are creating a record for an instructor, "insert"ion is done. the order of the given values should be the same as the order that rows are hold.
		result = run_statement(f"INSERT INTO instructor VALUES ('{username}', '{psw}', '{name}', '{email}', '{surname}', '{department_id}', '{title}');")
		return render(request, "webapi/adminOperationSuccessful.html")
	except:
		return HttpResponse()


# deletes a record of student if there is one with the given student id
def deleteStudent(request):
	# take parameters put in the adminHomePage in order to delete a student record in the system	
	student_id = request.POST.get('student_id', False)

	try: # if the query throws an exception, the user will be warned in a way that will not scare him/her

		# delete the record that has the student_id the same as the given one, since studentId is PK, this query will return at most 1 instance
		result = run_statement(f"DELETE FROM student WHERE studentId='{student_id}';")
		return render(request, "webapi/adminOperationSuccessful.html")
	except:
		return render(request, "webapi/adminOperationFail.html")


# update the title column of the record of an instructor if there is one with the given username  
def updateTitle(request):
	# take parameters put in the adminHomePage in order to update the title of the instructor 	
	username = request.POST.get("username", False)
	new_title = request.POST.get("new_title", False)

	try: # if the query throws an exception, the user will be warned in a way that will not scare him/her

		# since only one column will be changed and operation will be done with an existing record, "update" is the correct operation
		result = run_statement(f"UPDATE instructor SET title='{new_title}' WHERE username='{username}';")
		return render(request, "webapi/adminOperationSuccessful.html")
	except:
		return render(request, "webapi/adminOperationFail.html")


# view all students in the database
def viewStudents(request):
	# the html page that will be called shows the result in table form and needs the headers of the columns
	attrs = ["username", "name", "surname", "email", "department", "completed_credits", "gpa"]
	try: # if the query throws an exception, the user will be warned in a way that will not scare him/her

		# select all necessary columns from student table, with no condition since admin wants to see all students
		result = run_statement(f"SELECT username, name, surname, email, departmentId, completedCredits, gpa FROM student ORDER BY completedCredits ASC;")

		# create a dictionary for headers and result that will be passed to the html page
		context = {
			'attrs': attrs,
			'results': result,
		}

		return render(request, "webapi/viewUsers.html", context)
	except:
		return render(request, "webapi/adminOperationFail.html")

# view all instructors in the database
def viewInstructors(request):
	# the html page that will be called shows the result in table form and needs the headers of the columns
	attrs = ["username", "name", "surname", "email", "department", "title"]
	try: # if the query throws an exception, the user will be warned in a way that will not scare him/her

		# select all necessary columns from instructor table, with no condition since admin wants to see all instructors
		result = run_statement(f"SELECT username, name, surname, email, departmentId, title FROM instructor;")

		# create a dictionary for headers and result that will be passed to the html page
		context = {
			'attrs': attrs,
			'results': result,
		}

		return render(request, "webapi/viewUsers.html", context)
	except:
		return render(request, "webapi/adminOperationFail.html")



# view grade records of a specific student
def viewGradesOfStudent(request):
	# the html page that will be called shows the result in table form and needs the headers of the columns
	attrs = ["course_id", "course_name", "grade"]

	# take parameters put in the adminHomePage in order to see grades of a student
	student_id = request.POST.get('student_id', False)
	try: # if the query throws an exception, the user will be warned in a way that will not scare him/her

		# select all records in the graded table that points to the given student. since the courses that student is taking are hold in graded table also, the records that has null value in
		# the table should be eliminated
		result = run_statement(f"SELECT graded.courseId, course.name, grade FROM graded INNER JOIN course ON graded.courseId=course.courseId WHERE grade IS NOT NULL;")

		# create a dictionary for headers and result that will be passed to the html page
		context = {
			'attrs': attrs,
			'results': result,
		}

		return render(request, "webapi/viewUsers.html", context)

	except:
		return render(request, "webapi/adminOperationFail.html")


# view courses of an instructor
def viewCoursesOfInstructor(request):
	# the html page that will be called shows the result in table form and needs the headers of the columns
	attrs = ["course_id", "course_name", "classroom_id", "campus", "time_slot"]

	# take parameters put in the adminHomePage in order to see courses of an instructor
	inst = request.POST.get("username", False)
	try: # if the query throws an exception, the user will be warned in a way that will not scare him/her

		# select all records in the course table whose instructor matches with the input.
		# since the table will show where and at which classroom the course is given: join givenin table on the condition of matching course ids with the course table
		# since the table will show at which campus the course is given: join classroom table on the condition of matching classroom ids with the givenin table
		result = run_statement(f"SELECT course.courseId, course.name, givenin.classroomId, campus, timeSlot FROM course LEFT JOIN givenin ON course.courseId=givenin.courseId INNER JOIN classroom ON givenin.classroomId=classroom.classroomId WHERE course.instructor='{inst}';")

		# create a dictionary for headers and result that will be passed to the html page
		context = {
			'attrs': attrs,
			'results': result,
		}
		return render(request, "webapi/viewUsers.html", context)
	except:
		return render(request, "webapi/adminOperationFail.html")


# view average of grade of a specific course
def viewCourseAverage(request):
	# the html page that will be called shows the result in table form and needs the headers of the columns
	attrs = ["course_id", "course_name", "grade_average"]

	# take parameters put in the adminHomePage in order to see the average grade of a course
	course = request.POST.get("course_id", False)

	try: # if the query throws an exception, the user will be warned in a way that will not scare him/her

		# select average of grade values in the graded table that is created for a specific course. since some records will have null value, implying that that student has not been graded
		# yet, those records should be discarded.
		result = run_statement(f"SELECT graded.courseId, course.name, avg(graded.grade) FROM graded INNER JOIN course ON course.courseId=graded.courseId WHERE graded.courseId='{course}' AND grade IS NOT NULL;")

		# create a dictionary for headers and result that will be passed to the html page
		context = {
			'attrs': attrs,
			'results':result,
		}

		return render(request, "webapi/viewUsers.html", context)
	except:
		return render(request, "webapi/adminOperationFail.html")



### INSTRUCTOR OPERATIONS WILL BE HANDLED


# list classrooms where there is no lecture at a given time slot
def listAvailableClassrooms(request):
	# the html page that will be called shows the result in table form and needs the headers of the columns
	attrs = ["classroom_id", "campus", "classroom_capacity"]

	# take parameters put in the instructorHomePage in order to see available classrooms
	time_slot = request.POST.get("time_slot", False)

	try: # if the query throws an exception, the user will be warned in a way that will not scare him/her

		# select classroom records whose classroomId attribute is not placed in a record in the givenin table for a given time slot value
		result = run_statement(f"SELECT classroomId, campus, capacity FROM classroom WHERE classroomId NOT IN (SELECT classroomId FROM givenin WHERE timeSlot={time_slot});")
		
		# create a dictionary for headers and result that will be passed to the html page
		context = {
			'attrs': attrs,
			'results':result,
		}

		return render(request, "webapi/viewUsers.html", context)
	except:
		return render(request, "webapi/adminOperationFail.html")


# open a course with necessary information
def openCourse(request):
	# take parameters put in the instructorHomePage in order to open a new course
	course_id = request.POST.get("course_id", False)
	course_name = request.POST.get("name", False)
	credits = request.POST.get("credits", False)
	classroom_id = request.POST.get("classroom_id", False)
	time_slot = request.POST.get("time_slot", False)
	quota = request.POST.get("quota", False)
	username = request.POST.get("username", False)

	# check whether given quota for the course exceeds the capacity of the specified classroom 
	capacity = int(run_statement(f"SELECT capacity FROM classroom WHERE classroomId={classroom_id};")[0][0]) >= int(quota)
	# check whether this classroom holds a lecture at the wanted time slot
	available = len(run_statement(f"SELECT classroomId FROM givenin WHERE classroomId={classroom_id} AND timeSlot={time_slot};")) == 0

	if capacity and available: # both conditions must be hold
		try: # if the query throws an exception, the user will be warned in a way that will not scare him/her

			# create a record in both course and givenin tables. 
			run_statement(f"INSERT INTO course VALUES ('{course_name}', '{course_id}', {credits}, {quota}, '{username}');\nINSERT INTO givenin VALUES ({classroom_id}, '{course_id}', {time_slot});")

			return render(request, "webapi/adminOperationSuccessful.html")

		except:
			return render(request, "webapi/adminOperationFail.html")
	else:
		return render(request, "webapi/adminOperationFail.html")


# add a prerequisite condition between two classes
def addPrereq(request):
	# take parameters put in the instructorHomePage in order to create a prerequisite condition
	preceding = request.POST.get("preceding_course", False)
	following = request.POST.get("following_course", False)

	try: # if the query throws an exception, the user will be warned in a way that will not scare him/her

		# create a new record in the prereq table
		run_statement(f"INSERT INTO prereq VALUES('{preceding}', '{following}');")
		return render(request, "webapi/adminOperationSuccessful.html")
	except:
		return render(request, "webapi/adminOperationFail.html")


# view your active courses
def viewGivenCourses(request):
	# the html page that will be called shows the result in table form and needs the headers of the columns
	attrs = ["course_id", "course_name", "classroom_id", "time_slot", "quota", "prerequisites"]
	# take parameters put in the instructorHomePage in order to view courses
	username = request.POST.get("username", False)

	# first, find courses given by this instructor.
	course_ids = run_statement(f"SELECT courseId FROM course WHERE instructor='{username}' ORDER BY courseId ASC;")
	prereqs = []
	# second, find all prerequisites for all courses you find in the first step
	for c_id in course_ids:
		# find prerequisites for every course and gather those in a string
		precedings = run_statement(f"SELECT precedingCourse FROM prereq WHERE followingCourse='{c_id[0]}'")
		temp_result = ""
		
		for prereq in precedings:
			temp_result += prereq[0] + ","
		if len(temp_result)!=0:
			temp_result = temp_result[:-1]

		prereqs.append(temp_result)

	try: # if the query throws an exception, the user will be warned in a way that will not scare him/her

		# select course records whose instructor field is the same as our logged-in instructor and whose courseId value finds itself a place in givenin table 
		result = run_statement(f"SELECT course.courseId, course.name, classroomId, timeSlot, quota FROM course INNER JOIN givenin ON givenin.courseId=course.courseId WHERE instructor='{username}' ORDER BY courseId ASC;")
		# normally, result comes as a tuple of tuples. in order to make additions in the tuples inside result, it should be casted as a list
		result = list(result)

		# add prerequisite strings you created above to the tuples one by one
		for i in range(len(result)):
			t = tuple([prereqs[i]])
			result[i] += t

		# create a dictionary for headers and result that will be passed to the html page
		context = {
			'attrs':attrs,
			'results':result,
		}
		return render(request, "webapi/viewUsers.html", context)
	except:
		return render(request, "webapi/adminOperationFail.html")


# view enrolled students for one of your courses
def viewEnrolledStudents(request):
	# the html page that will be called shows the result in table form and needs the headers of the columns
	attrs = ["username", "student_id", "email", "name", "surname"]

	# take parameters put in the instructorHomePage in order to view courses
	course_id = request.POST.get("course_id", False)
	username = request.POST.get("username", False)

	try: # if the query throws an exception, the user will be warned in a way that will not scare him/her

		# select student records whose studentId column is in the list of studentIds of the graded columns where givenin.courseId is the specified courseId and grade is null(if grade is 
		# not null, that means the student passed the course, not enrolled anymore)
		result = run_statement(f"SELECT username, studentId, email, name, surname FROM student WHERE studentId IN (SELECT studentId FROM graded INNER JOIN course ON instructor='{username}' AND course.courseId='{course_id}' WHERE graded.courseId='{course_id}' AND grade IS NULL);")

		# create a dictionary for headers and result that will be passed to the html page
		context = {
			'attrs':attrs,
			'results':result,
		}

		return render(request, "webapi/viewUsers.html", context)
	except:
		return render(request, "webapi/adminOperationFail.html")


# update the name of the one of your courses
def updateCourseName(request):
	# take parameters put in the instructorHomePage in order to update the name of the course
	course_id = request.POST.get("course_id", False)
	new_name = request.POST.get("new_name", False)
	username = request.POST.get("username", False)

	try: # if the query throws an exception, the user will be warned in a way that will not scare him/her

		# update the course record whose courseId is the courseId instructor gave and check whether this course is given by the logged-in instructor.
		run_statement(f"UPDATE course SET name='{new_name}' WHERE courseId='{course_id}' AND instructor='{username}';")
		return render(request, "webapi/adminOperationSuccessful.html")
	except:
		return render(request, "webapi/adminOperationFail.html")


# give a grade to a given student for a given course
def gradeStudent(request):
	# take parameters put in the instructorHomePage in order to update the name of the course
	student_id = request.POST.get("student_id", False)
	course_id = request.POST.get("course_id", False)
	grade = request.POST.get("grade", False)
	username = request.POST.get("username", False)

	# check whether the course is given by the logged-in instructor
	inst = run_statement(f"SELECT instructor FROM course WHERE courseId='{course_id}' AND instructor='{username}';")

	if len(inst)!=0:
		try: # if the query throws an exception, the user will be warned in a way that will not scare him/her

			# update graded and student tables accordingly
			run_statement(f"UPDATE graded SET grade={grade} WHERE studentId={student_id} AND courseId='{course_id}';\nUPDATE student INNER JOIN course ON courseId='{course_id}' SET gpa=(gpa*completedCredits+{grade}*credits)/(completedCredits+credits), completedCredits=completedCredits+credits;")
			return render(request, "webapi/adminOperationSuccessful.html")
		except:
			return render(request, "webapi/adminOperationFail.html")
	else:
		return render(request, "webapi/adminOperationFail.html")




### STUDENT OPERATIONS WILL BE HANDLED


# see all courses in the database
def seeCourses(request):
	# the html page that will be called shows the result in table form and needs the headers of the columns
	attrs = ["course_id", "course_name", "instructor_surname", "department_id", "credits", "classroom_id", "time_slot", "quota", "prerequisites"]

	# first, find courses given by this instructor.
	course_ids = run_statement(f"SELECT courseId FROM course WHERE instructor='{username}' ORDER BY courseId ASC;")
	prereqs = []
	# second, find all prerequisites for all courses you find in the first step
	for c_id in course_ids:
		# find prerequisites for every course and gather those in a string
		precedings = run_statement(f"SELECT precedingCourse FROM prereq WHERE followingCourse='{c_id[0]}'")
		temp_result = ""
		
		for prereq in precedings:
			temp_result += prereq[0] + ","
		if len(temp_result)!=0:
			temp_result = temp_result[:-1]

		prereqs.append(temp_result)

	try: # if the query throws an exception, the user will be warned in a way that will not scare him/her

		# select all courses in the course table.
		# inner join givenin on the same courseId for the time slot
		# inner join instructor on the same username for the surname and department 
		result = run_statement(f"SELECT course.courseId, course.name, instructor.surname, instructor.departmentId, credits, givenin.classroomId, givenin.timeSlot, quota FROM course INNER JOIN givenin ON course.courseId=givenin.courseId INNER JOIN instructor ON username=course.instructor;")
		# normally, result comes as a tuple of tuples. in order to make additions in the tuples inside result, it should be casted as a list
		result = list(result)

		# add prerequisite strings you created above to the tuples one by one
		for i in range(len(result)):
			t = tuple([prereqs[i]])
			result[i] += t

		# create a dictionary for headers and result that will be passed to the html page
		context = {
			'attrs':attrs,
			'results':result,
		}
		return render(request, "webapi/viewUsers.html", context)
	except:
		return render(request, "webapi/adminOperationFail.html")


# take a new course
def addCourse(request):
	# take parameters put in the studentHomePage in order to take a new course
	course_id = request.POST.get("course_id", False)
	student_id = request.POST.get("student_id", False)

	# find the number of students who are taking this course currently
	taken_by = run_statement(f"SELECT count(studentId) FROM graded WHERE courseId='{course_id}' AND grade IS NULL;")
	# check whether there is place in the course so that the logged-in student can add the course
	is_avail = run_statement(f"SELECT quota from course WHERE courseId='{course_id}';")[0][0] > taken_by[0][0]
	# check if the logged-in student had taken the all of the prerequisite courses
	is_ready = run_statement(f"SELECT {student_id} IN (SELECT S.studentId FROM student S WHERE NOT EXISTS(SELECT precedingCourse FROM prereq WHERE followingCourse='{course_id}' AND precedingCourse NOT IN (SELECT G.courseId FROM graded G WHERE G.studentId=S.studentId)));")[0][0] == 1


	if is_avail and is_ready:
		try: # if the query throws an exception, the user will be warned in a way that will not scare him/her

			# create a record in the graded table, grade is null since that means that the student is taking the course right now
			run_statement(f"INSERT INTO graded VALUES ({student_id}, '{course_id}', NULL);")
			return render(request, "webapi/adminOperationSuccessful.html")
		except:
			return render(request, "webapi/adminOperationFail.html")
	else:
		return render(request, "webapi/adminOperationFail.html")


# see all courses you took and are taking
def courseHistory(request):
	# the html page that will be called shows the result in table form and needs the headers of the columns
	attrs = ["course_id", "course_name", "grade"]
	# take parameters put in the studentHomePage in order to see course history
	student_id = request.POST.get("student_id", False)

	try: # if the query throws an exception, the user will be warned in a way that will not scare him/her

		# select all graded records whose studentId is the same as the logged-in student's studentId
		result = run_statement(f"SELECT graded.courseId, course.name, grade FROM graded INNER JOIN course ON course.courseId=graded.courseId WHERE studentId={student_id};")

		# create a dictionary for headers and result that will be passed to the html page
		context = {
			'attrs':attrs,
			'results':result,
		}

		return render(request, "webapi/viewUsers.html", context)
	except:
		return render(request, "webapi/adminOperationFail.html")


# find courses whose name includes the given keyword
def findCoursesByKeyword(request):
	# the html page that will be called shows the result in table form and needs the headers of the columns
	attrs = ["course_id", "course_name", "instructor_surname", "department_id", "credits", "classroom_id", "time_slot", "quota", "prerequisites"]
	# take parameters put in the studentHomePage in order to find courses by a keyword
	student_id = request.POST.get("student_id", False)
	keyword = request.POST.get("keyword", False)

	try: # if the query throws an exception, the user will be warned in a way that will not scare him/her

		#first, find the courses whose name is "like" the keyword. after this statement, prerequisites are still on table and they should be retrieved, too.
		result_without_prereqs = run_statement(f"SELECT course.courseId, course.name, surname, departmentId, credits, classroomId, timeSlot, quota FROM course INNER JOIN givenin ON givenin.courseId=course.courseId INNER JOIN instructor ON course.instructor=instructor.username WHERE course.name LIKE '%{keyword}%';")

		# find all prerequisites for all courses you find above
		prereqs = []
		for i in range(len(result_without_prereqs)):
			# take the first element of every tuple in the outer tuple. that will give the course id.
			c_id = result_without_prereqs[i][0]

			# find the prerequisites for the course whose id is the value you found above
			precedings = run_statement(f"SELECT precedingCourse FROM prereq WHERE followingCourse='{c_id}'")

			# gather all prerequisites in a string
			temp_result = ""			
			for prereq in precedings:
				temp_result += prereq[0] + ","
			if len(temp_result)!=0:
				temp_result = temp_result[:-1]

			prereqs.append(temp_result)


		# normally, result_without_prereqs comes as a tuple of tuples. in order to make additions in the tuples inside resulwithout_prereqs, it should be casted as a list
		result = list(result_without_prereqs)
		for i in range(len(result)):
			t = tuple([prereqs[i]])
			result[i] += t

		# create a dictionary for headers and result that will be passed to the html page
		context = {
			'attrs':attrs,
			'results':result,
		}

		return render(request, "webapi/viewUsers.html", context)

	except:
		return render(request, "webapi/adminOperationSuccessful.html")



def filterCourses(request):
	# the html page that will be called shows the result in table form and needs the headers of the columns
	attrs = ["course_id", "course_name", "instructor_surname", "department_id", "credits", "classroom_id", "campus", "time_slot", "quota"]
	# take parameters put in the studentHomePage in order to filter courses
	min_credits = request.POST.get("min_credits", False)
	max_credits = request.POST.get("max_credits", False)
	department = request.POST.get("department_id", False)
	campus = request.POST.get("campus", False)
	
	try: # if the query throws an exception, the user will be warned in a way that will not scare him/her

		# call the stored procedure you created in the database
		result = run_statement(f"CALL filterCourses({min_credits}, {max_credits}, '{department}', '{campus}');");

		# create a dictionary for headers and result that will be passed to the html page
		context = {
			'attrs': attrs,
			'results': result
		}

		return render(request, "webapi/viewUsers.html", context)
	except:
		return render(request, "webapi/adminOperationFail.html")