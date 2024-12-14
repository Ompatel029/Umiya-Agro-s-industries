import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'P@tel2004',
    'database': 'om'
}


def get_connection():
    return mysql.connector.connect(**db_config)


def create_USER_table():
    con = get_connection()
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS USER1(
    email VARCHAR(255) NOT NULL primary key,
    password VARCHAR(255) NOT NULL)
    """)
    con.commit()
    cur.close()
    con.close()


create_USER_table()


def create_user2_table():
    con = get_connection()
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS USER2(
    pincode VARCHAR(60) NOT NULL primary key,
    grain VARCHAR(255) NOT NULL)
    """)
    con.commit()
    cur.close()
    con.close()


create_user2_table()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'signup' in request.form:  # Handling signup form for USER1
            email = request.form['email']
            password = request.form['password']
            try:
                # Insert data into USER1 table
                con = get_connection()
                cur = con.cursor()
                cur.execute("INSERT INTO USER1 (email, password) VALUES (%s, %s)", (email, password))
                con.commit()
                cur.close()
                con.close()
                session['email'] = email
                return redirect(url_for('res'))
            except Exception as e:
                print("Error inserting values:", e)
                return 'Error inserting values'
        elif 'login' in request.form:  # Handling login form for USER1
            email = request.form['email']
            password = request.form['password']
            try:
                # Check credentials in USER1 table
                con = get_connection()
                cur = con.cursor()
                cur.execute("SELECT * FROM USER1 WHERE email=%s AND password=%s", (email, password))
                user = cur.fetchone()
                if user:
                    session['email'] = email
                    return redirect(url_for('res'))
                else:
                    return render_template('index.html', message='Invalid username or password')
            except Exception as e:
                print("Error:", e)
                return 'Error'
        elif 'buy_order' in request.form:  # Handling buy order form for USER2
            pincode = request.form['pincode']
            grain = request.form['grain']
            try:
                # Insert data into USER2 table
                con = get_connection()
                cur = con.cursor()
                cur.execute("INSERT INTO USER2 (pincode, grain) VALUES (%s, %s)", (pincode, grain))
                con.commit()
                cur.close()
                con.close()
                session['pincode'] = pincode
                return redirect(url_for('res'))
            except Exception as e:
                print("Error inserting values:", e)
                return 'Error inserting values'
        elif 'login2' in request.form:  # Handling login form for USER2 (if needed)
            # Similar to handling login for USER1, implement as needed
            pass

    return render_template('index.html')


@app.route('/main')
def res():
    if 'email' in session:
        return render_template('main.html')
    else:
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)