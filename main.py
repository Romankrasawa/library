import sqlite3
from flask import *
import datetime
import os
from Dbase import *
from werkzeug.security import generate_password_hash, check_password_hash


DATABASE='site.db'
DEBUG=True
SECRET_KEY='fdgfh78@#5?>gfhf89dx, v06k'

app=Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path,'site.db')))

def connect_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('create_tables.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'Link_db'):
        g.link_db.close()



@app.route("/home")
@app.route("/")
def home():
    db = get_db()
    dbase = FDataBase(db)
    return render_template("homepage.html", title="School Library Home", description = dbase.home_books())


@app.route("/picture/<id>", methods = ['POST','GET'])
def showpicture(id):
    db = get_db()
    dbase = FDataBase(db)
    image = dbase.getpicture(id)
    return Response(image, mimetype='image/png')

@app.errorhandler(404)
def errorpage(error) :
    return render_template("errorpage.html", title="Error 404")



@app.route("/about")
def about():
    return render_template("aboutsite.html", title="About site")



@app.route("/chat/<code>", methods = ['POST','GET'])
def chat(code):
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        print(code)
        print(dbase.add_massage(request.form["massage"], datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S"), int(code)))
        return redirect(url_for("chat", code = code))
    print(code)
    for i in dbase.checkmassages(code):
        print(i)
    return render_template("chat.html", title="Library chat", massages = dbase.checkmassages(code), description = dbase.search_id(code), id = code)



@app.route("/search", methods = ['POST','GET'])
def search():
    if request.method == "POST":
        if request.form['searchbar'] == "":
            return redirect("/home")
        elif request.form['searchbar'][0] == "#":
            print(request.form['searchbar'][1:])
            return redirect(f"/search_id={request.form['searchbar'][1:]}")
        else:
            return redirect(f"/search={request.form['searchbar'].replace(' ', '_')}")
    else:
         return redirect("/home")

@app.route("/search_id=<searchid>")
def searchbyid(searchid):
    db = get_db()
    dbase = FDataBase(db)
    print(searchid)
    return render_template("search.html", title=f"Search {searchid}".replace('_', ' '), search=dbase.search_id(searchid))

@app.route("/search=<searchbar>")
def searchthing(searchbar):
    db = get_db()
    dbase = FDataBase(db)
    return render_template("search.html", title=f"Search {searchbar}".replace('_', ' '), search = dbase.search(searchbar))



@app.route("/register", methods = ['POST','GET'])
def register():
    if request.method == "POST":
        db = get_db()
        dbase = FDataBase(db)
        dbase.registrate(request.form["username"],request.form["email"],generate_password_hash(request.form["password"]))
        return redirect("login")
    return render_template("register.html", title="Registration")



@app.route("/login", methods = ['POST','GET'])
def login():
    if request.method == "POST":
        return redirect(f"/account/{request.form['username']}")
    else:
        return render_template("login.html", title="Log in")



@app.route("/account/<username>")
def account(username):
    return render_template("account.html", title="Your Account" , user=username)



@app.route("/errorpage")
def errorpage():
    return render_template("errorpage.html", title="Error")



@app.route("/addbook", methods = ['POST','GET'])
def addbook():
    if request.method == "POST":
        db = get_db()
        dbase = FDataBase(db)
        if dbase.add_book(request.form["name"], request.form["author"], int(request.form["years"]), int(request.form["pages"]), request.form["company"], request.files["cover"].read()):
            return redirect("home")
    return render_template("addbook.html", title="Add book")



@app.route("/account/<username>/changeavatar")
def changeavatar(username):
    return render_template("account.html", title="Account", user=username)



@app.route("/account/<username>/changepassword")
def changepassword(username):
    return render_template("account.html", title="Account", user= username)



if __name__ == "__main__":
    create_db()
    app.run(debug=True)