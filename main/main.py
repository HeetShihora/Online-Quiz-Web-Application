from xlrd import open_workbook
import uuid
from flask import *
from fileinput import filename
import pandas
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
import csv
import openpyxl
from werkzeug.utils import secure_filename
app = Flask(__name__)


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'quiz'
mysql = MySQL(app)


@app.route('/')
def main():
    return render_template("index.html")


@app.route("/make")
def make():
    return render_template("make.html")


@app.route('/upload', methods=['POST'])
def upload():
    rows = []
    fields = []
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)

        id = uuid.uuid4()
        ct = 1
        li = []
        try:
            with open(f.filename, mode='r')as file:

                # reading the CSV file
                csvFile = csv.reader(file)

                # displaying the contents of the CSV file
                for lines in csvFile:
                    li.append(lines)
        except:
            return render_template('error.html', msg='Can not open file')

        data = []
        for i in range(1, len(li)):
            x = li[i]
            data.append(x)

        try:
            for x in data:
                cursor = mysql.connection.cursor()
                cursor.execute(''' INSERT INTO questions VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''',
                               (id, x[0], x[1], x[2], x[3], x[4], x[5], x[6]))
                ct += 1
                mysql.connection.commit()
                cursor.close()
        except:
            return render_template('error.html', msg='Could not load data from mysql server')
    return render_template('acknowledgement.html', id=id)


@app.route('/give')
def give():
    return render_template('give.html')


@app.route('/start', methods=['POST'])
def start():
    if request.method == 'POST':
        x = request.form.get("quiz_id")
        qid = str(x)
        qid = qid.strip()
        try:
            cursor = mysql.connection.cursor()

            s = """select question_id,question,opt1,opt2,opt3,opt4 from questions where quiz_id=%s"""

            cursor.execute(s, (qid,))
            questions = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
        except:
            return render_template('error.html', msg='Could not load data from mysql server')
        if len(questions) == 0:
            return render_template('error.html', msg='No questions found for this quiz id')

        return render_template('start.html', questions=questions)


@app.route('/submit', methods=['POST'])
def submit():
    print(request.form)
    x = request.form.get('quiz_id')
    ct = 0
    qid = str(x)
    qid = qid.strip()
    try:
        cursor = mysql.connection.cursor()

        s = """select answer from questions where quiz_id=%s"""

        cursor.execute(s, (qid,))
        answers = cursor.fetchall()
        mysql.connection.commit()
    # print(answers)
        cursor.close()
    except:
        return render_template('error.html', msg='Could not load data from mysql server')

    if len(answers) == 0:
        return render_template('error.html', msg='Please check your quiz id.')
    no_que = len(answers)
    response = []
    correct_ans = []
    try:
        cursor = mysql.connection.cursor()

        s = """select question_id,question,opt1,opt2,opt3,opt4 from questions where quiz_id=%s"""

        cursor.execute(s, (qid,))
        questions = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
    except:
        return render_template('error.html', msg='Could not load data from mysql server')
    if len(questions) == 0:
        return render_template('error.html', msg='Please check your quiz id.')
    for i in range(no_que):
        res = request.form.get((str(i+1)))
        res = res.strip()
        ans = str(answers[i])
        le = len(ans)
        temp = ans[2:le-3:]
        response.append(res)
        correct_ans.append(temp)

        if res == temp:
            ct += 1
    print(ct)

    que = []
    for q in questions:

        a = q[0]
        b = q[1].strip()
        c = q[2].strip()
        d = q[3].strip()
        e = q[4].strip()
        f = q[5].strip()

        li = [a, b, c, d, e, f]

        que.append(li)
    print('\n\n')
    print(que)
    print('\n\n')
    print(response)
    print('\n\n')
    print(correct_ans)
    print('\n\n')
    info = zip(que, response, correct_ans)
    return render_template('answers.html', info=info, marks=ct, total=len(que))


app.run(host='127.0.0.1', port=3000, debug=True)
