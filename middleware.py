from flask import redirect, session

def is_logged_in():
    if session.get("username", False) == False:
        return False
    else:
        return True

def is_author(user_id):
    if session.get("user_id") == user_id:
        return True
    else:
        return False