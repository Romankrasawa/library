import sqlite3


class FDataBase:


    def __init__(self, dbase):
        self._db = dbase
        self._cur = dbase.cursor()



    def home_books(self):
        sql= 'SELECT * FROM book ORDER BY view DESC LIMIT 15'
        try:
             self._cur.execute(sql)
             res=self._cur.fetchall()
             if res:
                 print(res)
                 return res
        except:
             print("error БД")
        return []



    def add_book(self, name, author, years, pages, company, image):
        book_id = 0
        self._cur.execute("SELECT MAX(book_id) FROM book")
        for i in self._cur.fetchone():
            if i == None:
                book_id =str(1).zfill(6)
            else:
                book_id = str(int(i.lstrip("0"))+1).zfill(6)
        try:
            binary = sqlite3.Binary(image)
            self._cur.execute('INSERT INTO book (book_id, name, pages, author, year, company, book_photo) VALUES (?,?,?,?,?,?,?);', (book_id, name, pages, author, years, company, binary))
        except:
            return False
        self._db.commit()
        print("book was added")
        return True


    def search_id(self, searchbar):
        sql = f"SELECT * FROM book WHERE book_id = \'{searchbar}\';"
        try:
            self._cur.execute(sql)
            result = self._cur.fetchall()
            print(len(result))
            print("search completed")
            return result
        except:
            print("error БД")
        return []


    def search(self, searchid,sort, page):
        sql = f"SELECT * FROM book WHERE name LIKE \"%{searchid}%\";"
        try:
            print(sql)
            self._cur.execute(sql)
            paging = self._cur.fetchall()
            print("search completed")
        except:
            print("error БД")
        sort = sort.replace('-', ' ')
        print(sort)
        sql = f"SELECT * FROM book WHERE name LIKE \"%{searchid}%\" ORDER BY {sort} LIMIT 3 OFFSET {(int(page)-1)*3};"
        try:
            print(sql)
            self._cur.execute(sql)
            result = self._cur.fetchall()
            print("search completed")
            return [result, len(paging)]
        except:
            print("error БД")
        return []


    def registrate(self, username, email, password, avatar):
        try:
            self._cur.execute('INSERT INTO user (username, email, password, avatar) VALUES (?,?,?,?);', (username, email, password, avatar))
            self._db.commit()
            print("logged")
            return True
        except:
             print("error БД")
             return False

    def getUser(self, user_id):
        try:
            self._cur.execute(f"SELECT*FROM user WHERE user_id={user_id} LIMIT 1")
            res = self._cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД" + str(e))
        return False

    def getUserByEmail(self, email):
        try:
            self._cur.execute(f"SELECT*FROM user WHERE email='{email}' LIMIT 1")
            res = self._cur.fetchone()
            print(res)
            if not res:
                print("Пользователь не найден")
                return False
            for i in res:
                print(i)

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД" + str(e))
        return False

    def addview(self, id):
        book_view = 0
        print(id)
        sql = f"SELECT view FROM book WHERE book_id = \"{id}\""
        print(sql)
        self._cur.execute(sql)
        for i in self._cur.fetchone():
            book_view = i+1
        print(book_view)
        try:
            self._cur.execute("UPDATE book SET view = ? WHERE book_id = ?", (book_view,id))
            self._db.commit()
            print("view updated")
            return True
        except sqlite3.Error as e:
            print("errorrr БД:" + str(e))
            return False


    def checkmassages(self, searchid):
        sql = f"SELECT * FROM massages WHERE book_id = \"{searchid}\";"
        try:
            print(sql)
            self._cur.execute(sql)
            result = self._cur.fetchall()
            print(self._cur.description)
            print("search completed")
            return result
        except:
            print("error БД")
        return []


    def add_massage(self, text, time, book_id, user_id):
        print(user_id)
        sql = f'INSERT INTO massages (text, time, book_id, user_id) VALUES (\"{text}\",\"{time}\",\"{book_id}\",\"{user_id}\");'
        try:
            print(sql)
            self._cur.execute(sql)
            self._db.commit()
            print("logged")
            return True
        except:
             print("error БД")
             return False


    def getpicture(self, id):
        sql= f'SELECT book_photo FROM book WHERE book_id = \"{id}\"'
        try:
             self._cur.execute(sql)
             res = self._cur.fetchone()
             if res:
                 for i in res:
                    return i
        except sqlite3.Error as e:
             print("error БД:" + str(e))
        return []
