import sqlite3 as sq
from flask import *
import datetime

app = Flask(__name__)


with sq.connect("tmp/site.db") as con:
    cur = con.cursor()
    codes = [str(i).zfill(6) for i in range(1,22)]

    CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'

    @app.route("/home")
    @app.route("/")
    def home():
        return render_template("homepage.html", title="School Library Home", code = codes)

    @app.errorhandler(404)
    def errorpage(error) :
        return render_template("errorpage.html", title="Error 404")

    @app.route("/about")
    def about():
        return render_template("aboutsite.html", title="About site")

    @app.route("/chat/<code>", methods = ['POST','GET'])
    def chat(code):
        if request.method == "POST":
            return render_template("chat.html", title="Library chat", datetime = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), text=request.form["massage"])
        else:
            return render_template("chat.html", title="Library chat", datetime = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), text="")

    @app.route("/search")
    def search():
        return render_template("search.html", title="Search")

    @app.route("/register")
    def register():
        return render_template("register.html", title="Registration")

    @app.route("/login")
    def login():
        return render_template("login.html", title="Log in")

    @app.route("/account/<username>")
    def account(username):
        return render_template("account.html", title="Your Account" , user=username)

    @app.route("/errorpage")
    def errorpage():
        return render_template("errorpage.html", title="Error")

    @app.route("/addbook")
    def addbook():
        return render_template("addbook.html", title="Add book")
    @app.route("/account/<username>/changeavatar")
    def changeavatar(username):
        return render_template("account.html", title="Account", user=username)

    @app.route("/account/<username>/changepassword")
    def changepassword(username):
        return render_template("account.html", title="Account", user= username)
    if __name__ == "__main__":
        app.run(debug=True)
