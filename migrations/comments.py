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
    # User id , Comment , Post id
    cursor.execute("CREATE TABLE comments(id int primary key auto_increment, user_id int not null, comment longtext not null, post_id int not null);")
    db.commit()