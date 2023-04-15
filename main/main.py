import uuid
from flask import *
from fileinput import filename
import pandas
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
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
        dataframe = openpyxl.load_workbook(f.filename)
        dataframe1 = dataframe.active
        id = uuid.uuid4()
        ct = 1
        li = []
        for row in range(1, dataframe1.max_row):

            for col in dataframe1.iter_cols(1, dataframe1.max_column):
                li.append(col[row].value)

            cursor = mysql.connection.cursor()
            cursor.execute(''' INSERT INTO questions VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''',
                           (id, li[0], li[1], li[2], li[3], li[4], li[5], li[6]))
            ct += 1
            mysql.connection.commit()
            cursor.close()
        return render_template('acknowledgement.html', id=id)


@app.route('/give')
def give():
    return render_template('give.html')


@app.route('/start', methods=['POST'])
def start():
    if request.method == 'POST':
        qid = request.form.get("quiz_id")
        print(qid)
        cursor = mysql.connection.cursor()

        s = """select question_id,question,opt1,opt2,opt3,opt4 from questions where quiz_id=%s"""

        cursor.execute(s, (qid,))
        questions = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()

        return render_template('start.html', questions=questions)


@app.route('/submit', methods=['POST'])
def submit():
    print(request.form)
    qid = request.form.get('quiz_id')
    ct = 0
    cursor = mysql.connection.cursor()

    s = """select answer from questions where quiz_id=%s"""

    cursor.execute(s, (qid,))
    answers = cursor.fetchall()
    mysql.connection.commit()
    print(answers)
    cursor.close()
    no_que = len(answers)
    response = []
    correct_ans = []
    cursor = mysql.connection.cursor()

    s = """select question_id,question,opt1,opt2,opt3,opt4 from questions where quiz_id=%s"""

    cursor.execute(s, (qid,))
    questions = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
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
    
    que=[]
    for q in questions:
        
        a=q[0]
        b=q[1].strip()
        c=q[2].strip()
        d=q[3].strip()
        e=q[4].strip()
        f=q[5].strip()
        
        li=[a,b,c,d,e,f]
        
        que.append(li)
        
    
    info = zip(que, response,correct_ans)
    return render_template('answers.html',info=info,marks=ct,total=len(que))


app.run(host='127.0.0.1', port=3000, debug=True)
