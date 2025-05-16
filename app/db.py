import pymysql
import os

def connectDB():
    return pymysql.connect(
        user='CMS_ADMIN', 
        password= os.environ.get('PASSWORD'), 
        host='localhost', 
        database='CourseManagementSystem',
    )