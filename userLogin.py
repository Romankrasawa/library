class UserLogin():


    def fromDB(self,user_id,db):
        self .__user = db.getUser(user_id)
        return self


    def create(self,user):
        self .__user = user
        return self


    def is_authenticated(self):
        return True


    def is_active(self):
        return True


    def is_anonymous(self):
        return False


    def get_id(self):
        print("lool",str(self .__user['user_id']))
        return self .__user['user_id']
    def get_username(self):
        print("lool",str(self .__user['username']))
        return self .__user['username']
    def get_email(self):
        print("lool",str(self .__user['email']))
        return self .__user['email']
    def get_password(self):
        print("lool",str(self .__user['password']))
        return self .__user['password']
    def get_avatar(self):
        avatar = self .__user['avatar']
        print("youhoooooooooo")
        return avatar
    def get_aboutme(self):
        print("lool",str(self .__user['aboutme']))
        return self .__user['aboutme']
    def get_folowed(self):
        print("lool",str(self .__user['folowed']))
        return str(self .__user['folowed'])