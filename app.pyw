import sys
from PyQt5.QtCore import QTimer, QTime, Qt, QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QWidget, QLCDNumber, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox

class Countdown(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('倒计时')
        self.resize(400, 300)
        self.center()
        self.lcd = QLCDNumber(self)
        self.lcd.setDigitCount(10)
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        font = QFont()
        font.setPointSize(72)
        self.lcd.setFont(font)
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.lcd)

        hbox1 = QHBoxLayout()
        self.startButton = QPushButton('开始', self)
        self.startButton.clicked.connect(self.start)
        hbox1.addWidget(self.startButton)

        self.pauseButton = QPushButton('暂停', self)
        self.pauseButton.clicked.connect(self.pause)
        hbox1.addWidget(self.pauseButton)

        # self.resetButton = QPushButton('重置', self)
        # self.resetButton.clicked.connect(self.reset)
        # hbox1.addWidget(self.resetButton)

        self.timeComboBox = QComboBox(self)
        self.timeComboBox.addItems(['1分钟', '2分钟', '3分钟', '4分钟', '5分钟'])
        self.timeComboBox.currentIndexChanged.connect(self.changeTime)
        hbox1.addWidget(self.timeComboBox)

        vbox.addLayout(hbox1)

        self.setLayout(vbox)
        self.show()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.time = QTime(0, 1, 0)
        self.remainingTime = self.time
        self.player = QMediaPlayer(self)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile('resource/audio.mp3')))
        self.pauseFlag = False

    def center(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showTime(self):
        self.remainingTime = self.remainingTime.addMSecs(-10)
        self.lcd.display(self.remainingTime.toString('mm:ss.zzz'))
        if self.remainingTime == QTime(0, 0, 0):
            self.timer.stop()
            self.player.play()
            self.startButton.setText('开始')
            self.pauseButton.setEnabled(False)
            self.resetButton.setEnabled(True)

    def start(self):
        if self.startButton.text() == '开始':
            self.startButton.setText('重置')
            self.pauseButton.setEnabled(True)
            # self.resetButton.setEnabled(False)
            self.remainingTime = self.time
            self.lcd.display(self.remainingTime.toString('mm:ss.zzz'))
            self.timer.start(10)
        else:
            self.reset()

    def pause(self):
        if not self.pauseFlag:
            self.pauseButton.setText('继续')
            self.timer.stop()
            self.pauseFlag = True
        else:
            self.pauseButton.setText('暂停')
            self.timer.start(10)
            self.pauseFlag = False

    def reset(self):
        self.startButton.setText('开始')
        self.pauseButton.setEnabled(False)
        # self.resetButton.setEnabled(False)
        self.timer.stop()
        self.remainingTime = self.time
        self.lcd.display(self.remainingTime.toString('mm:ss.zzz'))
        self.pauseFlag = False

    def changeTime(self):
        if self.timeComboBox.currentText() == '1分钟':
            self.time = QTime(0, 1, 0)
        elif self.timeComboBox.currentText() == '2分钟':
            self.time = QTime(0, 2, 0)
        elif self.timeComboBox.currentText() == '3分钟':
            self.time = QTime(0, 3, 0)
        elif self.timeComboBox.currentText() == '4分钟':
            self.time = QTime(0, 4, 0)
        elif self.timeComboBox.currentText() == '5分钟':
            self.time = QTime(0, 5, 0)
        self.remainingTime = self.time
        self.lcd.display(self.remainingTime.toString('mm:ss.zzz'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Countdown()
    sys.exit(app.exec_())
