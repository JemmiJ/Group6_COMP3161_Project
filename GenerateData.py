from faker import Faker
import random

fake = Faker()
max_lecturers = 50
max_courses = 200
max_students = 100000
students= []
lecturers = []
courses = []
enrolls = []
Faculty = ('Science and Technology', 'Social Sciences', 'Medical Sciences')
Science_tech = ('Biology', 'Chemistry', 'Mathematics', 'Computing', 'Biochemistry', 'Marine Biology', 'Geography', 'Physics', 'Geology')
social_sci = ('Sociology', 'Economics', 'Psychology', 'Government')
medical_sci = ('Pathology', 'Radiology', 'Pscychiatry', 'Gynaecology')
Prefix = ("Introduction to ", "Advanced ", "Fundamentals of ", "Principles of ", "Applied ")
Level = ("I", "II", " III", " IV", "V")

def generate_lecturer(max_lec):
    for _ in range(max_lec):
        lec_id = fake.random_int(min=000000,max=999999)
        faculty = random.choice(Faculty)
        if faculty == 'Science and Technology':
            department = random.choice(Science_tech)
            lecturers.append((lec_id, fake.unique.first_name(), fake.unique.last_name(), department))
        if faculty == 'Social Sciences':
            department = random.choice(social_sci)
            lecturers.append((lec_id, fake.unique.first_name(), fake.unique.last_name(), department))
        if faculty == 'Medical Sciences':
            department = random.choice(medical_sci)
            lecturers.append((lec_id, fake.unique.first_name(), fake.unique.last_name(), department))
    return lecturers

def generate_courses(c_range):
    for _ in range(c_range):
        eligible = []
        while not eligible:
            course_id = fake.unique.random_int()
            faculty = random.choice(Faculty)
            if faculty == 'Science and Technology':
                department = random.choice(Science_tech)
                cName = random.choice(Prefix) + department + fake.random_element(Level)
                cCode = department[:4].upper() + str(fake.unique.random_int(min=1000, max=9999))
                eligible = [lec[0] for lec in lecturers if lec[3] == department]
            if faculty == 'Social Sciences':
                department = random.choice(social_sci)
                cName = random.choice(Prefix) + department + fake.random_element(Level)
                cCode = department[:4].upper() + str(fake.unique.random_int(min=1000, max=9999))
                eligible = [lec[0] for lec in lecturers if lec[3] == department]
            if faculty == 'Medical Sciences':
                department = random.choice(medical_sci)
                cName = random.choice(Prefix) + department + fake.random_element(Level)
                cCode = department[:4].upper() + str(fake.unique.random_int(min=1000, max=9999))
                eligible = [lec[0] for lec in lecturers if lec[3] == department]
                
        lec_Id = random.choice(eligible)
        courses.append((course_id, cName, cCode, lec_Id))
    return courses

def generate_course_lec():
    lecturer_courses = {lec[0] : [] for lec in lecturers}
    for course in courses:
        lecturer_courses[course[3]].append(course[0])

def generate_students(S_range):
    for _ in range(S_range):
        stu_id = int('6201' + str(fake.random_int(min=10000,max=99999)))
        students.append((stu_id,fake.first_name(),fake.last_name()))
        registered_courses = random.sample(courses,5)
        for course in registered_courses:
            grade = random.randint(50, 100)
            enrolls.append((stu_id, course[0], grade))
    return students, enrolls

def SQL_storage():
    
    with open("Group6_GenerationFile.sql", 'w') as f:
        f.write("INSERT INTO CMS_Students (StudID, FirstName, LastName) VALUES\n")
        f.write(",\n".join([str(tuple(student)) for student in students]) + ";\n\n")

        f.write("INSERT INTO CMS_CourseS (CID, CName, CCode, CDepartment, LecID) VALUES\n")
        f.write(",\n".join([str(tuple(course)) for course in courses]) + ";\n\n")

        f.write("INSERT INTO CMS_Lecturers (LecID, LFirstName, LLastName, Department) VALUES\n")
        f.write(",\n".join([str(tuple(lec)) for lec in lecturers]) + ";\n\n")

        f.write("INSERT INTO CMS_Enrolment (StudID, CID, Grade) VALUES\n")
        f.write(",\n".join([str(tuple(enrol)) for enrol in enrolls]) + ";\n\n")
    print("Data File Generated Successfully")

        

def main():
    generate_lecturer(max_lecturers)
    generate_courses(max_courses)
    generate_course_lec()
    generate_students(max_students)
    SQL_storage()

if __name__ == "__main__":
    main()