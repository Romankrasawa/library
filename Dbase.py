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

    def add_book(self, name, author, years, pages, company, image, user_id):
        book_id = 0
        self._cur.execute("SELECT MAX(book_id) FROM book")
        for i in self._cur.fetchone():
            if i == None:
                book_id =str(1).zfill(6)
            else:
                book_id = str(int(i.lstrip("0"))+1).zfill(6)
        try:
            binary = sqlite3.Binary(image)
            print(binary)
            self._cur.execute('INSERT INTO book (book_id, name, pages, author, year, company, book_photo, user_id, search_name) VALUES (?,?,?,?,?,?,?,?,?);', (book_id, name, pages, author, years, company, binary,user_id, name.lower()))
        except sqlite3.Error as e:
            print("error БД" + str(e))
            return False
        self._db.commit()
        print("book was added")
        return True, book_id

    def change_book(self, name, author, years, pages, company,book_id, image=None):
        try:
            if image == None:
                self._cur.execute('UPDATE book SET name=?,search_name=?, pages=?, author=?, year=?, company=?  WHERE book_id = ?;', (name, name.lower(), pages, author, years, company, book_id))
            else:
                binary = sqlite3.Binary(image)
                print(image)
                self._cur.execute('UPDATE book SET name=?,search_name=?, pages=?, author=?, year=?, company=?, book_photo=?  WHERE book_id = ?;', (name, name.lower(), pages, author, years, company, image, book_id))
        except sqlite3.Error as e:
            print("error БД" + str(e))
            return False
        self._db.commit()
        print("book changed")
        return True

    def delete_book(self,book_id):
        try:
            print(book_id)
            self._cur.execute(f"DELETE FROM book WHERE book_id = \"{book_id}\";")
            self._cur.execute(f"DELETE FROM massages WHERE book_id = \"{book_id}\";")
        except sqlite3.Error as e:
            print("error БД" + str(e))
            return False
        self._db.commit()
        print("book deleted")
        return True

    def search_id(self, searchbar):
        sql = f"SELECT * FROM book WHERE book_id = \'{searchbar}\' LIMIT 1;"
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
        searchid = "".join([i + "%" for i in searchid.lower()])
        sql = f"SELECT book_id FROM book WHERE search_name LIKE \"%{searchid}\";"
        try:
            print(sql)
            self._cur.execute(sql)
            paging = self._cur.fetchall()
            for  i in  paging:
                for x in i:
                    print(x)
            print("search completed")
        except:
            print("error БД")
        sort = sort.replace('-', ' ')
        print(sort)
        sql = f"SELECT * FROM book WHERE search_name LIKE \"%{searchid}\" ORDER BY {sort} LIMIT 9 OFFSET {(int(page)-1)* 9 };"
        try:
            print(sql)
            self._cur.execute(sql)
            result = self._cur.fetchall()
            print("search completed")
            return [result, len(paging)]
        except:
            print("error БД")
        return []

    def created(self, user_id, sort, page):
        sql = f"SELECT book_id FROM book WHERE user_id = {user_id};"
        try:
            print(sql)
            self._cur.execute(sql)
            paging = self._cur.fetchall()
            for i in paging:
                for x in i:
                    print(x)
            print("search completed")
        except:
            print("error БД")
        sort = sort.replace('-', ' ')
        print(sort)
        sql = f"SELECT * FROM book WHERE user_id = {user_id} ORDER BY {sort} LIMIT 9 OFFSET {(int(page) - 1) * 9};"
        try:
            print(sql)
            self._cur.execute(sql)
            result = self._cur.fetchall()
            print("search completed")
            return [result, len(paging)]
        except sqlite3.Error as e:
            print("error БД" + str(e))
        return []

    def deletefolow(self, user_id, folowed, book_id):
        print(user_id)
        book_id = book_id
        folowed = folowed.translate("".maketrans("","",book_id))
        print(folowed)
        sql = f"UPDATE user SET folowed = \"{folowed}\" WHERE user_id = {user_id}"
        print(sql)
        try:
            self._cur.execute(sql)
            self._db.commit()
            paging = self._cur.fetchall()
            for i in paging:
                for x in i:
                    print(x)
            print("folowed added")
        except sqlite3.Error as e:
            print("error БД" + str(e))

    def addfolow(self, user_id, folowed, book_id):
        print(user_id)
        folowed = folowed + book_id + " "
        print(folowed)
        sql = f"UPDATE user SET folowed = \"{folowed}\" WHERE user_id = {user_id}"
        print(sql)
        try:
            self._cur.execute(sql)
            self._db.commit()
            paging = self._cur.fetchall()
            for i in paging:
                for x in i:
                    print(x)
            print("folowed added")
        except sqlite3.Error as e:
            print("error БД" + str(e))

    def folowed(self, user_id, sort, page):
        print(user_id)
        folowed = tuple(user_id.split(" "))
        print(folowed)
        sql = f"SELECT book_id FROM book WHERE book_id in {folowed};"
        try:
            print(sql)
            self._cur.execute(sql)
            paging = self._cur.fetchall()
            for i in paging:
                for x in i:
                    print(x)
            print("search completed")
        except:
            print("error БД")
        sort = sort.replace('-', ' ')
        print(sort)
        sql = f"SELECT * FROM book WHERE book_id in {folowed} ORDER BY {sort} LIMIT 9 OFFSET {(int(page) - 1) * 9};"
        try:
            print(sql)
            self._cur.execute( sql)
            result = self._cur.fetchall()
            print("search completed")
            return [result, len(paging)]
        except sqlite3.Error as e:
            print("error БД" + str(e))
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
                print("dosnt founded")
                return False
            return res
        except sqlite3.Error as e:
            print("error БД" + str(e))
        return False

    def getUserInfo(self, user_id):
        try:
            self._cur.execute(f"SELECT username, aboutme FROM user WHERE user_id={user_id} LIMIT 1")
            res = self._cur.fetchall()
            if not res:
                print("dosnt founded")
                return False
            return res
        except sqlite3.Error as e:
            print("error БД" + str(e))
        return False

    def getUserByEmail(self, email):
        try:
            self._cur.execute(f"SELECT*FROM user WHERE email='{email}' LIMIT 1")
            res = self._cur.fetchone()
            print(res)
            if not res:
                print("dosnt founded")
                return False
            for i in res:
                print(i)

            return res
        except sqlite3.Error as e:
            print("error БД" + str(e))
        return False

    def getUserByUsername(self, username):
        try:
            self._cur.execute(f"SELECT*FROM user WHERE username ='{username}' LIMIT 1")
            res = self._cur.fetchone()
            print(res)
            if not res:
                print("dosnt founded")
                return False
            for i in res:
                print(i)

            return res
        except sqlite3.Error as e:
            print("error БД" + str(e))
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
    def updatedata(self,aboutme,username,email,password,image, user_id):
        try:
            if aboutme:
                aboutme = f"aboutme = \'{aboutme}\',"
            else:
                aboutme = ""
            if password:
                password = f"password = \'{password}\',"
            else:
                password = ""
            print(username,email,password)
            if image:
                binary = sqlite3.Binary(image)
                print(binary)
                self._cur.execute(f"UPDATE user SET {aboutme} {password} avatar = ?,username=?,email=? WHERE user_id = ?", (image,username,email, user_id))
            else:
                self._cur.execute(f"UPDATE user SET {aboutme} {password} username=?,email=? WHERE user_id = ?", (username,email, user_id))
            self._db.commit()
            print("data updated")
            return True
        except sqlite3.Error as e:
            print("errorrr updateБД:" + str(e))
            return False


    def checkmassages(self, book_id, page):
        sql = f"SELECT * FROM massages WHERE book_id = \"{book_id}\";"
        try:
            print(sql)
            self._cur.execute(sql)
            paging = self._cur.fetchall()
            print("search completed")
        except:
            print("error БД")
        sql = f"SELECT * FROM massages WHERE book_id = \"{book_id}\" ORDER BY massage_id DESC LIMIT 15 OFFSET {(int(page) - 1) * 15};"
        try:
            print(sql)
            self._cur.execute(sql)
            result = self._cur.fetchall()
            print("search completed")
            return [result, len(paging)]
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

    def getavatar(self, id):
        sql= f'SELECT avatar FROM user WHERE user_id = {id}'
        try:
             self._cur.execute(sql)
             res = self._cur.fetchone()
             if res:
                 for i in res:
                    return i
        except sqlite3.Error as e:
             print("error БД:" + str(e))
        return []

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
