import dlib
import cv2
import imutils
import serial
import time
import sys

arduino = serial.Serial('COM11', 9600)
time.sleep(2)
print("Connection to arduino...")


stream = cv2.VideoCapture(0)

# 面部识别器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# 标记面部四周
def draw_border(img, pt1, pt2, color, thickness):
    x1, y1 = pt1
    x2, y2 = pt2
    wt = abs(x1 - x2)
    ht = abs(y1 - y2)

    cv2.line(img, (x1,y1), (x1 + wt,y1), color, thickness)
    cv2.line(img, (x1 + wt,y1), (x1 + wt,y1 + ht), color, thickness)
    cv2.line(img, (x1 + wt,y1 + ht), (x1,y1 + ht), color, thickness)
    cv2.line(img, (x1,y1 + ht), (x1,y1), color, thickness)


while True:
    # 读入摄像头
    (grabbed, frame) = stream.read()

    # 灰度化
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 复制绘图图层
    frame2 = frame.copy()
    output = frame.copy()

    cv2.line(frame2, (0,200), (500,200), (255,255,255), 2)
    cv2.line(frame2, (250,0), (250,500), (255,255,255), 2)

    # 识别
    face_rects = detector(gray, 0)
    

    # 循环标记面部
    for i, d in enumerate(face_rects):
        x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()

        xx = int(d.left() + d.right()) / 2
        yy = int(d.top() + d.bottom()) / 2

        # 面部周围边框绘制
        draw_border(frame2, (x1, y1), (x2, y2), (255,0,0), 2)

        #面部轮廓检测
        face_shapes = predictor(gray, d)

        for point_id in range(0, 67):
            pt = (face_shapes.part(point_id).x, face_shapes.part(point_id).y)
            #print(face_shapes.part(point_id).x,face_shapes.part(point_id).y)
            cv2.circle(frame2, pt, 3, color = (0,255,0))

        center = (xx,yy)

        #云台串口
        #print("Center of Rectangle is :", center)
        data = "X{0:d}Y{1:d}Z".format(int(xx), int(yy))
        #print ("output = '" +data+ "'")
        sdata = bytes(data, encoding = "utf8")
        arduino.write(sdata)
       
    cv2.imshow("Face Detection", frame2)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cv2.destroyAllWindows()
stream.stop()