from flask import Flask, render_template, Response
import cv2
import numpy as np
import time
import pafy
import PoseModule as pm


app = Flask(__name__)
# cap1 = cv2.VideoCapture(0)
video1 = pafy.new("https://www.youtube.com/watch?v=Ic1f9wKjoJg")
best1 = video1.getbest(preftype="mp4")
cap1 = cv2.VideoCapture(best1.url)

video2 = pafy.new("https://www.youtube.com/watch?v=Ic1f9wKjoJg")
best2 = video2.getbest(preftype="mp4")
cap2 = cv2.VideoCapture(best2.url)

video3 = pafy.new("https://www.youtube.com/watch?v=Ic1f9wKjoJg")
best3 = video3.getbest(preftype="mp4")
cap3 = cv2.VideoCapture(best3.url)

video4 = pafy.new("https://www.youtube.com/watch?v=Ic1f9wKjoJg")
best4 = video4.getbest(preftype="mp4")
cap4 = cv2.VideoCapture(best4.url)

def generate_frames(cap):
    fall = False
    detector = pm.poseDetector()
    pTime = 0
    
    while True:
        success, img = cap.read()
        img = cv2.resize(img, (1280, 720))
        # img = cv2.imread("AiTrainer/test.jpg")
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        #print(lmList)
        if len(lmList) != 0:
            # Right Arm
            angle = detector.findAngle(img, 12, 24, 26)
            if angle < 80:
                fall = True
            elif angle > 280:
                fall = True
            else:
                fall = False
            if cap1:
                with open("fall_value1.txt", "w") as f:
                    f.write(str(fall))
            if cap2:
                with open("fall_value2.txt", "w") as f:
                    f.write(str(fall))
            if cap3:
                with open("fall_value3.txt", "w") as f:
                    f.write(str(fall))
            if cap4:
                with open("fall_value4.txt", "w") as f:
                    f.write(str(fall))
            #print(fall)     
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video1')
def video1():
    return Response(generate_frames(cap1), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video2')
def video2():
    return Response(generate_frames(cap2), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video3')
def video3():
    return Response(generate_frames(cap3), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/video4')
def video4():
    return Response(generate_frames(cap4), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port= 8000)