import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QDialog, QLineEdit, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QSound

flag=1
class MatrixEffect(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: black; color: green; font-size: 20px;")
        self.setWindowOpacity(0.9)  # Adjust the opacity level here (0.0 to 1.0)

        self.labels = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.drop_numbers)
        self.timer.start(100)  # Update every 100 milliseconds     self.close_button.clicked.connect(self.close_timer)
        

    def drop_numbers(self):
        number = str(random.randint(0, 1))

        label = QLabel(number, self)
        label.setStyleSheet("background-color: transparent; color: green;")  # Set transparent background
        label.move(random.randint(0, self.width()), -30)
        label.show()

        self.labels.append(label)
        self.move_labels()

    def move_labels(self):
        for label in self.labels:
            pos = label.pos()
            if pos.y() < self.height():
                label.move(pos.x(), pos.y() + 20)
            else:
                label.deleteLater()
                self.labels.remove(label)

class TimerWindow(QDialog):
    def __init__(self, study_time, break_time, main_window):
        super().__init__()
        self.study_time = study_time
        self.break_time = break_time
        self.initial_study_time = study_time
        self.initial_break_time = break_time
        self.is_studying = True
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Timer Window')
        self.setGeometry(0, 0, 300, 0)
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: black; color: white;")
        screen_geometry = QApplication.desktop().screenGeometry()
        #self.move((screen_geometry.width() - self.width()) / 2, 0)
        self.move((screen_geometry.width() - self.width()) // 2, 0)
		#self.setAttribute(Qt.WA_TranslucentBackground)  # Set the window as translucent

        self.timer_label = QLabel()
        self.nonosignature = QLabel()

        self.pause_button = QPushButton()
        self.pause_button.setIcon(QIcon.fromTheme("media-playback-pause"))  # Replace with desired icon
        self.pause_button.setFixedSize(30, 30)  # Set the size of the button

        self.reset_button = QPushButton()
        self.reset_button.setIcon(QIcon.fromTheme("view-refresh"))  # Replace with desired icon
        self.reset_button.setFixedSize(30, 30)  # Set the size of the button

        self.close_button = QPushButton()
        self.close_button.setIcon(QIcon.fromTheme("application-exit"))  # Replace with desired icon
        self.close_button.setFixedSize(30, 30)  # Set the size of the button

        main_layout = QVBoxLayout()  # Main vertical layout

        timer_buttons_layout = QHBoxLayout()  # Nested horizontal layout for timer and buttons
        timer_buttons_layout.addWidget(self.timer_label)
        timer_buttons_layout.addStretch()  # Add stretchable space between label and buttons
        timer_buttons_layout.addWidget(self.pause_button)
        timer_buttons_layout.addWidget(self.reset_button)
        timer_buttons_layout.addWidget(self.close_button)
        timer_buttons_layout.addWidget(self.nonosignature)
        
        

        main_layout.addLayout(timer_buttons_layout)  # Add nested layout to the main layout
        main_layout.addStretch()  # Add stretchable space below the buttons
        self.setLayout(main_layout)


        # Adding the MatrixEffect as a child widget
        # Adding the MatrixEffect as a child widget
        self.matrix_effect = MatrixEffect()
        self.matrix_effect.setParent(self)
        self.matrix_effect.setGeometry(0, 0, 300, 150)

        # Raise buttons to ensure they are clickable
        self.pause_button.raise_()
        self.reset_button.raise_()
        self.close_button.raise_()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Update every 1 second
        self.close_button.clicked.connect(self.close_timer)
        self.pause_button.clicked.connect(self.pause_timer)
        self.reset_button.clicked.connect(self.reset_timer)
    def update_timer(self):
		
        global flag
        if flag>0:self.nonosignature.setText(f"<span style='font-weight: bold; font-size: 14px;color:green;'>Nono was here :)");flag=0
        else :			self.nonosignature.setText(f"<span style='font-weight: bold; font-size: 14px;color:yellow;'>Nono was here :)");flag=1


			
        if self.is_studying:
            if self.study_time > 0:
                self.timer_label.setText(f"Study Time: {self.study_time} sec")
                self.study_time -= 1
            else:
                self.is_studying = False
                self.alarm()
                self.break_time = self.initial_break_time
        else:
            if self.break_time > 0:
                self.timer_label.setText(f"Break Time: {self.break_time} sec")
                self.break_time -= 1
            else:
                self.is_studying = True
                self.alarm()
                self.study_time = self.initial_study_time

    def pause_timer(self):
        if self.timer.isActive():
            self.pause_button.setIcon(QIcon.fromTheme("media-playback-start"))
            self.timer.stop()
        else:
            self.pause_button.setIcon(QIcon.fromTheme("media-playback-pause"))
            self.timer.start(1000)

    def reset_timer(self):
        self.timer.stop()
        self.study_time = self.initial_study_time
        self.break_time = self.initial_break_time
        self.is_studying = True
        self.timer_label.setText(f"Study Time: {self.study_time} sec")
        self.timer.start(1000)  # Restart the timer

    def close_timer(self):
        self.timer.stop()
        self.close()
        self.main_window.show()
        
    def alarm(self):
        QSound.play("/home/nonososo/12.wav")  # Replace with the path to your sound file


class TransparentTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.alarm()
        self.setWindowTitle('Transparent Timer')
        self.setGeometry(100, 100, 300, 200)
        self.setWindowOpacity(0.7)  # Adjust the opacity level here (0.0 to 1.0)
        #self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.setStyleSheet("background-color: black; color: white;")

        self.timer_label = QLabel('Enter study time (minutes):')
        self.study_input = QLineEdit()
        self.break_label = QLabel('Enter break time (minutes):')
        self.break_input = QLineEdit()

        self.start_button = QPushButton('Start Timer')

        layout = QVBoxLayout()
        layout.addWidget(self.timer_label)
        layout.addWidget(self.study_input)
        layout.addWidget(self.break_label)
        layout.addWidget(self.break_input)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

        self.start_button.clicked.connect(self.show_timer_window)

    def show_timer_window(self):
        study_time = int(self.study_input.text()) * 60
        break_time = int(self.break_input.text()) * 60
        self.hide()
        self.timer_window = TimerWindow(study_time, break_time, self)
        self.timer_window.show()

        # Adding the MatrixEffect as a child widget
        self.matrix_effect = MatrixEffect()
        self.matrix_effect.setParent(self.timer_window)
        self.matrix_effect.setGeometry(0, 0, 300, 150)
    def alarm(self):
        QSound.play("/home/nonososo/12.wav")

def main():
    flag=1
    app = QApplication(sys.argv)
    ex = TransparentTimer()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
