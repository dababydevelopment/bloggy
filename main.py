from flask import Flask, request, render_template, redirect, session
from flask_session import Session
import mysql.connector
import middleware
import hashlib
app = Flask(__name__, '', 'public/')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.context_processor
def inject_username():
  username = session.get("username", False)
  user_id = session.get("user_id", False)
  return dict(username=username)

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="OwenKL611",
  database="blog",
  auth_plugin='mysql_native_password'
)

cursor = db.cursor()

@app.route('/')
def home():
  if session.get("user_id",False):
    return render_template("me/me.html")
  else:
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(temp):
    return render_template('404.html')


@app.route('/posts/create')
def create():
  if middleware.is_logged_in():
    return render_template("/posts/create.html")
  else:
    return redirect("/login")
    
@app.route('/posts',methods=['GET', 'POST'])
def route():
    if request.method == 'POST':
      if middleware.is_logged_in():
        #create a post within the posts table
        title=request.form['title']
        content=request.form['content']
        #once the post is in the db, redirect to /
        command = "INSERT INTO posts(title, content, user_id) VALUES('"+title+"', '"+content+"', '"+str(session.get("user_id"))+"');"
        cursor.execute(command)
        db.commit()
        return redirect('/')
      else:
        return redirect('/login')
    else:
      cursor.execute("select * from posts;")
      posts=cursor.fetchall()
      return render_template("/posts/index.html",posts=posts)

    #be able to go to /posts/{id}, and display the content and title for that id

@app.route('/posts/<id>/edit')
def edit(id):
  cursor.execute("select * from posts WHERE id="+id+";")
  post=cursor.fetchall()
  if middleware.is_author(post[0][3]):
    return render_template("/posts/edit.html",post=post)
  else:
    return redirect('/posts/'+id)

@app.route('/posts/<id>',methods=["POST","GET"])
def update(id):
  cursor.execute("select * from posts WHERE id="+id+";")
  post=cursor.fetchall()
  if request.method == "GET":
    cursor.execute("select * from comments WHERE post_id="+id+";")
    comments = cursor.fetchall()
    return render_template("/posts/show.html",post=post, comments=comments)
  elif request.form['_method']=="PUT":
    if middleware.is_author(post[0][3]):
      cursor.execute("UPDATE posts SET title='"+request.form['title']+"', content='"+request.form['content']+"' WHERE id="+id+";")
      db.commit()
      return redirect('/posts')
    else:
      return redirect('/posts')
  elif request.form['_method']=="DELETE":
    if middleware.is_author(post[0][3]):
      cursor.execute("DELETE from posts where id="+id+";")
      db.commit()
    return redirect('/posts')
#when making a new comment, ensure the person is logged in
#when editing or deleting a comment, ensure the person who is logged in is the author
#when making a comment, ensure to fill the user_id column. If that column doesn't exist, make it in the migration
@app.route('/posts/<post_id>/comments/<comment_id>/edit',methods=['GET'])
def edit_comment(post_id,comment_id):
  cursor.execute("SELECT * FROM comments WHERE post_id="+post_id+" AND id="+comment_id+";")
  comment=cursor.fetchall()
  user_id = session.get("user_id",False)
  if user_id != False and comment[0][1]==user_id:
    return render_template('/comments/edit_comment.html',id=post_id,comment=comment)
  else:
    return redirect('/login')

@app.route('/posts/<post_id>/comments/<comment_id>',methods=['POST'])
def update_comment(post_id,comment_id):
  if request.form['_method']=='PUT':
    cursor.execute("SELECT * FROM comments WHERE post_id="+post_id+" AND id="+comment_id+";")
    comment=cursor.fetchall()[0]
    user_id = session.get("user_id",False)
    if user_id != False and comment[1]==user_id:
      cursor.execute("UPDATE comments SET comment='"+request.form['comment']+"' WHERE id='"+comment_id+"' AND post_id='"+post_id+"';")
      db.commit()
      return redirect('/posts/'+post_id)
    else:
      return redirect('/login')
  elif request.form['_method'] == 'DELETE':
    cursor.execute("SELECT * FROM comments WHERE post_id="+post_id+" AND id="+comment_id+";")
    comment=cursor.fetchall()[0]
    user_id = session.get("user_id",False)
    if user_id != False and comment[1]==user_id:
      cursor.execute("DELETE from comments WHERE id="+comment_id+" AND post_id="+post_id)
      db.commit()
      return redirect('/posts/'+post_id)
    else:
      return redirect('/login')

@app.route('/posts/<id>/comments',methods=["POST"])
def comments(id):
  user_id=session.get("user_id",False)
  if user_id:
    comment=request.form['comment']
    cursor.execute("INSERT INTO comments(post_id,user_id,comment) VALUES('"+id+"', '"+str(user_id)+"', '"+comment+"')")
    db.commit()
    return redirect('/posts/' + id)
  else:
    return redirect('/login')


@app.route('/register',methods=["GET","POST"])
def register():
  if request.method == 'GET':
    return render_template('/auth/register.html')
  elif request.method == 'POST':
    username = request.form['username']
    password = hashlib.sha256(str.encode(request.form['password']))
    cursor.execute("INSERT INTO user(username, password) VALUES('"+username+"', '"+password.hexdigest()+"')")
    db.commit()
    return redirect('/')
    
@app.route('/login',methods=["GET","POST"])
def login():
  if request.method == 'GET':
    return render_template('/auth/login.html')
  elif request.method == 'POST':
    username = request.form['username']
    password = hashlib.sha256(str.encode(request.form['password']))
    cursor.execute("SELECT * FROM user WHERE username='"+username+"' AND password='"+password.hexdigest()+"'")
    user = cursor.fetchall()
    if user:
      session["username"] = username
      session["user_id"] = user[0][1]
    else:
      return render_template('/auth/invalid_credential.html')
    return redirect('/')
  
@app.route('/logout',methods=["GET"])
def logout():
  session.clear()
  return redirect('/')


@app.route('/me', methods=["GET"])
def me():
  return render_template('/me/me.html')

@app.route('/profile', methods=["GET"])
def profile():
  return render_template('/me/profile.html')

@app.route('/posts/search')
def search():
  #/posts/search?query=21321
  title = request.args.get("query")
  cursor.execute("SELECT * FROM posts WHERE title LIKE '%"+title+"%';")
  #SELECT * from {table} WHERE {column} LIKE '%{value}%'
  posts = cursor.fetchall()
  return render_template('/posts/search.html',posts=posts,search=title)

app.run(port=8000) #this will host this code on http://localhost:8000