from django.db import models

from django.core.exceptions import ValidationError


instructor_title_options = ["Assistant Professor", "Associate Professor", "Professor"]

def validate_instructor_title(value):
	global instructor_title_options

	if value in instructor_title_options:
		return value
	else:
		raise ValidationError("There is no such available title")

def validate_time_slot(value):

	if value<=10 and value>=1:
		return value
	else:
		return ValidationError("Wrong time slot value")

# Create your models here.

class Classroom(models.Model):
	classroomId = models.IntegerField(primary_key=True)
	campus = models.CharField(max_length=255)
	capacity = models.PositiveIntegerField()


class DatabaseManager(models.Model):
	username = models.CharField(max_length=25, primary_key=True)
	password = models.CharField(max_length=255)


class Department(models.Model):
	departmentId = models.CharField(primary_key=True, max_length=255)
	name = models.CharField(max_length=255, unique=True)
	

class Instructor(models.Model):
	username = models.CharField(max_length=25, primary_key=True)
	password = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	surname = models.CharField(max_length=255)
	department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)	
	title = models.CharField(max_length=25, validators = [validate_instructor_title])	


class Course(models.Model):
	name = models.CharField(max_length=255)
	courseId = models.CharField(primary_key=True, max_length=255)
	credits = models.PositiveSmallIntegerField()
	quota = models.PositiveIntegerField()
	instructor = models.ForeignKey(Instructor, null=True, on_delete=models.SET_NULL)


class Student(models.Model):
	username = models.CharField(max_length=25, primary_key=True)
	password = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	surname = models.CharField(max_length=255)
	courses = models.TextField()
	department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
	studentId = models.IntegerField(unique=True)
	gpa = models.FloatField()
	completedCredits = models.PositiveSmallIntegerField()


class Prereq(models.Model):
	precedingCourse = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='preceding')
	followingCourse = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='following')

	class Meta:
		managed = False
		db_table = 'prereq'
		unique_together = (('precedingCourse', 'followingCourse'),)


class Graded(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	grade = models.FloatField()

	class Meta:
		managed = False
		db_table = 'graded'
		unique_together = (('student', 'course'),)


class GivenIn(models.Model):
	classroom = models.ForeignKey(Classroom, null=True, on_delete=models.SET_NULL)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	timeSlot = models.PositiveSmallIntegerField(validators = [validate_time_slot])

	class Meta:
		managed = False
		db_table = 'given_in'
		unique_together = (('classroom', 'course'), ('classroom', 'timeSlot'),)