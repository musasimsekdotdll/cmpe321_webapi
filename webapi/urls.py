from django.urls import path
from . import views

appname = 'webapi'

urlpatterns = [
	path('index', views.index, name='index'),
	path('adminLogin', views.adminLogin, name='adminLogin'),
	path('instructor/login', views.instructorLogin, name="instructor_login"),
	path('student/login', views.studentLogin, name="student_login"),
	path('admin/addStudent', views.addStudent, name='add_student'),
	path('admin/addInstructor', views.addInstructor, name="add_instructor"),
	path('admin/deleteStudent', views.deleteStudent, name="delete_student"),
	path('admin/updateTitle', views.updateTitle, name='update_title'),
	path("admin/viewStudents", views.viewStudents, name="view_students"),
	path("admin/viewInstructors", views.viewInstructors, name="view_instructors"),
	path("admin/viewGrades", views.viewGradesOfStudent, name="view_grades"),
	path("admin/viewCourses", views.viewCoursesOfInstructor, name="view_courses"),
	path("admin/viewAverage", views.viewCourseAverage, name="view_average"),
	path("instructor/availableClassrooms", views.listAvailableClassrooms, name="list_classrooms"),
	path("instructor/openCourse", views.openCourse, name="open_course"),
	path("instructor/addPrerequisite", views.addPrereq, name="add_prereq"),
	path("instructor/viewGivenCourses", views.viewGivenCourses, name="view_courses_given"),
	path("instructor/viewEnrolledStudents", views.viewEnrolledStudents, name="view_enrolled_students"),
	path("instructor/updateCourseName",views.updateCourseName, name="update_course_name"),
	path("instructor/gradeStudent", views.gradeStudent, name="grade_student"),
	path("student/seeCourses", views.seeCourses, name="see_courses"),
	path("student/addCourse", views.addCourse, name="add_course"),
	path("student/courseHistory", views.courseHistory, name="see_course_history"),
	path("student/searchCourses", views.findCoursesByKeyword, name="find_courses_keyword"),
	path("student/filterCourses", views.filterCourses, name="filter_courses"),
]