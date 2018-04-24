from flask import Flask, session, request
from flask_restful import Api, Resource
from flaskext.mysql import MySQL

app = Flask(__name__)
api = Api(app)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'new_login'
app.config['MYSQL_DATABASE_HOST'] = ''
mysql.init_app(app)


class LoginUser(Resource):
    def post(self):
        """"From this function, User is log into the device, If user is not registered, first he had to sign up"""

        conn = mysql.get_db()
        cursor = conn.cursor()
        error = None

        if 'UserName' in session:
            return print("User is already login to the device")

        if request.method == 'POST':
            username_form = request.form['UserName']
            password_secret = request.form['Pwd']

            cursor.execute("SELECT Count(1) FROM login WHERE UserName = %s;", [username_form])
            if cursor.fetchone()[0]:

                cursor.execute("SELECT Pwd FROM login WHERE UserName = %s;", [username_form])
                for row in cursor.fetchall():

                    # if md5(password_secret).hexdigest() == row[0]:
                    if password_secret == row[0]:

                        # session['UserName'] = request.form['UserName']

                        return "user is present in the db"
                    else:
                        error = "Invalid Credential"
            else:
                error = "Invalid Credential"
        return "User is not present in the db"


class AddUser(Resource):
    def post(self):
        """"Sign up function"""
        conn = mysql.get_db()
        # conn = mysql.connect()
        cursor = conn.cursor()

        username_form = request.form['UserName']
        pwd_form = request.form['Pwd']
        cursor.execute("Select Count(1) FROM login WHERE UserName = %s", [username_form])
        if cursor.fetchone()[0]:
            return "user is already present in the db"
        else:
            cursor.execute("INSERT INTO login (UserName, Pwd) VALUES ('%s','%s')" % (username_form, pwd_form))
            conn.commit()

            return "user is successfully added into the db"
        conn.close()


class UpdateUser(Resource):
    def put(self):
        """"If you want the password or username , you can update user information from this function"""
        conn = mysql.get_db()
        # conn = mysql.connect()
        cursor = conn.cursor()
        # user_id = os.geteuid()
        username_form = request.form['UserName']
        pwd_form = request.form['Pwd']
        cursor.execute("SELECT Count(1) FROM login WHERE UserName = %s;", [username_form])
        if cursor.fetchone()[0]:
            cursor.execute("Select Id from login WHERE UserName = %s", (username_form))
            uid = cursor.fetchone()
            cursor.execute("UPDATE login SET Pwd = '%s' WHERE ID = '%s'" % (pwd_form, uid[0]))

            conn.commit()
            return "user is successfully updated in the db"

        else:
            return "user is not found in the db"


class DeleteUser(Resource):
    def delete(self):
        """If you want to delete some user, simple enter their name and the user will be deleted"""
        conn = mysql.get_db()
        # conn = mysql.connect()
        cursor = conn.cursor()

        username_form = request.form['UserName']
        cursor.execute("SELECT Count(1) FROM login WHERE UserName = %s;", [username_form])

        if cursor.fetchone()[0]:
            cursor.execute("Select Id from login WHERE UserName = %s", [username_form])
            uid = cursor.fetchone()
            cursor.execute("DELETE from login WHERE Id = %s", (uid[0]))
            conn.commit()
            return "User is successfully removed from db"
            # cursor.execute("DELETE from login WHERE UserName = 'aslam'")
        else:
            return "User does not exist"


api.add_resource(UpdateUser, '/updateuser')
# api.add_resource(LoginUser, '/login')
# api.add_resource(DeleteUser, '/deluser')
# api.add_resource(AddUser, '/adduser')


if __name__ == '__main__':
    app.run(debug=True, port=8000)





