"""
login app for review
"""
from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify
import MySQLdb
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

db = MySQLdb.connect(host="localhost", user="root", passwd="", db="new_login")
cur = db.cursor()


def logout():
    session.pop('UserName', None)
    return print("User is now logout from the device")

@app.route('/')
def index():
    if 'UserName' in session:
        username_session = escape(session['UserName']).capitalize()
        return render_template('index.html', session_user_name=username_session)
    return redirect(url_for('login'))


# @app.route('/login', methods=['GET', 'POST'])


class LoginUser(Resource):

    def post(self):
        error = None

        if 'UserName' in session:
            return print("User is already login to the device")

        if request.method == 'POST':
            username_form = request.form['UserName']
            password_secret = request.form['Pwd']

            cur.execute("SELECT Count(1) FROM login WHERE UserName = %s;", [username_form])
            if cur.fetchone()[0]:

                cur.execute("SELECT Pwd FROM login WHERE UserName = %s;", [username_form])
                for row in cur.fetchall():

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
    def post(self, name):

        UserName_form = request.form['UserName']
        Pwd_form = request.form['Pwd']

        new_user = AddUser(UserName_form, Pwd_form)

        db.session.add(new_user)
        db.session.commit()
        print("User is successfully added in the db")

        return jsonify(new_user)



@app.route('/logout')
def logout():
    session.pop('UserName', None)
    return "User is getting logout from the device"


api.add_resource(LoginUser, '/login')

# api.add_resource(logout, '/logout')
# api.add_resource(AddUser, '/addUser')


if __name__ == '__main__':
    app.run(debug=True, port=5000)




