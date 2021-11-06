from mysql.connector.errors import ProgrammingError
import comments 
import posts
import user

__name__ = '__main__'

try:    
    comments.run()
except Exception as error:
    print(error)

try:
    posts.run()
except Exception as error:
    print(error)

try:
    user.run()
except Exception as error:
    print(error)
