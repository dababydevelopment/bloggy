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

  cursor.execute("CREATE TABLE posts(id int primary key auto_increment, title tinytext not null, content longtext not null, user_id int not null);")
  db.commit()