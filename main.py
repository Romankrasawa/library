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
login_manager.login_view = "login"
login_manager.login_message = "Щоб отримати доступ ввійдіть в аккаунт"
login_manager.login_message_category = "error"

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
    db = get_db()
    dbase = FDataBase(db)
    return render_template("homepage.html", title="School Library Home", description = dbase.home_books())


@app.route("/picture/<id>", methods = ['POST','GET'])
def showpicture(id):
    db = get_db()
    dbase = FDataBase(db)
    image = dbase.getpicture(id)
    return Response(image, mimetype='image/png')

@app.route("/avatar/<user_id>", methods = ['POST','GET'])
def showotheravatar(user_id):
    db = get_db()
    dbase = FDataBase(db)
    image = dbase.getavatar(user_id)
    return Response(image, mimetype='image/png')

@app.route("/avatar", methods = ['POST','GET'])
def showmyavatar():
    if current_user.is_authenticated:
        image = current_user.get_avatar()
        print("chotko")
    else:
        with open("static/image/default-profile.png", "rb") as img:
            image = img.read()
    print(image)
    return Response(image, mimetype='image/png')

@app.errorhandler(404)
def errorpage(error) :
    return render_template("errorpage.html", title="Error 404")

@app.route("/logout", methods = ['POST','GET'])
def logout():
    logout_user()
    flash("Ви вийшли з аккаунта", category='success')
    return redirect(url_for("login"))


@app.route("/addmassage/<id>", methods = ['POST','GET'])
@login_required
def addmassage(id):
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        print(id)
        if len(request.form["massage"]) > 0:
            print(dbase.add_massage(request.form["massage"], datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S"), id, current_user.get_id()))
            flash("Ви додали коментар", category='success')
        else:
            flash("Некоректне повідомляення", category='error')
        return redirect(url_for("chat", code = id, page=1))

@app.route("/deletefolow/<id>", methods = ['POST','GET'])
@login_required
def deletefolow(id):
    db = get_db()
    dbase = FDataBase(db)
    print("id =     ",id,current_user.get_folowed())
    if id in current_user.get_folowed():
        dbase.deletefolow(current_user.get_id(),current_user.get_folowed(),id)
        flash("Ця книга була видалена з вподобаних", category='success')
        print('okey')
    else:
        flash("Ця книга уже немає у вподобаних", category='error')
    return redirect(url_for("chat", code = id, page=1))

@app.route("/addfolow/<id>", methods = ['POST','GET'])
@login_required
def addfolow(id):
    db = get_db()
    dbase = FDataBase(db)
    print("id =     ",id,current_user.get_folowed())
    if not id in current_user.get_folowed():
        dbase.addfolow(current_user.get_id(),current_user.get_folowed(),id)
        flash("Ця книга була добавлена до вподобаних", category='success')
    else:
        flash("Ця книга уже у вподобаних", category='error')
    return redirect(url_for("chat", code = id, page=1))

@app.route("/chat/<code>:page=<page>", methods = ['POST','GET'])
def chat(code, page):
    db = get_db()
    dbase = FDataBase(db)
    description = dbase.search_id(code)
    if not description:
        flash("Книга не знайдена", category='error')
        return redirect("/home")
    print(code)
    result = dbase.checkmassages(code, page)
    massages = result[0]
    paging = result[1]
    print(page, paging)
    pages = ceil(paging / 15) if ceil(paging / 15) > 0 else 1
    if 1 > int(page) or int(page) > pages:
        flash("Cторінка не знайдена", category='error')
        return redirect(f"/chat/{code}:page=1")
    next = int(page) + 1 if int(page) < pages else int(page)
    prev = int(page) -1 if int(page) > 1 else 1
    dbase.addview(code)
    if code in current_user.get_folowed():
        liked = True
    else:
        liked =False
    print(paging,page,next,prev)
    return render_template("chat.html", title="Library chat", massages = massages, description = description, id = code, current_user=current_user.get_id(), searching = paging, pages = int(pages), next = next, prev = prev, current_page=int(page), liked=liked)



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
    pages = ceil(paging / 9) if ceil(paging / 9) > 0 else 1
    if 1 > int(page) or int(page) > pages:
        flash("Cторінка не знайдена", category='error')
        return redirect(f"/search={searchbar}:sort={sort}/page=1")
    next = int(page) + 1 if int(page) < pages else int(page)
    prev = int(page) - 1 if int(page) > 1 else 1
    return render_template("search.html", title=f"{searchbar}".replace('_', ' '), search = search_, searchthing = searchbar, searching = paging, pages = pages, next = next, prev = prev, sort =sort, current_page=int(page))

@app.route("/account:created", methods = ["POST"])
@login_required
def create():
    return redirect(f"/account:created:sort={request.form['sort']}/page=1")

@app.route("/account:created:sort=<sort>/page=<page>")
@login_required
def created(sort, page):
    db = get_db()
    dbase = FDataBase(db)
    print(sort ,page)
    result = dbase.created(current_user.get_id(),sort, page)
    search_ = result[0]
    paging = result[1]
    pages = ceil(paging / 9) if ceil(paging / 9) > 0 else 1
    if 1 > int(page) or int(page) > pages:
        flash("Cторінка не знайдена", category='error')
        return redirect(f"/account:created:sort={sort}/page=1")
    next = int(page) + 1 if int(page) < pages else int(page)
    prev = int(page) - 1 if int(page) > 1 else 1
    return render_template("created.html", search = search_, searching = paging, pages = pages, next = next, prev = prev, sort =sort, current_page=int(page))

@app.route("/account:folowed", methods = ["POST"])
@login_required
def folow():
    return redirect(f"/account:folowed:sort={request.form['sort']}/page=1")

@app.route("/account:folowed:sort=<sort>/page=<page>")
@login_required
def folowed(sort, page):
    db = get_db()
    dbase = FDataBase(db)
    print(sort ,page)
    result = dbase.folowed(current_user.get_folowed(),sort, page)
    search_ = result[0]
    paging = result[1]
    pages = ceil(paging / 9) if ceil(paging / 9) > 0 else 1
    if 1 > int(page) or int(page) > pages:
        flash("Cторінка не знайдена", category='error')
        return redirect(f"/account:folowed:sort={sort}/page=1")
    next = int(page) + 1 if int(page) < pages else int(page)
    prev = int(page) - 1 if int(page) > 1 else 1
    return render_template("folowe.html", search = search_, searching = paging, pages = pages, next = next, prev = prev, sort =sort, current_page=int(page))


@app.route("/register", methods = ['POST','GET'])
def register():
    if request.method == "POST":
        db = get_db()
        dbase = FDataBase(db)
        if not "@" in request.form["username"]:
            if not dbase.getUserByUsername(request.form["username"]):
                if not dbase.getUserByEmail(request.form["email"]):
                    if request.form["password"] == request.form["repeatpassword"]:
                        if len(request.form["password"]) >= 8:
                            with open(f"static/image/deffault_{randint(1,6)}.png", "rb") as img:
                                image = img.read()
                            dbase.registrate(request.form["username"],request.form["email"],generate_password_hash(request.form["password"]), image)
                            flash("Ви успішно зареєструвалися", category='success')
                            return redirect("login")
                        else:
                            flash("Введіть пароль довжиною від 8 символів", category='error')
                    else:
                        flash("Паролі не збігаються", category='error')
                else:
                    flash("Така пошта уже існує", category='error')
            else:
                flash("Таке ім'я уже існує", category='error')
        else:
            flash("Некоректне ім'я", category='error')
        return redirect("register")
    return render_template("register.html", title="Registration")



@app.route("/login", methods = ['POST','GET'])
def login():
    if request.method == "POST":
        db = get_db()
        dbase = FDataBase(db)
        if "@" in request.form['email']:
            user = dbase.getUserByEmail(request.form['email'])
        else:
            user = dbase.getUserByUsername(request.form['email'])
        if user:
            if check_password_hash(user['password'], request.form['password']):
                userlogin = UserLogin().create(user)
                print(userlogin)
                print(request.form.get('remember_me'))
                remember_me = True if request.form.get('remember_me') else False
                login_user(userlogin,remember=remember_me)
                print("okey")
                print(remember_me)
                flash("Ви успішно ввійшли в аккаунт", category='success')
                return redirect(url_for('account'))
            else:
                flash("Пароль не підходить", category='error')
        else:
            flash("Не знайдено аккаунт з таким іменем або поштою", category='error')
    if current_user.get_id() == None:
        return render_template("login.html", title="Log in")
    else:
        return redirect(url_for('account'))

@app.route("/profile/<id>")
def profile(id):
    if int(id) == current_user.get_id():
        return redirect("/account")
    print(current_user.get_id())
    db = get_db()
    dbase = FDataBase(db)
    user = dbase.getUserInfo(id)
    if not user:
        flash("Профіль не знайдений", category='error')
        return redirect("/home")
    print("toooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooop")
    username = ''
    for i in user:
        print(i)
        username = i[0]
        aboutme = i[1]
    print("okeey", username)
    return render_template("profile.html", title=f"Profile {username}" , username= username, id = id, aboutme = aboutme)

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
    if request.method == "POST":
        db = get_db()
        dbase = FDataBase(db)
        if not "#" in request.form["name"]:
            if not request.files["cover"]:
                with open("static/image/deffault_cover.png", "rb") as img:
                    image = img.read()
            else:
                image = request.files['cover'].read()
            print(image)
            result, book_id = dbase.add_book(request.form["name"], request.form["author"], int(request.form["years"]), int(request.form["pages"]), request.form["company"], image, current_user.get_id())
            print(result,book_id)
            if result:
                flash("Книга була додана успішно", category='success')
                return redirect((url_for("chat", code = book_id, page=1)))
            else:
                flash("Виникла помилка під час додавання книги", category='error')
        else:
            flash("Некоректна назва", category='error')
    return render_template("addbook.html", title="Add book", current_year =datetime.datetime.now().strftime("%Y"))

@app.route("/changebook/<id>", methods = ['POST','GET'])
@login_required
def changebook(id):
    db = get_db()
    dbase = FDataBase(db)
    description = dbase.search_id(id)
    user_id = 0
    for i in description:
        user_id = i["user_id"]
    if request.method == "POST":
        if not "#" in request.form["name"]:
            if not request.files["cover"]:
                result = dbase.change_book(request.form["name"], request.form["author"], int(request.form["years"]), int(request.form["pages"]), request.form["company"], id)
            else:
                result = dbase.change_book(request.form["name"], request.form["author"], int(request.form["years"]), int(request.form["pages"]), request.form["company"], id, image = request.files['cover'].read())
            if result:
                flash("Книга була змінена успішно", category='success')
                return redirect(url_for("chat", code=id, page=1))
            else:
                flash("Виникла помилка під час зміни книги", category='error')
        else:
            flash("Некоректна назва", category='error')
    if description and user_id == current_user.get_id():
        return render_template("changebook.html", title="Add book", current_year =datetime.datetime.now().strftime("%Y") , information = description, id =id)
    else:
        return redirect("/home")

@app.route("/deletebook/<id>", methods = ['POST','GET'])
@login_required
def deletebook(id):
    db = get_db()
    dbase = FDataBase(db)
    description = dbase.search_id(id)
    user_id = 0
    for i in description:
        user_id = i["user_id"]
    if user_id == current_user.get_id():
        res = dbase.delete_book(id)
        if res:
            flash("Книга була видалена успішно", category='success')
        else:
            flash("Виникла помилка під час видалення книги", category='error')
    return redirect("/home")



@app.route("/account/changedata", methods = ['POST','GET'])
def changedata():
    if request.method == "POST":
        db = get_db()
        dbase = FDataBase(db)
        if check_password_hash(current_user.get_password(), request.form['password']):
            if not "@" in request.form["newusername"]:
                if not (dbase.getUserByUsername(request.form["newusername"]) and request.form["newusername"] != current_user.get_username()):
                    if not (dbase.getUserByEmail(request.form["newemail"]) and request.form["newemail"] != current_user.get_email()):
                        if request.form['newpassword']:
                            if len(request.form["newpassword"]) >= 8:
                                password = generate_password_hash(request.form['newpassword'])
                            else:
                                flash("Введіть пароль довжиною від 8 символів", category='error')
                                return redirect("/account/changedata")
                        else:
                            password = None
                        if request.form['massage']:
                            aboutme = request.form['massage']
                        else:
                            aboutme = None
                        if request.files["loadavatar"]:
                            print("cool")
                            avatar = request.files["loadavatar"].read()
                        else:
                            print("not cool")
                            avatar = None
                        print("suuuuuuuppppppppeeeeeerrrr")
                        res = dbase.updatedata(aboutme,request.form['newusername'], request.form['newemail'],password, avatar, current_user.get_id())
                        if res:
                            flash("Дані було змінено успішно", category='success')
                        else:
                            flash("Виникла помилка під зміни даних", category='error')
                        return redirect("/account")
                    else:
                        flash("Така пошта уже існує", category='error')
                else:
                    flash("Таке ім'я уже існує", category='error')
            else:
                flash("Некоректне ім'я", category='error')
        else:
                flash("Пароль не підходить", category='error')
    return render_template("changedata.html", username = current_user.get_username(), email = current_user.get_email())



if __name__ == "__main__":
    create_db()
    app.run(debug=False)