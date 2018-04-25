"""Login, Sign Up, Update and Delete User"""
from flask import Flask, session, request
from flaskext.mysql import MySQL
from flask_restful import Api, Resource

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
                cursor.execute("SELECT Count(*) FROM login WHERE UserName = %s;", [username_form])
            if cursor.fetchone()[0]:
                cursor.execute("SELECT Pwd FROM login WHERE UserName = %s;", [username_form])
                for row in cursor.fetchall():
                    if password_secret == row[0]:
                        return "UserName = %s is present in the db", username_form
                    else:
                        error = "Invalid Credential"
            else:
                error = "Invalid Credential"
                conn.close()
        return "User is not present in the db"


class AddUser(Resource):
    def post(self):
        """"Sign up function"""
        conn = mysql.get_db()
        cursor = conn.cursor()
        username_form = request.form['UserName']
        pwd_form = request.form['Pwd']
        cursor.execute("Select Count(*) FROM login WHERE UserName = %s", [username_form])
        if cursor.fetchone()[0]:
            return "user is already present in the db"
        else:
            cursor.execute("INSERT INTO login (UserName, Pwd) VALUES ('%s','%s')" % (username_form, pwd_form))
            conn.commit()
            return "UserName = %s is successfully added into the db", username_form
        conn.close()


class UpdateUser(Resource):
    def put(self):
        """"Update user information"""
        conn = mysql.get_db()
        cursor = conn.cursor()
        username_form = request.form['UserName']
        pwd_form = request.form['Pwd']
        cursor.execute("SELECT Count(*) FROM login WHERE UserName = %s;", [username_form])
        if cursor.fetchone()[0]:
            cursor.execute("Select Id from login WHERE UserName = %s", username_form)
            uid = cursor.fetchone()
            cursor.execute("UPDATE login SET Pwd = '%s' WHERE ID = '%s'" % (pwd_form, uid[0]))
            conn.commit()
            return "UserName = %s is successfully updated in the db", username_form

        else:
            conn.close()
            return "user is not found in the db"


class DeleteUser(Resource):
    """Delete User"""
    def delete(self):
        """If you want to delete some user, simple enter their name and the user will be deleted"""
        conn = mysql.get_db()
        cursor = conn.cursor()
        username_form = request.form['UserName']
        cursor.execute("SELECT Count(*) FROM login WHERE UserName = %s;", [username_form])
        if cursor.fetchone()[0]:
            cursor.execute("Select Id from login WHERE UserName = %s", [username_form])
            uid = cursor.fetchone()
            cursor.execute("DELETE from login WHERE Id = %s", (uid[0]))
            conn.commit()
            return "UserName = %s is successfully removed from db", username_form

        else:
            conn.close()
            return "User does not exist"


api.add_resource(UpdateUser, '/updateuser')
api.add_resource(LoginUser, '/login')
api.add_resource(DeleteUser, '/deluser')
api.add_resource(AddUser, '/adduser')

if __name__ == '__main__':
    app.run(debug=True, port=8000)





