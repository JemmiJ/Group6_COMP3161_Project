
import pymysql
from app import app
def connectDB():
    return pymysql.connect(
        user='CMS_ADMIN', 
        password= app.config['PASSWORD'], 
        host='localhost', 
        database='CourseManagementSystem',
        auth_plugin='mysql_native_password'
    )