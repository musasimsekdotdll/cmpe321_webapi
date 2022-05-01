from django import forms

# This page is for all required inputs in order to make operations


# username and password is necessary so that we can open a session for the user
class UserLoginForm(forms.Form):
	username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
	password=forms.CharField(widget=forms.PasswordInput)


### FORMS FOR ADMIN OPERATIONS


# all input fields that admin needs to add a student to the database
class addStudentForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username'}))
	password = forms.CharField(widget=forms.PasswordInput)
	name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'name'}))
	surname = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'surname'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'email'}))
	student_id = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'studentId'}))
	gpa = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder':'gpa'}))
	completed_credits = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'completed credits'}))
	department_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'department id'}))


# all input fields that admin needs to add an instructor to the database
class addInstructorForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username'}))
	password = forms.CharField(widget=forms.PasswordInput)
	name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'name'}))
	surname = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'surname'}))
	email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'email'}))
	department_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'department id'}))
	title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'title'}))


# this form is used for all operations that need a student_id only
class studentForm(forms.Form):
	student_id = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'student id'}))


# input parameters for updating the title of an instructor
class updateTitleForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username of the instructor'}))
	new_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'new title'}))


# see all courses given by a specific instructor
class coursesOfInstructorForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username'}))


# average grada of a specific course
class averageGradeForm(forms.Form):
	course_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'course id'}))




### FORMS FOR INSTRUCTOR OPERATIONS


# available classrooms in a given time slot
class availableClassroomsForm(forms.Form):
	time_slot = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'time slot'}))


# open a course 
class openCourseForm(forms.Form):
	course_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'course id'}))
	name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'course name'}))
	credits = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'credits'}))
	classroom_id = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'classroom id'}))
	time_slot = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'time slot'}))
	quota = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'quota'}))


# add prerequisite condition for a given class, the prerequisite course must be given also
class addPrereqForm(forms.Form):
	preceding_course = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'preceding course id'}))
	following_course = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'following course id'}))


# view all students taking one of your courses and not graded yet
class viewEnrolledStudentsForm(forms.Form):
	course_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'course id'}))


# update the name of a course given by you
class updateCourseNameForm(forms.Form):
	course_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'course id'}))
	new_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'new name'}))


# grade a student for one of your courses
class gradeStudentForm(forms.Form):
	student_id = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'student id'}))
	course_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'course id'}))
	grade = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':'grade'}))



### FORMS FOR STUDENT OPERATIONS


# add an open course to your course list
class addCourseForm(forms.Form):
	course_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'course id'}))


# find all courses whose name includes the specified keyword
class findCoursesKeywordForm(forms.Form):
	keyword = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'keyword'}))


# filter courses by credit interval, campus and department
class filterCoursesForm(forms.Form):
	min_credits = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'minimum credits'}))
	max_credits = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'maximum credits'}))
	department_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'department id'}))
	campus = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'campus'}))


