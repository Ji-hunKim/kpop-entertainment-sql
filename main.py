from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

connect = psycopg2.connect("dbname=dbentertainment user=postgres password=0513")
cur = connect.cursor()

#homepage
@app.route('/')
def one():
    return render_template("loginpage.html")

#when login failed
@app.route('/loginfail')
def loginfailed():
    return render_template("login_fail.html")

#in loginfail page, you can go back home just by clicking 'gohome' botton
@app.route('/fail', methods=['POST'])
def gohome():
    return redirect(url_for('one'))

#login check
@app.route('/register', methods=['POST'])
def logincheck():
    idd = request.form["id"]
    pwd = request.form["password"]

    cur.execute ("SELECT id FROM idpw WHERE id = '%s'" % idd)
    result1 = cur.fetchall()
    cur.execute("SELECT pw FROM idpw WHERE pw = '%s'" % pwd)
    result2 = cur.fetchall()

    if not result1 or not result2:
        return redirect(url_for('loginfailed'))
    else:
        return redirect(url_for('homepage'))

@app.route('/homepage')
def homepage():
    return render_template("home.html")

@app.route('/first', methods=['POST'])
def data_cartesian():
    a = request.form["g_idd"]
    cur.execute ("SELECT g_name, debut_year, s_name, age, salary FROM groups,singers "
                 "WHERE groups.g_id = '%s' and groups.g_id = singers.g_id " % a)
    result = cur.fetchall()
    return render_template("first.html", users = result)

@app.route('/second', methods=['POST'])
def move_to_second():
    return render_template("second.html")

@app.route('/secondtwo', methods=['POST'])
def data_insert():
    a = request.form["song_id"]
    b = request.form["song_name"]
    c = int(request.form["song_year"])
    d = request.form["g_id"]
    e = request.form["p_id"]


    cur.execute ("INSERT INTO songs VALUES ('%s','%s',%d,'%s','%s')" % (a,b,c,d,e))
    connect.commit()

    cur.execute ("SELECT * FROM songs")
    result = cur.fetchall()
    return render_template("secondtwo.html", users = result)

@app.route('/secondthree', methods=['POST'])
def data_delete():
    a = request.form["song_id2"]

    cur.execute("DELETE FROM songs WHERE song_id = '%s'" % a)
    connect.commit()

    cur.execute ("SELECT * FROM songs")
    result = cur.fetchall()
    return render_template("secondtwo.html", users = result)

@app.route('/third', methods=['POST'])
def avg_salary():
    a = request.form["g_iddd"]
    cur.execute ("SELECT g_id, avg(salary) FROM managers WHERE salary > "
                 "all (select salary from managers where g_id = '%s') group by g_id " %a)
    result = cur.fetchall()
    return render_template("third.html", users = result)

@app.route('/fourth', methods=['POST'])
def move_to_fourth():
    return render_template("fourth.html")

@app.route('/fourthtwo', methods=['POST'])
def update():
    a = request.form["s_id"]
    b = int(request.form["sal"])

    cur.execute("UPDATE singers SET salary = %d WHERE s_id = '%s'" % (b, a))
    connect.commit()

    cur.execute("SELECT * FROM singers")
    result = cur.fetchall()
    return render_template("fourthtwo.html", users=result)

@app.route('/fifth', methods=['GET'])
def naturaljoin():
    cur.execute ("SELECT song_name, p_name FROM songs natural join producers")
    result = cur.fetchall()
    return render_template("fifth.html", users = result)


if __name__ == '__main__':
    app.run()
