import webapp2
import cgi
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Sign Up Page</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
        <h1>
            Please. Sign. Up.
        </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

form  = """
<form method="post">
    <label>
        Username:
        <input type="text" name="username" value="%(username)s"/>
    </label>
    <div style="color: red">%(error1)s</div>
    <br>
    <label>
        Password:
        <input type="password" name="password" value=""/>
    </label>
    <div style="color: red">%(error2)s</div>
    <br>
    <label>
        Verify Password:
        <input type="password" name="verify" value=""/>
    </label>
    <div style="color: red">%(error3)s</div>
    <br>
    <label>
        Email (optional):
        <input type="text" name="email" value="%(email)s"/>
    </label>
    <div style="color: red">%(error4)s</div>
    <br>
    <br>
    <input type="submit" value="Submit"/>
</form>
"""
content = page_header + form + page_footer

def escape_html(s):
    return cgi.escape(s, quote = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password)

def valid_verify(verify, password):
    return verify == password


EMAIL_RE = re.compile("[^@]+@[^@]+\.[^@]+")
def valid_email(email):
    if email:
        return EMAIL_RE.match(email)
    else:
        return True



class MainHandler(webapp2.RequestHandler):

    def write_form(self, username="", error1="", error2="", email="", error3="", error4=""):

        self.response.out.write(content % {"username": username,
                                           "error1": error1,
                                           "error2": error2,
                                           "email": email,
                                           "error3": error3,
                                           "error4": error4
                                           })

    def get(self):
        self.write_form()


    def post(self):
        have_error = False
        user_name = self.request.get("username")
        user_password = self.request.get("password")
        user_verify = self.request.get("verify")
        user_email = self.request.get("email")

        username = valid_username(user_name)
        password = valid_password(user_password)
        email = valid_email(user_email)
        matches = valid_verify(user_password, user_verify)


        if username and password and email and matches:
            self.redirect("/welcome?username=" + user_name)

        else:

            if not username:
                error1 = "That's not a valid username."
            else:
                error1 = ""

            if not password:
                error2 = "That's not a valid password."
            else:
                error2 = ""

            if not matches:
                error3 = "Your password doesn't match."
            else:
                error3 = ""
            if not email:
                error4 = "That's not a valid email."
            else:
                error4 = ""

            self.write_form(user_name, error1, error2, user_email, error3, error4)


class WelcomeHandler(webapp2.RequestHandler):

    def get(self):

        username = self.request.get('username')

        if valid_username(username):
            welcome = "Welcome " + username + "!!"
            self.response.write(welcome)

        else:
            self.redirect('/')




app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
