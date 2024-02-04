from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)

# the home page of the website
@app.route('/')
def home():
    title = 'home'
    return render_template('home.html', title=title)

# this page is used to save the coordinates sent from the home page
@app.route('/savedata',  methods=['GET', 'POST'])
def savedata():
    data = request.form
    x = data["X"]
    y = data["Y"]
    tbl = data["tbl"]
    newClick(x, y, tbl)
    return data

# runs the sql commands that are passed in
def runsql(*args):
    conn = sqlite3.connect("clicks.db")
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()
    if len(args) == 1:
        cursor.execute(args[0])
    else:
        cursor.execute(args[0], args[1])
    conn.commit()
    return cursor.fetchall()

# saves a new click to the database
def newClick(x, y, tbl):
    sqlstring = "SELECT * FROM " + tbl + " WHERE xCoord = ? AND yCoord = ?"
    values = (x, y)
    data = runsql(sqlstring, values)
    if data == []:
        exists = False
    else:
        exists = True

    if not exists:
        sqlstring = "INSERT INTO " + tbl + "(xCoord, yCoord, count) VALUES (?, ?, 1)"
        values = (x, y)
        runsql(sqlstring, values)

    else:
        sqlstring = "SELECT Count FROM " + tbl + " WHERE xCoord = ? AND yCoord = ?"
        values = (x, y)
        data = runsql(sqlstring, values)
        count = data[0][0]
        count += 1

        sqlstring = "UPDATE " + tbl + " SET count = ? WHERE xCoord = ? AND yCoord = ?"
        values = (count, x, y)
        runsql(sqlstring, values)

if __name__ == '__main__':
    app.run(debug=True)
