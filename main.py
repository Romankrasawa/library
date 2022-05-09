import sqlite3 as sq
from flask import Flask, render_template

app = Flask(__name__)

with sq.connect("tmp/site.db") as con:
    cur = con.cursor()

    @app.route("/home")
    @app.route("/")
    def home():
        return render_template("homepage.html", title="School Library Home")

    @app.route("/about")
    def about():
        return render_template("aboutsite.html", title="About site")

    @app.route("/chat")
    def chat():
        return render_template("chat.html", title="Library chat")

    @app.route("/search")
    def search():
        return render_template("search.html", title="Search")

    @app.route("/register")
    def register():
        return render_template("register.html", title="Registration")

    @app.route("/login")
    def login():
        return render_template("login.html", title="Log in")

    @app.route("/account")
    def account():
        return render_template("account.html", title="Your Account")

    @app.route("/errorpage")
    def errorpage():
        return render_template("errorpage.html", title="Error")

    @app.route("/addbook")
    def addbook():
        return render_template("addbook.html", title="Add book")

    if __name__ == "__main__":
        app.run(debug=True)
