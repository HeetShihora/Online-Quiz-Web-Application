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
global last_seen_time

# import time
# import pyautogui
# from face import *
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
        print("******", time, "*********")
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

            cursor = mysql.connection.cursor()
            cursor.execute(''' INSERT INTO time VALUES(%s,%s)''',
                           (id, time))

            mysql.connection.commit()
            cursor.close()
        except:
            return render_template('error.html', msg='Could not load data from mysql server')
    return render_template('acknowledgement.html', id=id)

# def fun():
    def detect_face_in_frame(frame, frame_region):
        # Load the face detection classifier
        face_cascade = cv2.CascadeClassifier(
            'C:/Users/HEET/Desktop/psc/main/haarcascade_frontalface_default.xml')

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(
            gray_frame, scaleFactor=1.1, minNeighbors=5)

        # Draw a rectangle in the specified frame region
        x, y, w, h = frame_region
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Check if any detected face falls within the specified frame region
        face_in_frame = False
        for (x, y, w, h) in faces:
            if x > frame_region[0] and y > frame_region[1] and x + w < frame_region[2] and y + h < frame_region[3]:
                face_in_frame = True
                break

        # Display a message if the detected face is not within the specified frame region
        if not face_in_frame:
            cv2.putText(frame, 'Please keep your face within the frame', (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        # Display the resulting frame
        cv2.imshow('Face detection', frame)

    # Open the video stream from the user's camera
    cap = cv2.VideoCapture(0)

    # Set the frame region in which the face should be detected
    frame_region = (100, 100, 500, 500)

    while True:
        # Capture a frame from the video stream
        ret, frame = cap.read()

        # Detect faces in the frame and check if the detected face falls within the specified region
        detect_face_in_frame(frame, frame_region)

        # Exit the loop if the user presses the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video stream and close all windows
    cap.release()
    cv2.destroyAllWindows()
# extra


def fun():
    def detect_face_in_frame(frame, frame_region):
        # Load the face detection classifier
        face_cascade = cv2.CascadeClassifier(
            'C:/Users/HEET/Desktop/psc/main/haarcascade_frontalface_default.xml')

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(
            gray_frame, scaleFactor=1.1, minNeighbors=5)

        # Draw a rectangle in the specified frame region
        x, y, w, h = frame_region
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Check if any detected face falls within the specified frame region
        face_in_frame = False
        for (x, y, w, h) in faces:
            if x > frame_region[0] and y > frame_region[1] and x + w < frame_region[2] and y + h < frame_region[3]:
                face_in_frame = True
                break

        # Display a message if the detected face is not within the specified frame region

        if not face_in_frame:
            last_seen_time = time.monotonic()
            if last_seen_time is None:
                pass
            else:
                elapsed_time = time.monotonic() - last_seen_time
                if elapsed_time > 10:
                    t1.join()
                    return render_template('error.html')
                    cv2.destroyAllWindows()
                    cap.release()
                    exit()
                else:
                    cv2.putText(frame, 'Please keep your face within the frame', (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            last_seen_time = None

        # Display the resulting frame
        cv2.imshow('Face detection', frame)

    # Open the video stream from the user's camera
    cap = cv2.VideoCapture(0)

    # Set the frame region in which the face should be detected
    frame_region = (100, 100, 500, 500)

    # last_seen_time = 0

    while True:
        # Capture a frame from the video stream
        ret, frame = cap.read()

        # Detect faces in the frame and check if the detected face falls within the specified region
        detect_face_in_frame(frame, frame_region)

        # Exit the loop if the user presses the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video stream and close all windows
    cap.release()
    cv2.destroyAllWindows()




t1 = threading.Thread(target=fun)
@app.route('/give')
def give():
    # pyautogui.press('f11')
    return render_template('give.html')


@app.route('/start', methods=['POST'])
def start():
    if request.method == 'POST':
        # start_detection()
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

        t1.start()
        # t1.kill()
        t1.join()
        # t1 = threading.Thread(target=fun)
        # t1.start()
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

        x = request.form.get((str(i+1)))
        res = str(x)
        # print(type(res))
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
    print('\n\n')
    print(que)
    print('\n\n')
    print(response)
    print('\n\n')
    print(correct_ans)
    print('\n\n')
    info = zip(que, response, correct_ans)
    empty = ''
    
    return render_template('answers.html', info=info, marks=ct, total=len(que), empty=empty)


app.run(host='127.0.0.1', port=3000, debug=True)
