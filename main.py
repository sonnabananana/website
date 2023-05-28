from flask import Flask, render_template, request, redirect, session, flash
import pymysql
import datetime
import os
import uuid

app = Flask(__name__)
app.secret_key = '!SeCrEt__KeY.mERLIN13542!'

def create_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="MER!13062006Iby.nz!LIN",
        db="users",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def main_page():
    if 'logged_in' in session:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE id = %s" 
                values = ( 
                    session['id']
                )
                cursor.execute(sql, values)
                result = cursor.fetchone()
        return render_template('home_page.html', result=result)
    else:
        return render_template('home_page.html')

#YRUE


@app.route('/signup', methods = ['POST', 'GET'] )
def signup():
    if request.method == 'POST':
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = """INSERT INTO users
                    (fname, lname, email, password, birthday, acc_creation)
                    VALUES (%s, %s, %s, %s, %s, %s) """
                values = (
                    request.form["fname"],
                    request.form["lname"],
                    request.form["email"],
                    request.form["password"],
                    request.form["birthday"],
                    datetime.date.today()
                )
                cursor.execute(sql, values)
                connection.commit()

                return redirect('/')
            
    else:
        return render_template('signup.html')

@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        with create_connection() as connection:
            with connection.cursor() as cursor:

                sql = """ SELECT * FROM users WHERE 
                email = %s AND password = %s """
                values = (
                    request.form["email"],
                    request.form["password"]
                )
                cursor.execute(sql, values)
                result = cursor.fetchone()
        if result:
            session['logged_in'] = True
            session['id'] = result['id']
            session['password'] = result['password']
            session['email'] = result['email']
            session['fname'] = result['fname']
            session['lname'] = result['lname']
            session['birthday'] = result['birthday']
            session['role'] = result['role']
            
            return redirect('/')
        else:
            flash('Incorrect login information!')
            return redirect('/login')
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/settings')
def settings():
    return render_template('/settings.html')

@app.route('/account_details')
def account_details():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE id = %s"
            values = (
                request.args['id']
                )
            cursor.execute(sql, values)
            result = cursor.fetchone()
    return render_template('/account_details.html', result=result)

@app.route('/edit_profile', methods = ["POST", "GET"])
def edit_profile():
    if request.method == "POST":
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = """UPDATE users SET
                fname = %s,
                lname = %s,
                password = %s,
                email = %s,
                birthday = %s,
                acc_creation = %s
                WHERE id = %s
                """
                values = (
                    request.form['fname'],
                    request.form['lname'],
                    request.form['password'],
                    request.form['email'],
                    request.form['birthday'],
                    request.form['acc_creation'],
                    session['id']
                )
                cursor.execute(sql, values)
                connection.commit()
        return redirect('/')

    else:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE id = %s"
                values = (request.args['id'])
                cursor.execute(sql, values)
                result = cursor.fetchone()
        return render_template('/edit_profile.html', result=result)

@app.route('/user_posts')
def user_posts():
    return render_template('/user_posts.html')

if __name__ == "__main__":
    app.run(debug=True)