from werkzeug.utils import secure_filename
import openpyxl
from xlrd import open_workbook
import uuid
from flask import *
from fileinput import filename
import pandas
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
import csv
import cv2
import threading
import time
last_seen_time = None
cheat = 0
cheat_ct = 0
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
        time = request.form.get("time")

        f.save(f.filename)

        id = uuid.uuid4()
        ct = 1
        li = []
        try:
            with open(f.filename, mode='r')as file:

                csvFile = csv.reader(file)

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

            cursor = mysql.connection.cursor()
            cursor.execute(''' INSERT INTO time VALUES(%s,%s)''',
                           (id, time))

            mysql.connection.commit()
            cursor.close()
        except:
            return render_template('error.html', msg='Could not load data from mysql server')
    return render_template('acknowledgement.html', id=id)

    def detect_face_in_frame(frame, frame_region):

        face_cascade = cv2.CascadeClassifier(
            'C:/Users/HEET/Desktop/psc/main/haarcascade_frontalface_default.xml')

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray_frame, scaleFactor=1.1, minNeighbors=5)

        x, y, w, h = frame_region
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        face_in_frame = False
        for (x, y, w, h) in faces:
            if x > frame_region[0] and y > frame_region[1] and x + w < frame_region[2] and y + h < frame_region[3]:
                face_in_frame = True
                break

        if not face_in_frame:
            cv2.putText(frame, 'Please keep your face within the frame', (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow('Face detection', frame)

    cap = cv2.VideoCapture(0)

    frame_region = (100, 100, 500, 500)

    while True:

        ret, frame = cap.read()

        detect_face_in_frame(frame, frame_region)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def fun():
    def detect_face_in_frame(frame, frame_region):

        face_cascade = cv2.CascadeClassifier(
            'C:/Users/HEET/Desktop/psc/main/haarcascade_frontalface_default.xml')

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray_frame, scaleFactor=1.1, minNeighbors=5)

        x, y, w, h = frame_region
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        face_in_frame = False
        for (x, y, w, h) in faces:
            if x > frame_region[0] and y > frame_region[1] and x + w < frame_region[2] and y + h < frame_region[3]:
                face_in_frame = True
                break

        global last_seen_time
        global cheat_ct
        cheat_ct += 1
        if not face_in_frame:
            if last_seen_time is None:

                last_seen_time = time.monotonic()
            else:
                elapsed_time = time.monotonic() - last_seen_time
                if elapsed_time > 5:
                    cv2.destroyAllWindows()
                    cap.release()
                    global cheat
                    cheat = 1

                    exit()

                else:

                    cv2.putText(frame, 'Please keep your face within the frame', (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            last_seen_time = None

        cv2.imshow('Face detection', frame)

    cap = cv2.VideoCapture(0)

    frame_region = (100, 100, 500, 500)

    last_seen_time = None

    while True:

        ret, frame = cap.read()

        detect_face_in_frame(frame, frame_region)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


@app.route('/give')
def give():
    cheat = 0
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

            cursor = mysql.connection.cursor()

            s = """select time from time where quiz_id=%s"""

            cursor.execute(s, (qid,))
            time = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
        except:
            return render_template('error.html', msg='Could not load data from mysql server')
        if len(questions) == 0:
            return render_template('error.html', msg='No questions found for this quiz id')
        t1 = threading.Thread(target=fun)
        t1.start()

        t1 = threading.Thread(target=fun)
        t1.start()
        return render_template('start.html', questions=questions, time=time)


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

        x = request.form.get((str(i+1)))
        res = str(x)

        if len(res) != 0:
            res = res.strip()
        else:
            res = ''
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

    info = zip(que, response, correct_ans)
    empty = ''
    global cheat

    if cheat == 1:

        cheat = 0
        return render_template('error.html', msg="You have done cheating")
    else:
        return render_template('answers.html', info=info, marks=ct, total=len(que), empty=empty)


app.run(host='127.0.0.1', port=3000, debug=True)
