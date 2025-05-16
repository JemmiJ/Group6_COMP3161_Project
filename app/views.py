# Refactored views.py for COMP3161 Course Management System

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, RegisterForm, CourseForm, RegisterCourse, CalenderEventForm, ForumForm, DiscussionThreadForm, CommentForm, CourseContentForm, AssignmentForm, SubmissionForm, GradeForm
from app.utils import token_required, role_required
from app.db import connectDB
import json

app_views = Blueprint('app_views', __name__)

@app_views.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

# --- Auth Routes ---
@app_views.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        db = connectDB()
        cursor = db.cursor()
        user_id = form.user_id.data
        password = form.password.data
        
        
        query = "SELECT * FROM CMS_Account WHERE AccID = %s"
        cursor.execute(query, (user_id))
        account = cursor.fetchone()
        acc_id, pass_hash = account
        print(acc_id, pass_hash)

        if acc_id and check_password_hash(pass_hash, password):
            session['user_id'] = acc_id
            # Determine user role
            print("User role:", session['role'])
            if session['role'] == 'student':
                print("Redirecting to student dashboard...")
                session['logged_in'] = True
                return jsonify({"Success": 200, "message": "Login successful."})
            
            if session['role'] == 'lecturer':
                session['logged_in'] = True
                return jsonify({"Success": 200, "message": "Login successful."})

            if session['role'] == 'admin':
                session['logged_in'] = True
                return jsonify({"Success": 200, "message": "Login successful."})
            return jsonify({"Error": 401, "message:": "Not authorized."})
        else:
            return jsonify({"Error": 400,"message": "Invalid credentials."})
    return jsonify({"Error": 400, "message": "Login failed."})



@app_views.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        db = connectDB()
        cursor = db.cursor()

        user_id = form.user_id.data
        password = generate_password_hash(form.password.data)
        first_name = form.first_name.data
        last_name = form.last_name.data
        role = request.form.get('role')

        # Insert into CMS_Account
        cursor.execute("INSERT INTO CMS_Account (AccID, AccPassword) VALUES (%s, %s)", (user_id, password))

        if role == 'student':
            cursor.execute("INSERT INTO CMS_Students (StudID, FirstName, LastName) VALUES (%s, %s, %s)",
                           (user_id, first_name, last_name))
        elif role == 'lecturer':
            department = request.form.get('department')
            cursor.execute("INSERT INTO CMS_Lecturers (LecID, LFirstName, LLastname, Department) VALUES (%s, %s, %s, %s)",
                           (user_id, first_name, last_name, department))
        elif role == 'admin':
            cursor.execute("INSERT INTO CMS_Admin (AdminID, AdminName, AdminPassword) VALUES (%s, %s, %s)",
                           (user_id, first_name + ' ' + last_name, password))

        db.commit()
        return jsonify({"Succces":201, "message":"Account created successfully"}) 
    return jsonify({"Error":400, "message":"Account creation failed"})


@app_views.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('app_views.login'))


# --- Dashboard routes ---
@app_views.route('/student/dashboard')
@login_required
@role_required('student')
def student_dashboard():
    return render_template('student_dashboard.html')


@app_views.route('/lecturer/dashboard')
@login_required
@role_required('lecturer')
def lecturer_dashboard():
    return render_template('lec_dashboard.html')


@app_views.route('/admin/dashboard')
@login_required
@role_required('admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app_views.route('/courses/create', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def create_course():
    form = CourseForm()
    if request.method == 'POST' and form.validate_on_submit():
        course_code = form.course_code.data
        course_name = form.course_name.data
        department = form.department.data
        lecturer_name = form.lecturer.data

        try:
            first, last = lecturer_name.strip().split(" ", 1)
            db = connectDB()
            cursor = db.cursor()
            cursor.execute("SELECT LecID FROM CMS_Lecturers WHERE LFirstName = %s AND LLastname = %s", (first, last))
            lec = cursor.fetchone()

            if not lec:
                flash("Lecturer not found", "danger")
                return redirect(url_for('app_views.create_course'))

            lec_id = lec[0]
            cursor.execute("""
                INSERT INTO CMS_Courses (CName, CCode, CDepartment, LecID)
                VALUES (%s, %s, %s, %s)
            """, (course_name, course_code, department, lec_id))
            db.commit()
            flash("Course created successfully.", "success")
            return redirect(url_for('app_views.create_course'))

        except Exception as e:
            flash(f"Error: {e}", "danger")

    return render_template('create_course.html', form=form)


@app_views.route('/courses')
@login_required
def view_all_courses():
    db = connectDB()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM CMS_Courses")
    courses = cursor.fetchall()
    return render_template('course_list.html', courses=courses)


@app_views.route('/student/courses')
@login_required
@role_required('student')
def student_courses():
    student_id = session['user_id']
    db = connectDB()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM CMS_Courses
        INNER JOIN CMS_Enrolment ON CMS_Courses.CID = CMS_Enrolment.CID
        WHERE CMS_Enrolment.StudID = %s
    """, (student_id,))
    courses = cursor.fetchall()
    return render_template('student_courses.html', courses=courses)


@app_views.route('/lecturer/courses')
@login_required
@role_required('lecturer')
def lecturer_courses():
    lecturer_id = session['user_id']
    db = connectDB()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM CMS_Courses WHERE LecID = %s", (lecturer_id,))
    courses = cursor.fetchall()
    return render_template('lecturer_courses.html', courses=courses)


@app_views.route('/courses/register', methods=['GET', 'POST'])
@login_required
@role_required('student')
def register_course():
    form = RegisterCourse()
    student_id = session['user_id']
    if request.method == 'POST' and form.validate_on_submit():
        course = form.course.data
        try:
            course_code, course_name = course.strip().split(" ", 1)
            db = connectDB()
            cursor = db.cursor()
            cursor.execute("SELECT CID FROM CMS_Courses WHERE CCode = %s AND CName = %s", (course_code, course_name))
            result = cursor.fetchone()
            if not result:
                flash("Course not found.", "danger")
                return redirect(url_for('app_views.register_course'))
            course_id = result[0]
            cursor.execute("INSERT INTO CMS_Enrolment (StudID, CID) VALUES (%s, %s)", (student_id, course_id))
            db.commit()
            return jsonify({"Success": 200, "message": "Course registered successfully."})
        except Exception as e:
            return jsonify({"Error": 400, "message": f"Error: {e}"})
    return jsonify({"Error": 400, "message": "Course registration failed."})

@app_views.route('/calendar/<int:course_id>')
@login_required
def view_calendar(course_id):
    db = connectDB()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM CMS_Events WHERE CourseID = %s", (course_id,))
    events = cursor.fetchall()
    return render_template('calendar_view.html', events=events, course_id=course_id)


@app_views.route('/calendar/create', methods=['GET', 'POST'])
@login_required
@role_required('lecturer')
def create_event():
    form = CalenderEventForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            event_date = form.event_date.data
            description = form.event_description.data
            course = form.course.data.strip()
            course_code, course_name = course.split(" ", 1)

            db = connectDB()
            cursor = db.cursor()
            cursor.execute("SELECT CID FROM CMS_Courses WHERE CCode = %s AND CName = %s", (course_code, course_name))
            cid_row = cursor.fetchone()
            if not cid_row:
                flash("Course not found.", "danger")
                return redirect(url_for('app_views.create_event'))

            course_id = cid_row[0]
            cursor.execute("""
                INSERT INTO CMS_Events (CourseID, eventDate, eventDescription)
                VALUES (%s, %s, %s)
            """, (course_id, event_date, description))
            db.commit()
            flash("Event created successfully.", "success")
            return redirect(url_for('app_views.view_calendar', course_id=course_id))
        except Exception as e:
            flash(f"Error: {e}", "danger")
    return render_template('create_event.html', form=form)


@app_views.route('/calendar/date/<string:date>/student')
@login_required
@role_required('student')
def student_events_by_date(date):
    student_id = session['user_id']
    db = connectDB()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.* FROM CMS_Events e
        JOIN CMS_Enrolment en ON e.CourseID = en.CID
        WHERE en.StudID = %s AND DATE(e.eventDate) = %s
    """, (student_id, date))
    events = cursor.fetchall()
    return render_template('student_events.html', events=events, date=date)

@app_views.route('/forums/<int:course_id>')
@login_required
def view_forums(course_id):
    db = connectDB()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM CMS_Forums WHERE ForumCourseID = %s", (course_id,))
    forums = cursor.fetchall()
    return render_template('forums_list.html', forums=forums, course_id=course_id)


@app_views.route('/forums/create', methods=['GET', 'POST'])
@login_required
@role_required('lecturer')
def create_forum():
    form = ForumForm()
    if request.method == 'POST' and form.validate_on_submit():
        forum_name = form.forum_name.data
        course_code, course_name = form.course.data.strip().split(" ", 1)
        db = connectDB()
        cursor = db.cursor()
        cursor.execute("SELECT CID FROM CMS_Courses WHERE CCode = %s AND CName = %s", (course_code, course_name))
        course_id = cursor.fetchone()

        if not course_id:
            flash("Course not found.", "danger")
            return redirect(url_for('app_views.create_forum'))

        cursor.execute("INSERT INTO CMS_Forums (ForumCourseID, ForumName) VALUES (%s, %s)", (course_id[0], forum_name))
        db.commit()
        flash("Forum created successfully.", "success")
        return redirect(url_for('app_views.view_forums', course_id=course_id[0]))

    return render_template('create_forum.html', form=form)


@app_views.route('/threads/<int:forum_id>')
@login_required
def view_threads(forum_id):
    db = connectDB()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM CMS_Threads WHERE ForumID = %s", (forum_id,))
    threads = cursor.fetchall()
    return render_template('thread_list.html', threads=threads, forum_id=forum_id)


@app_views.route('/threads/create', methods=['GET', 'POST'])
@login_required
def create_thread():
    form = DiscussionThreadForm()
    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        forum_name = form.forum.data
        user_id = session['user_id']

        db = connectDB()
        cursor = db.cursor()
        cursor.execute("SELECT ForumID FROM CMS_Forums WHERE ForumName = %s", (forum_name,))
        forum_id = cursor.fetchone()

        if not forum_id:
            flash("Forum not found.", "danger")
            return redirect(url_for('app_views.create_thread'))

        cursor.execute("""
            INSERT INTO CMS_Threads (ForumID, CreatorID, Title, Content)
            VALUES (%s, %s, %s, %s)
        """, (forum_id[0], user_id, title, content))
        db.commit()
        flash("Thread created successfully.", "success")
        return redirect(url_for('app_views.view_threads', forum_id=forum_id[0]))

    return render_template('create_thread.html', form=form)


@app_views.route('/replies/create', methods=['GET', 'POST'])
@login_required
def create_reply():
    form = CommentForm()
    if request.method == 'POST' and form.validate_on_submit():
        thread_title = form.thread.data
        content = form.content.data
        user_id = session['user_id']

        db = connectDB()
        cursor = db.cursor()
        cursor.execute("SELECT TID FROM CMS_Threads WHERE Title = %s", (thread_title,))
        thread = cursor.fetchone()

        if not thread:
            flash("Thread not found.", "danger")
            return redirect(url_for('app_views.create_reply'))

        cursor.execute("INSERT INTO CMS_Comments (ThreadID, AuthorID, Content) VALUES (%s, %s, %s)",
                       (thread[0], user_id, content))
        db.commit()
        flash("Reply posted successfully.", "success")
        return redirect(url_for('app_views.view_threads', forum_id=thread[0]))

    return render_template('create_reply.html', form=form)

@app_views.route('/assignments/create', methods=['GET', 'POST'])
@login_required
@role_required('lecturer')
def create_assignment():
    form = AssignmentForm()
    if request.method == 'POST' and form.validate_on_submit():
        course = form.course.data.strip()
        course_code, course_name = course.split(" ", 1)

        db = connectDB()
        cursor = db.cursor()
        cursor.execute("SELECT CID FROM CMS_Courses WHERE CCode = %s AND CName = %s", (course_code, course_name))
        course_id = cursor.fetchone()

        if not course_id:
            flash("Course not found.", "danger")
            return redirect(url_for('app_views.create_assignment'))

        cursor.execute("""
            INSERT INTO CMS_Assignments (CourseID, Title, Description, DueDate)
            VALUES (%s, %s, %s, %s)
        """, (course_id[0], form.title.data, form.description.data, form.due_date.data))
        db.commit()
        flash("Assignment created successfully.", "success")
        return redirect(url_for('app_views.create_assignment'))

    return render_template('create_assignment.html', form=form)


@app_views.route('/assignments/submit', methods=['GET', 'POST'])
@login_required
@role_required('student')
def submit_assignment():
    form = SubmissionForm()
    student_id = session['user_id']
    if request.method == 'POST' and form.validate_on_submit():
        course = form.assignment.data.strip()
        course_code, course_name = course.split(" ", 1)

        db = connectDB()
        cursor = db.cursor()
        cursor.execute("SELECT CID FROM CMS_Courses WHERE CCode = %s AND CName = %s", (course_code, course_name))
        course_id = cursor.fetchone()

        if not course_id:
            flash("Course not found.", "danger")
            return redirect(url_for('app_views.submit_assignment'))

        # Get assignment ID (assuming latest for course)
        cursor.execute("SELECT AssignId FROM CMS_Assignments WHERE CourseID = %s ORDER BY DueDate DESC LIMIT 1", (course_id[0],))
        assignment_id = cursor.fetchone()

        if not assignment_id:
            flash("Assignment not found for this course.", "danger")
            return redirect(url_for('app_views.submit_assignment'))

        cursor.execute("""
            INSERT INTO CMS_Submissions (AID, SID, Content)
            VALUES (%s, %s, %s)
        """, (assignment_id[0], student_id, form.content.data))
        db.commit()
        flash("Assignment submitted successfully.", "success")
        return redirect(url_for('app_views.submit_assignment'))

    return render_template('submit_assignment.html', form=form)


@app_views.route('/assignments/grade', methods=['GET', 'POST'])
@login_required
@role_required('lecturer')
def grade_assignment():
    form = GradeForm()
    if request.method == 'POST' and form.validate_on_submit():
        student_id = form.student_id.data
        grade = form.grade.data
        feedback = form.feedback.data
        course = form.assignment.data.strip()
        course_code, course_name = course.split(" ", 1)

        db = connectDB()
        cursor = db.cursor()
        cursor.execute("SELECT CID FROM CMS_Courses WHERE CCode = %s AND CName = %s", (course_code, course_name))
        course_id = cursor.fetchone()

        cursor.execute("SELECT AssignId FROM CMS_Assignments WHERE CourseID = %s ORDER BY DueDate DESC LIMIT 1", (course_id[0],))
        assignment_id = cursor.fetchone()

        if assignment_id:
            cursor.execute("""
                UPDATE CMS_Submissions
                SET Grade = %s, Feedback = %s
                WHERE AID = %s AND SID = %s
            """, (grade, feedback, assignment_id[0], student_id))
            db.commit()
            flash("Grade submitted successfully.", "success")
        else:
            flash("Assignment not found.", "danger")

    return render_template('grade_assignment.html', form=form)


@app_views.route('/grades')
@login_required
@role_required('student')
def view_grades():
    student_id = session['user_id']
    db = connectDB()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.Title, s.Grade, s.Feedback, s.SubmissionDATE
        FROM CMS_Submissions s
        JOIN CMS_Assignments a ON s.AID = a.AssignId
        WHERE s.SID = %s
        ORDER BY s.SubmissionDATE DESC
    """, (student_id,))
    grades = cursor.fetchall()
    return render_template('view_grades.html', grades=grades)

@app_views.route('/api/reports/courses/min_students/<int:min_students>', methods=['GET'])
@login_required
@role_required('admin')
def courses_with_min_students(min_students):
    """Return courses with at least min_students enrolled."""
    try:
        db_conn = connectDB()
        cursor = db_conn.cursor()

        query = """
        SELECT c.CID, c.CName, COUNT(e.StudID) AS student_count
        FROM CMS_Courses c
        JOIN CMS_Enrolment e ON c.CID = e.CID
        GROUP BY c.CID, c.CName
        HAVING student_count >= %s
        ORDER BY student_count DESC
        """
        cursor.execute(query, (min_students,))
        results = cursor.fetchall()

        courses = []
        for cid, cname, count in results:
            courses.append({
                "CourseID": cid,
                "CourseName": cname,
                "StudentCount": count
            })

        cursor.close()
        db_conn.close()
        return jsonify(courses)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app_views.route('/api/reports/students/min_courses/<int:min_courses>', methods=['GET'])
@login_required
@role_required('admin')
def students_with_min_courses(min_courses):
    """Return students enrolled in at least min_courses."""
    try:
        db_conn = connectDB()
        cursor = db_conn.cursor()

        query = """
        SELECT s.StudID, s.FirstName, s.LastName, COUNT(e.CID) AS course_count
        FROM CMS_Students s
        JOIN CMS_Enrolment e ON s.StudID = e.StudID
        GROUP BY s.StudID, s.FirstName, s.LastName
        HAVING course_count >= %s
        ORDER BY course_count DESC
        """
        cursor.execute(query, (min_courses,))
        results = cursor.fetchall()

        students = []
        for sid, fname, lname, count in results:
            students.append({
                "StudentID": sid,
                "FirstName": fname,
                "LastName": lname,
                "CourseCount": count
            })

        cursor.close()
        db_conn.close()
        return jsonify(students)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app_views.route('/api/reports/lecturers/min_courses/<int:min_courses>', methods=['GET'])
@login_required
@role_required('admin')
def lecturers_with_min_courses(min_courses):
    """Return lecturers teaching at least min_courses."""
    try:
        db_conn = connectDB()
        cursor = db_conn.cursor()

        query = """
        SELECT l.LecID, l.LFirstName, l.LLastname, COUNT(t.CID) AS course_count
        FROM CMS_Lecturers l
        JOIN CMS_Teaches t ON l.LecID = t.LecID
        GROUP BY l.LecID, l.LFirstName, l.LLastname
        HAVING course_count >= %s
        ORDER BY course_count DESC
        """
        cursor.execute(query, (min_courses,))
        results = cursor.fetchall()

        lecturers = []
        for lid, fname, lname, count in results:
            lecturers.append({
                "LecturerID": lid,
                "FirstName": fname,
                "LastName": lname,
                "CourseCount": count
            })

        cursor.close()
        db_conn.close()
        return jsonify(lecturers)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app_views.route('/api/reports/courses/most_enrolled', methods=['GET'])
@login_required
@role_required('admin')
def top_10_most_enrolled_courses():
    """Return top 10 courses by enrollment count."""
    try:
        db_conn = connectDB()
        cursor = db_conn.cursor()

        query = """
        SELECT c.CID, c.CName, COUNT(e.StudID) AS student_count
        FROM CMS_Courses c
        JOIN CMS_Enrolment e ON c.CID = e.CID
        GROUP BY c.CID, c.CName
        ORDER BY student_count DESC
        LIMIT 10
        """
        cursor.execute(query)
        results = cursor.fetchall()

        courses = []
        for cid, cname, count in results:
            courses.append({
                "CourseID": cid,
                "CourseName": cname,
                "StudentCount": count
            })

        cursor.close()
        db_conn.close()
        return jsonify(courses)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app_views.route('/api/reports/students/top_averages', methods=['GET'])
@login_required
@role_required('admin')
def top_10_students_by_average():
    """Return top 10 students with highest average grade."""

    # Assuming grades are stored as letters or numbers, this requires some normalization.
    # For this example, let's assume grades are numeric strings. Adjust as needed.

    try:
        db_conn = connectDB()
        cursor = db_conn.cursor()

        # Calculate average numeric grade per student, ignoring NULL grades
        query = """
        SELECT s.StudID, s.FirstName, s.LastName, AVG(CAST(sub.Grade AS DECIMAL(5,2))) AS avg_grade
        FROM CMS_Students s
        JOIN CMS_Submissions sub ON s.StudID = sub.SID
        WHERE sub.Grade IS NOT NULL AND sub.Grade != ''
        GROUP BY s.StudID, s.FirstName, s.LastName
        ORDER BY avg_grade DESC
        LIMIT 10
        """
        cursor.execute(query)
        results = cursor.fetchall()

        students = []
        for sid, fname, lname, avg_grade in results:
            students.append({
                "StudentID": sid,
                "FirstName": fname,
                "LastName": lname,
                "AverageGrade": float(avg_grade) if avg_grade is not None else None
            })

        cursor.close()
        db_conn.close()
        return jsonify(students)

    except Exception as e:
        return jsonify({"error": str(e)}), 500