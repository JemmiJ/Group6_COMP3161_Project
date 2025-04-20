CREATE DATABASE CourseManagementSystem;
USE CourseManagementSystem;

CREATE TABLE CMS_Account (
	AccID INT PRIMARY KEY AUTO_INCREMENT,
    AccName INT,
    AccPassword VARCHAR(512)
);

CREATE TABLE CMS_Admin (
	AdminID INT PRIMARY KEY,
    AdminName VARCHAR(255)
);

CREATE TABLE CMS_Students (
	StudID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(100)
);

CREATE TABLE CMS_Lecturers (
	LecID INT PRIMARY KEY,
    LFirstName VARCHAR(50),
    LLastname VARCHAR(100),
    Department VARCHAR (50)
);

CREATE TABLE CMS_Courses (
	CID INT PRIMARY KEY,
    CName VARCHAR(255),
    CCode VARCHAR(50),
    CDepartment VARCHAR(50),
    LecID INT,
    
    FOREIGN KEY(LecID)
    REFERENCES CMS_Lecturers(LecID)
    ON DELETE CASCADE
);

CREATE TABLE CMS_Enrolment (
	StudID INT,
    CID INT,
    Grade VARCHAR(5),
    
    PRIMARY KEY(StudID, CID),
    
    FOREIGN KEY(StudID)
    REFERENCES CMS_Students(StudID)
    ON DELETE CASCADE,
    
    FOREIGN KEY(CID)
    REFERENCES CMS_Courses(CID)
    ON DELETE CASCADE
);

CREATE TABLE CMS_Teaches (
	LecID INT,
    CID INT, 
    
	PRIMARY KEY(LecID, CID),
    
    FOREIGN KEY(LecID)
    REFERENCES CMS_Lecturers(LecID)
    ON DELETE CASCADE,
    
    FOREIGN KEY(CID)
    REFERENCES CMS_Courses(CID)
    ON DELETE CASCADE
);

CREATE TABLE  CMS_Student_Account (
	StudAccName INT,
    StudentPassword VARCHAR(512),
    
    FOREIGN KEY(StudAccName)
    REFERENCES CMS_Students(StudID)
    ON DELETE CASCADE
);

CREATE TABLE  CMS_Lecturer_Account (
	LecAccName INT,
    LecturerPassword VARCHAR(512),
    
    FOREIGN KEY(LecAccName)
    REFERENCES CMS_Lecturers(LecID)
    ON DELETE CASCADE
);

CREATE TABLE CMS_Events(
	eventID INT AUTO_INCREMENT PRIMARY KEY,
    CourseID INT,
    eventDate DATETIME,
    eventDescription TEXT,
    
    FOREIGN KEY(CourseID)
    REFERENCES CMS_Courses(CID)
    ON DELETE CASCADE
);

CREATE TABLE CMS_CourseContent (
	ContentId INT AUTO_INCREMENT PRIMARY KEY,
    CourseID INT,
    section VARCHAR(100) NOT NULL,
    content TEXT,
    contentType ENUM('link', 'file', 'slides'),
    
	FOREIGN KEY(CourseID)
    REFERENCES CMS_Courses(CID)
    ON DELETE CASCADE
);

CREATE TABLE CMS_Assignments (
	AssignId INT PRIMARY KEY AUTO_INCREMENT,
	CourseID INT,
    Title VARCHAR(100) NOT NULL,
    Description TEXT,
    DueDate DATETIME,
    
    FOREIGN KEY(CourseID)
    REFERENCES CMS_Courses(CID)
    ON DELETE CASCADE
);

CREATE TABLE CMS_Submissions (
	SUBid INT PRIMARY KEY AUTO_INCREMENT,
    AID INT,
    SID INT,
    SubmissionDATE DATETIME DEFAULT CURRENT_TIMESTAMP,
    Grade VARCHAR(5),
    Feedback TEXT,
    
    FOREIGN KEY (AID)
    REFERENCES CMS_Assignments(AssignId)
    ON DELETE CASCADE,
    
    FOREIGN KEY(SID)
    REFERENCES CMS_Students(StudID)
    ON DELETE CASCADE
    
);

CREATE TABLE CMS_Forums (
	ForumID INT PRIMARY KEY AUTO_INCREMENT,
    ForumCourseID INT,
    ForumName VARCHAR(50),
    
    FOREIGN KEY(ForumCourseID)
    REFERENCES CMS_Courses(CID)
    ON DELETE CASCADE
);

CREATE TABLE CMS_Threads (
	TID INT PRIMARY KEY AUTO_INCREMENT, 
    ForumID INT,
    CreatorID INT,
    Title VARCHAR(255),
    Content TEXT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY(ForumID) 
    REFERENCES CMS_Forums(ForumID)
    ON DELETE CASCADE,
    
    FOREIGN KEY(CreatorID)
    REFERENCES CMS_Account(AccID)
    ON DELETE CASCADE
);

CREATE TABLE CMS_Comments (
	commentID INT AUTO_INCREMENT PRIMARY KEY,
    ThreadID INT,
    AuthorID INT,
    Content TEXT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY(ThreadID)
    REFERENCES CMS_Threads(TID)
    ON DELETE CASCADE,
    
    FOREIGN KEY(AuthorID)
    REFERENCES CMS_Account(AccID)
    ON DELETE CASCADE
);

