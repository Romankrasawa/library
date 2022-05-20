import sqlite3
from flask import *
import datetime
import os
from Dbase import *
from werkzeug.security import generate_password_hash, check_password_hash
from math import ceil
from flask_login import *
from userLogin import *
from random import randint



DATABASE='site.db'
DEBUG=True
SECRET_KEY='fdgfh78@#5?>gfhf89dx, v06k'

app=Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path,'site.db')))

login_manager=LoginManager(app)

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

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    dbase = FDataBase(db)
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)

@app.route("/home")
@app.route("/")
def home():
    print(current_user)
    if current_user.get_id() == None:
        print("bad")
    db = get_db()
    dbase = FDataBase(db)
    return render_template("homepage.html", title="School Library Home", description = dbase.home_books())


@app.route("/picture/<id>", methods = ['POST','GET'])
def showpicture(id):
    db = get_db()
    dbase = FDataBase(db)
    image = dbase.getpicture(id)
    return Response(image, mimetype='image/png')

@app.route("/avatar", methods = ['POST','GET'])
def showavatar():
    image = current_user.get_avatar()
    print("chotko")
    return Response(image, mimetype='image/png')

@app.errorhandler(404)
def errorpage(error) :
    return render_template("errorpage.html", title="Error 404")



@app.route("/about")
def about():
    return render_template("aboutsite.html", title="About site")

@app.route("/addmassage/<id>", methods = ['POST','GET'])
@login_required
def addmassage(id):
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        print(id)
        print(dbase.add_massage(request.form["massage"], datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S"), id, current_user.get_id()))
        return redirect(url_for("chat", code = id))

@app.route("/chat/<code>", methods = ['POST','GET'])
def chat(code):
    db = get_db()
    dbase = FDataBase(db)
    print(code)
    for i in dbase.checkmassages(code):
        print(i)
    dbase.addview(code)
    return render_template("chat.html", title="Library chat", massages = dbase.checkmassages(code), description = dbase.search_id(code), id = code, current_user=current_user.get_id())



@app.route("/search", methods = ['POST','GET'])
def search():
    if request.method == "POST":
        if request.form['searchbar'] == "":
            return redirect("/home")
        elif request.form['searchbar'][0] == "#":
            print(request.form['searchbar'][1:])
            return redirect(f"/search_id={request.form['searchbar'][1:]}")
        else:
            try:
                sort = request.form['sort']
            except:
                sort = "name-DESC"
            return redirect(f"/search={request.form['searchbar'].replace(' ', '_')}:sort={sort}/page=1")
    else:
         return redirect("/home")

@app.route("/search_id=<searchid>")
def searchbyid(searchid):
    db = get_db()
    dbase = FDataBase(db)
    print(searchid)
    return render_template("search.html", title=f"{searchid}".replace('_', ' '), search=dbase.search_id(searchid), seartchthing = searchid, searching = 1, pages = 1)

@app.route("/search=<searchbar>:sort=<sort>/page=<page>")
def searchthing(searchbar,sort, page):
    db = get_db()
    dbase = FDataBase(db)
    print(searchbar,sort ,page)
    result = dbase.search(searchbar,sort, page)
    search_ = result[0]
    paging = result[1]
    print(search_,paging)
    pages = ceil(paging / 3)
    next = int(page) + 1 if int(page) < pages else page
    prev = int(page) -1 if int(page) > 1 else 1
    return render_template("search.html", title=f"{searchbar}".replace('_', ' '), search = search_, searchthing = searchbar, searching = paging, pages = pages, next = next, prev = prev, sort =sort)



@app.route("/register", methods = ['POST','GET'])
def register():
    if request.method == "POST":
        db = get_db()
        dbase = FDataBase(db)
        with open(f"static/image/deffault_{randint(1,6)}.png", "rb") as img:
            image = img.read()
        dbase.registrate(request.form["username"],request.form["email"],generate_password_hash(request.form["password"]), image)
        return redirect("login")
    return render_template("register.html", title="Registration")



@app.route("/login", methods = ['POST','GET'])
def login():
    if request.method == "POST":
        db = get_db()
        dbase = FDataBase(db)
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['password'], request.form['password']):
            userlogin = UserLogin().create(user)
            print(userlogin)
            login_user(userlogin)
            print("okey")
            return redirect(url_for('home'))
    return render_template("login.html", title="Log in")



@app.route("/account")
@login_required
def account():
    return render_template("account.html", title="Your Account" , user=current_user)



@app.route("/errorpage")
def errorpage():
    return render_template("errorpage.html", title="Error")



@app.route("/addbook", methods = ['POST','GET'])
@login_required
def addbook():
    logout_user()
    if request.method == "POST":
        db = get_db()
        dbase = FDataBase(db)
        if not request.files["cover"].read():
            with open("static/image/deffault_cover.png", "rb") as img:
                image = img.read()
        else:
            image = request.files["cover"].read()
        if dbase.add_book(request.form["name"], request.form["author"], int(request.form["years"]), int(request.form["pages"]), request.form["company"], image):
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