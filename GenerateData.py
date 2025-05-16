from faker import Faker
import random

fake = Faker()
max_lecturers = 50
max_courses = 200
max_students = 100000
next_AccID = 62000
accounts = []
students= []
lecturers = []
courses = []
enrolls = []
Faculty = ('Science and Technology', 'Social Sciences', 'Medical Sciences')
Science_tech = ('Biology', 'Chemistry', 'Mathematics', 'Computing', 'Biochemistry', 'Marine Biology', 'Geography', 'Physics', 'Geology')
social_sci = ('Sociology', 'Economics', 'Psychology', 'Government')
medical_sci = ('Pathology', 'Radiology', 'Pscychiatry', 'Gynaecology')
Prefix = ("Introduction to ", "Advanced ", "Fundamentals of ", "Principles of ", "Applied ")
Level = (" I", " II", " III", " IV", " V")

def generate_lecturer(max_lec):
    for _ in range(max_lec):
        lec_id = fake.unique.random_int() ## Gets the ID from the ID, Password tuple
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
        courses.append((course_id, cName, cCode, department, lec_Id))
    return courses

def generate_course_lec():
    lecturer_courses = {lec[0] : [] for lec in lecturers}
    for course in courses:
        lecturer_courses[course[4]].append(course[0])

def generate_students(S_range):
    next_AccID = 62000
    for _ in range(S_range):
        AccID = next_AccID
        next_AccID += 1
        stu_id = AccID
        students.append((stu_id,fake.first_name(),fake.last_name()))
        registered_courses = random.sample(courses,5)
        for course in registered_courses:
            grade = random.randint(50, 100)
            enrolls.append((stu_id, course[0], grade))
    return students, enrolls

def generate_accounts():
    next_AccID = 62000  # Starting Account ID
    global accounts
    accounts = []  # Initialize accounts list
    # Generate candidate passwords - generate twice as many to increase chances of unique long passwords
    candidate_passwords = [fake.password(length=10) for _ in range(max_students * 2)]
    # Filter passwords: length >= 8 and unique
    filtered_passwords = []
    seen_passwords = set()
    for pwd in candidate_passwords:
        pwd_cap = pwd.capitalize()
        if len(pwd_cap) >= 8 and pwd_cap not in seen_passwords:
            seen_passwords.add(pwd_cap)
            filtered_passwords.append(pwd_cap)
        if len(filtered_passwords) == max_students:
            break
    # Create accounts pairing IDs and passwords
    for i in range(max_students):
        AccID = next_AccID + i
        AccPassword = filtered_passwords[i]
        accounts.append((AccID, AccPassword))
    return accounts



def SQL_storage():
    word = fake.word().capitalize()
    print("Fake Word:", word)
    with open("Group6_GenerationFile.sql", 'w') as f:
        f.write("INSERT INTO CMS_Account (AccID, AccPassword) VALUES\n")
        f.write(",\n".join([str(tuple(account)) for account in accounts]) + ";\n\n")

        f.write("INSERT INTO CMS_Students (StudID, FirstName, LastName) VALUES\n")
        f.write(",\n".join([str(tuple(student)) for student in students]) + ";\n\n")

        f.write("INSERT INTO CMS_Lecturers (LecID, LFirstName, LLastName, Department) VALUES\n")
        f.write(",\n".join([str(tuple(lec)) for lec in lecturers]) + ";\n\n")

        f.write("INSERT INTO CMS_CourseS (CID, CName, CCode, CDepartment, LecID) VALUES\n")
        f.write(",\n".join([str(tuple(course)) for course in courses]) + ";\n\n")

        f.write("INSERT INTO CMS_Enrolment (StudID, CID, Grade) VALUES\n")
        f.write(",\n".join([str(tuple(enrol)) for enrol in enrolls]) + ";\n\n")
    print("Data File Generated Successfully")
     
if __name__ == "__main__":
    generate_lecturer(max_lecturers)
    generate_courses(max_courses)
    generate_course_lec()
    generate_students(max_students)
    generate_accounts()
    SQL_storage()