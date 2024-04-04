from flask import redirect, render_template, session
from functools import wraps


def pageApology(message, code=400):
    """ Apology message for user | EXAMPLE : Invalid Username etc... """
    return render_template("apologyPage.html", top=code, bottom=(message)), code

def loginRequired(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("usr_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def isAdmin(f):
    # ADMIN STYLE PAGES

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("usr_id") != 1:
            session["isAdmin"] = False
        else:
            session["isAdmin"] = True
        return f(*args, **kwargs)
    return decorated_function
    # make check if username is in list of names/ids // nope


def isAdminPage(f):
    # ACTUAL ADMIN PAGES

    def decorated_function(*args, **kwargs):
        if session.get("usr_id") != 1:
            return redirect("/usrMainPage")
        return f(*args, **kwargs)
    return decorated_function