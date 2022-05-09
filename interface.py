import sys
import threading

import cv2
import gc
from datetime import datetime
import time, PIL, os
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PIL import ImageGrab
import numpy as np
from pynput import keyboard


def video_record():
    global name
    name = datetime.now().strftime('%Y-%m-%d %H-%M-%S')  # 当前的时间（当文件名）
    screen = ImageGrab.grab()  # 获取当前屏幕
    width, high = screen.size  # 获取当前屏幕的大小
    fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')  # MPEG-4编码,文件后缀可为.avi .asf .mov等
    video = cv2.VideoWriter('%s.mov' % name, fourcc, 15, (width, high))  # （文件名，编码器，帧率，视频宽高）
    # print('3秒后开始录制----')  # 可选
    # time.sleep(3)
    print('开始录制!')
    global start_time
    start_time = time.time()
    while True:
        if flag:
            print("录制结束！")
            global final_time
            final_time = time.time()
            video.release()  # 释放
            break
        im = ImageGrab.grab()  # 图片为RGB模式
        imm = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)  # 转为opencv的BGR模式
        video.write(imm)  # 写入
        # time.sleep(5) # 等待5秒再次循环


def on_press(key):  # 监听按键
    global flag
    if key == keyboard.Key.esc:
        flag = True  # 改变
        return False  # 返回False，键盘监听结束！


def video_info():  # 视频信息
    video = cv2.VideoCapture('%s.mov' % name)  # 记得文件名加格式不要错！
    fps = video.get(cv2.CAP_PROP_FPS)
    Count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print('帧率=%.1f' % fps)
    print('帧数=%.1f' % Count)
    print('分辨率', size)
    print('视频时间=%.3f秒' % (int(Count) / fps))
    print('录制时间=%.3f秒' % (final_time - start_time))
    print('推荐帧率=%.2f' % (fps * ((int(Count) / fps) / (final_time - start_time))))


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.font = QtGui.QFont()
        self.font.setBold(True)
        self.font.setPointSize(10)
        self.font.setWeight(10)
        self.resize(200, 50)
        self.setWindowTitle('截图工具')

        # 截图按钮设置
        self.but_scr = QPushButton('截图', self)
        self.but_scr.setFont(self.font)
        self.but_scr.setFlat(False)
        self.but_scr.setGeometry(1, 10, 50, 25)
        self.but_scr.clicked.connect(self.clickButton)
        # kbd.add_hotkey("esc", self.but_scr.clicked.connect(self.clickButton))

        # 录屏按钮设置
        self.but_save = QPushButton('录屏', self)
        self.but_save.setFont(self.font)
        self.but_save.setFlat(False)
        self.but_save.setGeometry(55, 10, 50, 25)
        # self.but_save.setBackgroundRole()
        self.but_save.clicked.connect(self.record_scree)

        # 退出界面按钮设置
        self.but_exit = QPushButton('退出', self)
        self.but_exit.setFlat(False)
        self.but_exit.setFont(self.font)
        self.but_exit.setGeometry(110, 10, 50, 25)
        self.but_exit.clicked.connect(self._tool_exit)

    def clickButton(self):
        # kbd.add_hotkey("shift+a", self.sender)
        # sender = self.sender()
        self.cut()

    def record_scree(self):
        th = threading.Thread(target=video_record)
        th.start()
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
        time.sleep(1)  # 等待视频释放过后
        video_info()

    def _tool_exit(self):
        exit()

    def test(self):
        print("截好需要的图开始下一次操作")

    def cut(self):
        self.scrren_cut()
        img = cv2.imread('screen.jpg')
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.on_mouse, img)
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        os.remove('screen.jpg')
        del img
        gc.collect()

    def scrren_cut(self):
        beg = time.time()
        debug = False
        # img = ImageGrab.grab(bbox=(250, 161, 1141, 610))
        image = ImageGrab.grab()
        image = image.convert('RGB')
        image.save("screen.jpg")

    def on_mouse(self, event, x, y, flags, param):
        global point1, point2
        img2 = param.copy()
        name = datetime.now().strftime('%Y-%m-%d %H-%M-%S')  # 当前的时间（当文件名）
        if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
            point1 = (x, y)
            cv2.circle(img2, point1, 10, (0, 255, 0), 5)
            cv2.imshow('image', img2)
        elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):  # 按住左键拖曳
            cv2.rectangle(img2, point1, (x, y), (255, 0, 0), 5)
            cv2.imshow('image', img2)
        elif event == cv2.EVENT_LBUTTONUP:  # 左键释放
            point2 = (x, y)
            cv2.rectangle(img2, point1, point2, (0, 0, 255), 5)
            cv2.imshow('image', img2)
            min_x = min(point1[0], point2[0])
            min_y = min(point1[1], point2[1])
            width = abs(point1[0] - point2[0])
            height = abs(point1[1] - point2[1])
            cut_img = param[min_y:min_y + height, min_x:min_x + width]
            cv2.imwrite('./picture/{}_photo.png'.format(name), cut_img)


if __name__ == '__main__':
    flag = False
    app = QApplication(sys.argv)
    main = MainWindow()
    main.setWindowOpacity(0.7)
    main.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    main.move(0, 100)
    main.show()
    sys.exit(app.exec_())

