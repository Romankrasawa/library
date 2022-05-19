import sqlite3


class FDataBase:


    def __init__(self, dbase):
        self._db = dbase
        self._cur = dbase.cursor()



    def home_books(self):
        sql= 'SELECT * FROM book LIMIT 15'
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
        if not image:
            try:
                self._cur.execute('INSERT INTO book (book_id, name, pages, author, year, company) VALUES (?,?,?,?,?,?);',(book_id, name, pages, author, years, company))
            except:
                print("llloooooollll")
                return False
        else:
            try:
                binary = sqlite3.Binary(image)
                self._cur.execute('INSERT INTO book (book_id, name, pages, author, year, company, book_photo) VALUES (?,?,?,?,?,?,?);', (book_id, name, pages, author, years, company, binary))
            except:
                return False
        self._db.commit()
        print("book was added")
        return True


    def search(self, searchbar):

        sql = f"SELECT * FROM book WHERE name LIKE \'%{searchbar}%\';"
        try:
            self._cur.execute(sql)
            result = self._cur.fetchall()
            print(result)
            print("search completed")
            return result
        except:
            print("error БД")
        return []


    def search_id(self, searchid):
        sql = f"SELECT * FROM book WHERE book_id = \"{searchid}\";"
        try:
            print(sql)
            self._cur.execute(sql)
            result = self._cur.fetchall()
            print("search completed")
            return result
        except:
            print("error БД")
        return []


    def registrate(self, username, email, password):
        sql = f'INSERT INTO user (username, email, password) VALUES (\"{username}\",\"{email}\",\"{password}\");'
        try:
            print(sql)
            self._cur.execute(sql)
            self._db.commit()
            print("logged")
            return True
        except:
             print("error БД")
             return False


    def checkmassages(self, searchid):
        sql = f"SELECT * FROM massages WHERE book_id = {searchid};"
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


    def add_massage(self, text, time, book_id):
        sql = f'INSERT INTO massages (text, time, book_id) VALUES (\"{text}\",\"{time}\",\"{book_id}\");'
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