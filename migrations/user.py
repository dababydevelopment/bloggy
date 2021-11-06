import mysql.connector

def run():
    db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="OwenKL611",
    database="blog",
    auth_plugin='mysql_native_password'
    )

    cursor = db.cursor()
    cursor.execute("CREATE TABLE user(username VARCHAR(255) not null unique, id int not null primary key auto_increment, password longtext not null);")
    db.commit()

"""

(in migrations)
Make a user table with username, password, and id. 
Modify the comments and posts table and add a user id column.

"""