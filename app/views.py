import os
from app import app, login_manager
from flask import Blueprint, render_template, request, redirect, jsonify,url_for,flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_bcrypt import Bcrypt 
from app.forms import * 
import jwt, datetime,json
from app.utils import token_required



app_views = Blueprint('app_views', __name__)
bcrypt = Bcrypt(app) 


@app.route('/login', methods=['POST'])
def user_login():
    form = LoginForm()
    db_conn = connectDB()
    cursor = db_conn.cursor()
    if form.validate_on_submit():
        user_id = form.user_id.data
        user_password = form.password.data
        query = "SELECT * FROM CMS_Account WHERE AccName = %s"
        cursor.execute(query, (user_id))
        account = cursor.fetchone()
        if account:
            if bcrypt.check_password_hash(user_password, account.password):
                login_user(account)
                flash('Logged in successfully!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password', 'fail')
        else:
            flash('User not found', 'fail')
    return render_template('login/login.html', form=form)




@app.route('/register', methods=['POST'])
def user_register():
    try:
        form = RegisterForm()
        db_conn= connectDB()
        cursor = db_conn.cursor()
        if form.validate_on_submit():
            user_id = form.user_id.data
            password = form.password.data
            first_name = form.first_name.data
            last_name = form.last_name.data

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') 

            acc_insert = "INSERT INTO CMS_Account (AccID, AccPassword) VALUES (%s, %s)"
            cursor.execute(acc_insert, (user_id, hashed_password ))

            if request.form['role'] == 'Student':
                student_insert= "INSERT INTO CMS_Students(StudID, FirstName, LastName) VALUES (%s, %s, %s)"
                cursor.execute = (student_insert, (user_id, first_name, last_name))
            
            elif request.form['role']== 'Lecturer':
                lecturer_insert = "INSERT INTO CMS_Lecturers(LecID,LFirstName,LLastname ,Department) VALUES (%s,%s,%s,%s)"
                cursor.execute = (lecturer_insert, (user_id, first_name, last_name, request.form['Department']))

            db_conn.commit()
            return redirect(url_for('user_login'))
        return render_template('signup/signup.html', form=form)
    except Exception as err:
        print({"Error": err})

#how to get the id for the account
@login_required
@app_views.route('/create/course', methods=['POST'])
def create_course():
    if request.form['role'] == 'Admin':
        try:
            form = CourseForm()
            db_conn = connectDB()
            cursor = db_conn.cursor()

            if form.validate_on_submit():
                course_code = form.course_code.data
                course_name = form.course_name.data
                department = form.department.data
                lecturer_name = form.lecturer.data
                def get_lecturer_id(name):
                    db_conn = connectDB()
                    cursor = db_conn.cursor()
                    lec_query = "SELECT LecID FROM CMS_Lecturers WHERE LFirstName= AND    LLastname= "
                    return id
                
                lecturer_id = get_lecturer_id(lecturer_name)

                course_insert = "INSERT INTO CMS_Courses(CName,CCode,CDepartment, LecID) VALUES (%s, %s, %s, %s)"
                cursor.execute(course_insert, (course_name, course_code, department, lecturer_id))

                db_conn.commit()
                return redirect(url_for('create_course'))

                pass
        except:
            pass



@login_required
@app_views.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for("user_login"))
    

#Retrieve Courses
@app_views.route("/api/courses", methods=["GET"])
def get_courses():
    if request.method== 'GET':
        try:
            db_conn = connectDB()
            cursor = db_conn.cursor()

            courses_query = "SELECT * FROM CMS_Courses"
            cursor.execute(courses_query)

            course_lst = []

            for course_id, course_name, course_code, course_department,lec_id in cursor:
                course = {}
                course['CID'] = course_id
                course[' CName '] = course_name
                course['CCode'] = course_code
                course['CDepartment'] = course_department
                course['LecID'] = lec_id

                course_lst.append(course)
            cursor.close()
            db_conn.close()
            return json.dumps(course_lst, sort_keys=False)
        except Exception as err:
            print({"Error": err})


@app_views.route("/api/courses/<student_id>", methods=['POST'])
def get_student_courses(student_id):
    if request.method =='POST':
        try:
            db_conn = connectDB()
            cursor = db_conn.cursor()

            student_courses = "SELECT CID,CName,CCode,CDepartment,LecID  FROM CMS_Courses INNER JOIN CMS_Enrolment on  CMS_Courses.CID=CMS_Enrolment.CID WHERE CMS_Enrolment.StudID={0}".format(student_id)
            cursor.execute(student_courses)

            course_lst = []

            for course_id, course_name, course_code, course_department,lec_id in cursor:
                course = {}
                course['CID'] = course_id
                course[' CName '] = course_name
                course['CCode'] = course_code
                course['CDepartment'] = course_department
                course['LecID'] = lec_id

                course_lst.append(course)
            cursor.close()
            db_conn.close()
            return json.dumps(course_lst, sort_keys=False)
        except Exception as err:
            print({"Error": err})        

@app_views.route("/api/courses/<lecturer_id>", methods=['POST'])
def get_lecturer_courses(lecturer_id):
    """Retrieves a list of courses taught by a lecturer."""
    if request.method =='POST':
        try:
            db_conn = connectDB()
            cursor = db_conn.cursor()

            courses_taught = "SELECT CID,CName,CCode,CDepartment,LecID FROM CMS_Courses WHERE LecID={0}".format(lecturer_id)
            cursor.execute(courses_taught)

            course_lst = []

            for course_id, course_name, course_code, course_department,lec_id in cursor:
                course = {}
                course['CID'] = course_id
                course['CName'] = course_name
                course['CCode'] = course_code
                course['CDepartment'] = course_department
                course['LecID'] = lec_id

                course_lst.append(course)
            cursor.close()
            db_conn.close()
            return json.dumps(course_lst, sort_keys=False)
        except Exception as err:
            print({"Error": err})  


@app_views.route("/api/course/<course_id>", methods=["POST"])
def get_course_members(course_id):
    """This function retrieves a list of students and lecturers enrolled in a course.
"""
    if request.method=="POST":
        try:
            db_conn = connectDB()
            cursor = db_conn.cursor()
            members_query = "SELECT FirstName ,LastName FROM CMS_Students  \
            INNER JOIN CMS_Enrolment on CMS_Students.StudID=CMS_Enrolment.StudID\
            INNER JOIN CMS_Courses on CMS_Enrolment.CID=CMS_Courses.CID \
            WHERE CMS_Courses.CID=%s\
            UNION SELECT LFirstName ,LLastname FROM CMS_Lecturers\
            INNER JOIN CMS_Teaches on CMS_Lecturers.LecID=CMS_Teaches.LecID \
            INNER JOIN CMS_Courses on CMS_Teaches.CID= CMS_Courses.CID \
            WHERE CMS_Courses.CID=%s"
            cursor.execute(members_query, (course_id, course_id))

            names_lst = []
            for first_name, last_name in cursor:
                name = {}
                name['Full_name'] = (first_name, last_name)
                names_lst.append(name)
            cursor.close()
            db_conn.close()
            return json.dumps(names_lst, sort_keys=False)
            
        except Exception as err:
            print({"Error": err})

@app_views.route("/api/register/course/<student_id>", methods=["POST"])
def register_course(student_id):
    """
    Registers a student for a course.
    """
    if request.method == "POST":
        form = RegisterCourse()
        if form.validate_on_submit():
            try:
                db_conn = connectDB()
                cursor = db_conn.cursor()
                course = form.course.data
                course_code, course_name = course.split()
                select_query= "SELECT CID FROM CMS_Courses WHERE CCode =%s AND CName=%s"
                cursor.execute(select_query, (course_code, course_name))
                course_id = cursor.fetchone()
                insert_course = "INSERT INTO CMS_Enrolment(StudID, CID) VALUES(%s, %s)"
                cursor.execute(insert_course,(student_id, course_id) )
                cursor.close()
                db_conn.close()
            except Exception as err:
                  print({"Error": err})
    pass


@app_views.route("/calender_event/<course_id>", methods="POST")
def get_calender_events(course_id):
    if request.method =="POST":
        try:
            db_conn = connectDB()
            cursor = db_conn.cursor()

            calender_query = "SELECT * FROM CMS_Events WHERE CourseID =%s"
            cursor.execute(calender_query, (course_id))
            event_lst= []
            for event_ID, course_ID, event_Date, event_Description in cursor:
                event = {}
                event["eventID"] = event_ID
                event["CourseID"] = course_ID
                event["eventDate"] = event_Date
                event['eventDescription'] = event_Description
                event_lst.append(event)
            cursor.close()
            db_conn.close()
            return json.dumps(event_lst, sort_keys=False)
        except Exception as err:
            print({"Error":err})

@app_views.route("/calender_event/<calender_date>/<student_id>", methods="GET")
def get_student_events(calender_date,student_id):
    if request.method =="GET":
        try:
            db_conn = connectDB()
            students_events = "SELECT * from CMS_Events INNER JOIN CMS_Enrolment CMS_Events.CourseID=CMS_Enrolment.CID \
                WHERE CMS_Enrolment.StudID = %s AND CMS_Events.eventDate = %s"
            cursor = db_conn.cursor()
            cursor.execute(students_events, (student_id, calender_date))
            events = cursor.fetchall()
            return jsonify(events)
        
        except Exception as err:
            return jsonify({"Error":str(err)})
        
@app_views.route("/create/calender_event", methods=["POST"])
def create_calender_event():
    if request.method == "POST":
        form = CalenderEventForm()
        if form.validate_on_submit():
            try:
                db_conn = connectDB()
                cursor = db_conn.cursor()
                event_date = form.event_date.data
                description = form.event_description.data
                course = form.course.data
                course_code, course_name = course.split()
                select_query= "SELECT CID FROM CMS_Courses WHERE CCode =%s AND CName=%s"
                cursor.execute(select_query, (course_code, course_name))
                course_id = cursor.fetchone()
                calender_event_insert = "INSERT INTO CMS_Events(CourseID,eventDate,eventDescription) VALUES(%s, %s, %s)"
                cursor.execute(calender_event_insert, (course_id, event_date, description))
                cursor.close()
                db_conn.close()
                return ({"Success: Calender event has been successfully added"})
            except Exception as err:
                return jsonify({"Error": err})
            
@app_views("/forums/<course_id>", methods=["GET"])
def get_forums(course_id):
    if request.method== "GET":
        try:
            db_conn = connectDB()
            cursor = db_conn.cursor()
            forum_query = "SELECT * FROM CMS_Forums WHERE ForumCourseID=%s"
            cursor.execute(forum_query, course_id)
            forum_lst = []
            for forum_id, course_id, forum_name in cursor:
                forum = {}
                forum["ForumID"] = forum_id
                forum["ForumCourseID"] = course_id
                forum["ForumName"] = forum_name

                forum_lst.append(forum)
            cursor.close()
            db_conn.close()
            return json.dumps(forum_lst, sort_keys=False)
        except Exception as err:
            return ({"Error": err})

@app_views("/api/create/forum", methods=["POST"])
def create_course_forum():
   if request.method == "POST":
       form = ForumForm()
       if form.validate_on_submit():
           try:
               db_conn = connectDB()
               cursor = db_conn.cursor()
               forum_name = form.forum_name.data
               course  = form.course.data
               course_code, course_name = course.split()
               select_query= "SELECT CID FROM CMS_Courses WHERE CCode =%s AND CName=%s"
               cursor.execute(select_query, (course_code, course_name))
               course_id = cursor.fetchone()

               forum_insert = "INSERT INTO CMS_Forums(ForumCourseID, ForumName) VALUES (%s, %s)"
               cursor.execute(forum_insert, (course_id, forum_name))

               return ({
                   "Statuscode":201,
                   "Success": "Forum created successfully"
               })
           except Exception as err:
               return({"Error": err})
    

@app_views("/api/discussion_threads/<forum_id>", methods=["GET"])
def get_forum_threads(forum_id):
    if request.method == "GET":
        try:
            db_conn = connectDB()
            cursor = db_conn.cursor()

            thread_query= "SELECT * FROM CMS_Threads WHERE ForumID=%s"
            cursor.execute(thread_query, (forum_id))

            threads = cursor.fetchall()
            thread_lst = []

            for thread_id, forum_id, creater_id, thread_title, thread_content, created_at in cursor:
                thread = {}
                thread["TID"] = thread_id
                thread["ForumID"] = forum_id
                thread["CreatorID"] = creater_id
                thread["Title"] = thread_title
                thread["Content"] = thread_content
                thread["CreatedAt"] = created_at
                thread_lst.append(thread)
            return json.dumps(thread_lst, sort_keys=False)
        
        except Exception as err:
            return ({"Error": err})


    

@app_views("/api/create/discussion_thread/forum", methods=["POST"])
@login_required
def create_forum_thread():
    if request.method == "POST":
        form  = DiscussionThreadForm()
        if form.validate_on_submit():
            try:
                db_conn = connectDB()
                cursor = db_conn.cursor()
                title = form.title.data
                content = form.content.data 
                forum_name = form.forum.data

                forum_query= "SELECT ForumID FROM CMS_Forums WHERE ForumName=%s"
                cursor.execute(forum_query, (forum_name))
                forum_id = cursor.fetchone()
                creater_id = current_user.id

                insert_sql = "INSERT INTO CMS_Threads (ForumID, CreatorID, Title, Content)\
                VALUES(%s, %s, %s, %s)"

                cursor.execute(insert_sql, (forum_id, creater_id, title, content))
                return jsonify(
            message="Discussion thread created successfully."
            )
            except Exception as err:
                return ({"Error": err})

@app_views("/api/discussion_thread/forum/reply", methods=["POST"])
@login_required
def create_reply_thread():
    if request.method=="POST":
        form  = CommentForm()
        if form.validate_on_submit():
            try:
                db_conn = connectDB()
                cursor = db_conn.cursor()
                thread = form.thread.data
                query_thread = "SELECT TID FROM CMS_Threads WHERE Title=%s"
                cursor.execute(query_thread, (thread))
                thread_id = cursor.fetchone()
                user_id = current_user.id
                content = form.content.data

                comment_insert  = "INSERT INTO CMS_Comments(ThreadID, AuthorID,  Content) VALUES(%s,%s,%s)"
                cursor.execute(comment_insert, (thread_id, user_id, content))

                db_conn.commit()
                return ({"Status" : 201,
                         "message": "Reply created successfully"})
    
            except Exception as err:
                return ({"Error": err})


@app_views("/api/create/course_content", methods=["POST"])
def create_course_content():
    if request.method == "POST":
        form = CourseContentForm()
        if form.validate_on_submit():
            if request.form["contentType"]=="link":
                try:
                    db_conn = connectDB()
                    cursor = db_conn.cursor()
                    course = form.course.data
                    section_no = form.section_no.data
                    content = form.content.data
                    content_type = request.form["contentType"]
                    course_code, course_name = course.split()
                    select_query= "SELECT CID FROM CMS_Courses WHERE CCode =%s AND CName=%s"
                    cursor.execute(select_query, (course_code, course_name))
                    course_id = cursor.fetchone()
                    course_content_insert = "INSERT INTO CMS_CourseContent(CourseID, SectionNo, Content, ContentType) VALUES(%s, %s, %s, %s)"
                except Exception as err:
                    return ({"Error": err})
            elif request.form["contentType"]=="file":
                try:
                    db_conn = connectDB()
                    cursor = db_conn.cursor()
                    course = form.course.data
                    section_no = form.section_no.data
                    content = form.content.data
                    content_type = request.form["contentType"]
                    course_code, course_name = course.split()
                    select_query= "SELECT CID FROM CMS_Courses WHERE CCode =%s AND CName=%s"
                    cursor.execute(select_query, (course_code, course_name))
                    course_id = cursor.fetchone()
                    course_content_insert = "INSERT INTO CMS_CourseContent(CourseID, SectionNo, Content, ContentType) VALUES(%s, %s, %s, %s)"
                except Exception as err:
                    return ({"Error": err})
            elif request.form["contentType"]=="slide":
                try:
                    db_conn = connectDB()
                    cursor = db_conn.cursor()
                    course = form.course.data
                    section_no = form.section_no.data
                    content = form.content.data
                    content_type = request.form["contentType"]
                    course_code, course_name = course.split()
                    select_query= "SELECT CID FROM CMS_Courses WHERE CCode =%s AND CName=%s"
                    cursor.execute(select_query, (course_code, course_name))
                    course_id = cursor.fetchone()
                    course_content_insert = "INSERT INTO CMS_CourseContent(CourseID, SectionNo, Content, ContentType) VALUES(%s, %s, %s, %s)"
                except Exception as err:
                    return ({"Error": err})

            cursor.execute(course_content_insert, (course_id, section_no, content, content_type))
            db_conn.commit()
            return ({"Status" : 201,
                     "message": "Course content created successfully"})
        
@app_views("/api/get/course_content/<course_id>", methods=["GET"])
def get_course_content(course_id):
    if request.method == "GET":
        try:
            db_conn = connectDB()
            cursor = db_conn.cursor()
            course_content_query = "SELECT * FROM CMS_CourseContent WHERE CourseID=%s"
            cursor.execute(course_content_query, (course_id))
            course_content = cursor.fetchall()
            cursor.close()
            db_conn.close()
            return json.dumps(course_content, sort_keys=False)
        except Exception as err:
            return ({"Error": err})
        


@app_views("/api/create_assignment", methods=["POST"])
def create_assignment():
    if request.method == "POST":
        form = AssignmentForm()
        if form.validate_on_submit():
            try:
                db_conn = connectDB()
                cursor = db_conn.cursor()
                course = form.course.data
                course_code, course_name = course.split()
                select_query= "SELECT CID FROM CMS_Courses WHERE CCode =%s AND CName=%s"
                cursor.execute(select_query, (course_code, course_name))
                course_id = cursor.fetchone()
                assignment_insert = "INSERT INTO CMS_Assignments(CourseID, Title, Description, DueDate) VALUES(%s, %s, %s, %s)"
                cursor.execute(assignment_insert, (course_id, form.title.data, form.description.data, form.due_date.data))
                db_conn.commit()
                return ({"Status" : 201,
                         "message": "Assignment created successfully"})
            except Exception as err:
                return ({"Error": err})
#Student can submit assignment to a course
app_views("/api/submit_assignment", methods=["POST"])
def submit_assignment():
    if request.method == "POST":
        form = SubmissionForm()
        if form.validate_on_submit():
            try:
                db_conn = connectDB()
                cursor = db_conn.cursor()
                course = form.assignment.data
                course_code, course_name = course.split()
                select_query= "SELECT CID FROM CMS_Courses WHERE CCode =%s AND CName=%s"
                cursor.execute(select_query, (course_code, course_name))
                course_id = cursor.fetchone()
                assignment_insert = "INSERT INTO CMS_Submissions(CourseID, AssignmentID, Content) VALUES(%s, %s, %s)"
                cursor.execute(assignment_insert, (course_id, form.assignment.data, form.content.data))
                db_conn.commit()
                return ({"Status" : 201,
                         "message": "Assignment submitted successfully"})
            except Exception as err:
                return ({"Error": err})

#A lecturer can submit a grade for a particular student for that assignment.
app_views("/api/grade_assignment", methods=["POST"])
def grade_assignment():
    if request.method == "POST":
        form = GradeForm()
        if form.validate_on_submit():
            try:
                db_conn = connectDB()
                cursor = db_conn.cursor()
                course = form.assignment.data
                course_code, course_name = course.split()
                select_query= "SELECT CID FROM CMS_Courses WHERE CCode =%s AND CName=%s"
                cursor.execute(select_query, (course_code, course_name))
                course_id = cursor.fetchone()
                assignment_insert = "INSERT INTO CMS_Submissions(CourseID, AssignmentID, Content) VALUES(%s, %s, %s)"
                cursor.execute(assignment_insert, (course_id, form.assignment.data, form.content.data))
                db_conn.commit()
                return ({"Status" : 201,
                         "message": "Assignment submitted successfully"})
            except Exception as err:
                return ({"Error": err})

#Each grade a student gets goes to their final average.
app_views("/api/get_grades", methods=["GET"])
def get_grades():
    if request.method == "GET":
        try:
            db_conn = connectDB()
            cursor = db_conn.cursor()
            course_content_query = "SELECT * FROM CMS_Submissions"
            cursor.execute(course_content_query)
            course_content = cursor.fetchall()
            cursor.close()
            db_conn.close()
            return json.dumps(course_content, sort_keys=False)
        except Exception as err:
            return ({"Error": err})

#Report section
app_views("/api/courses/students/<count>", methods=["GET"])
def get_courses_students(count):
    #All courses that have 50 or more students
    if request.method == "GET":
        try:
            db_conn = connectDB()
            cursor = db_conn.cursor()
            course_content_query = "SELECT * FROM CMS_Enrolment"
            cursor.execute(course_content_query)
            course_content = cursor.fetchall()
            cursor.close()
            db_conn.close()
            return json.dumps(course_content, sort_keys=False)
        except Exception as err:
            return ({"Error": err})
        
#All students that do 5 or more courses
app_views("/api/courses/students/<int:count>", methods=["GET"])
def get_courses_students(count):
    if request.method == "GET":
        try:
            db_conn = connectDB()
            cursor = db_conn.cursor()
            course_content_query = "SELECT * FROM CMS_Enrolment"
            cursor.execute(course_content_query)
            course_content = cursor.fetchall()
            cursor.close()
            db_conn.close()
            return json.dumps(course_content, sort_keys=False)
        except Exception as err:
            return ({"Error": err})

#All lecturers that teach 3 or more courses.
app_views("/api/courses/lecturers/<int:count>", methods=["GET"])
def get_courses_lecturers(count):
    if request.method == "GET":
        try:
            db_conn = connectDB()
            cursor = db_conn.cursor()
            course_content_query = "SELECT * FROM CMS_Enrolment"
            cursor.execute(course_content_query)
            course_content = cursor.fetchall()
            cursor.close()
            db_conn.close()
            return json.dumps(course_content, sort_keys=False)
        except Exception as err:
            return ({"Error": err})

#The 10 most enrolled courses
app_views("/api/courses/most_enrolled", methods=["GET"])
def get_courses_enrolled():
    if request.method == "GET":
        try:
            db_conn = connectDB()
            cursor = db_conn.cursor()
            course_content_query = "SELECT * FROM CMS_Enrolment"
            cursor.execute(course_content_query)
            course_content = cursor.fetchall()
            cursor.close()
            db_conn.close()
            return json.dumps(course_content, sort_keys=False)
        except Exception as err:
            return ({"Error": err})
        
@app_views("/api/students_highest_average", methods=["GET"])
def get_students_highest_average():
    if request.method == "GET":
        try:
            db_conn = connectDB()
            cursor = db_conn.cursor()
            course_content_query = "SELECT * FROM CMS_Enrolment"
            cursor.execute(course_content_query)
            course_content = cursor.fetchall()
            cursor.close()
            db_conn.close()
            return json.dumps(course_content, sort_keys=False)
        except Exception as err:
            return ({"Error": err})
