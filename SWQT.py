import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTimeEdit, QLabel, QMessageBox, QHBoxLayout, QDialog
)
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtMultimedia import QSound

class ArcProgress(QWidget):
    def __init__(self):
        super().__init__()
        self.progress = 0.0
        self.color = QColor(70, 130, 180)  # Steel Blue

    def setProgress(self, value):
        self.progress = max(0.0, min(1.0, value))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        pen = QPen(self.color, 10)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing)
        start_angle = 90 * 16
        span_angle = -int(360 * self.progress * 16)
        painter.drawArc(rect.adjusted(10, 10, -10, -10),
                        start_angle, span_angle)

class CountdownApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Countdown Timer")
        self.setFixedSize(320, 450)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.timeEdit = QTimeEdit()
        self.timeEdit.setDisplayFormat("HH:mm:ss")
        self.timeEdit.setTime(QTime(0, 1, 0))  # Default 1 min
        self.layout.addWidget(self.timeEdit)

        # Control Buttons
        button_layout = QHBoxLayout()
        self.startButton = QPushButton("Start")
        self.startButton.clicked.connect(self.toggleStartPause)
        self.resetButton = QPushButton("Reset")
        self.resetButton.clicked.connect(self.resetTimer)
        button_layout.addWidget(self.startButton)
        button_layout.addWidget(self.resetButton)
        self.layout.addLayout(button_layout)

        self.timeLabel = QLabel("Time left: 00:00:00")
        self.timeLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.timeLabel)

        self.arcWidget = ArcProgress()
        self.arcWidget.setFixedSize(220, 220)
        self.layout.addWidget(self.arcWidget, alignment=Qt.AlignCenter)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateCountdown)

        self.total_seconds = 0
        self.remaining_seconds = 0
        self.isRunning = False

    def toggleStartPause(self):
        if not self.isRunning:
            if self.remaining_seconds == 0:
                self.total_seconds = (
                    self.timeEdit.time().hour() * 3600 +
                    self.timeEdit.time().minute() * 60 +
                    self.timeEdit.time().second()
                )
                if self.total_seconds == 0:
                    return
                self.remaining_seconds = self.total_seconds
            self.timer.start(1000)
            self.isRunning = True
            self.startButton.setText("Pause")
        else:
            self.timer.stop()
            self.isRunning = False
            self.startButton.setText("Resume")
        self.updateDisplay()

    def resetTimer(self):
        self.timer.stop()
        self.isRunning = False
        self.remaining_seconds = 0
        self.startButton.setText("Start")
        self.arcWidget.setProgress(0.0)
        self.timeLabel.setText("Time left: 00:00:00")

    def updateCountdown(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.updateDisplay()
        else:
            self.timer.stop()
            QSound.play("alarm.wav")  # Make sure this file exists
            self.arcWidget.setProgress(1.0)
            self.startButton.setText("Start")
            self.isRunning = False
            self.remaining_seconds = 0
            self.showNotification()

    def updateDisplay(self):
        time_str = QTime(0, 0, 0).addSecs(self.remaining_seconds).toString("HH:mm:ss")
        self.timeLabel.setText(f"Time left: {time_str}")
        if self.total_seconds > 0:
            progress = 1 - (self.remaining_seconds / self.total_seconds)
            self.arcWidget.setProgress(progress)

    def showNotification(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Time's Up!")
        dialog.setFixedSize(300, 150)
        layout = QVBoxLayout()

        message_label = QLabel("The countdown has finished!")
        message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(message_label)

        # Add a custom button to close the dialog
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button, alignment=Qt.AlignCenter)

        dialog.setLayout(layout)
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CountdownApp()
    win.show()
    sys.exit(app.exec_())
