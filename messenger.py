import datetime

import requests
import self as self
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

import clientui


class ExampleApp(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.pressed.connect(self.button_pushed)

        self.after = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_messages)
        self.timer.start(1000)

    def button_pushed(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        text = self.textEdit.toPlainText()

        self.send_message(username, password, text)

        self.textEdit.setText('')
        self.textEdit.repaint()

    def send_message(self, username, password, text):
        message = {'username': username, 'password': password, 'text': text}
        response = requests.post('http://127.0.0.1:5000/send', json=message)
        return response.status_code == 200

    def update_messages(self):
        response = requests.get(
            "http://127.0.0.1:5000/messages",
            params={'after': self.after}
        )
        data = response.json()
        for message in data['messages']:
            self.print_message(message)
            self.after = message['time']

    def print_message(self, message):
        username = message['username']
        message_time = message['time']
        text = message['text']

        dt = datetime.datetime.fromtimestamp(message_time)
        dt_beauty = dt.strftime('%H:%M:%S')

        self.show_text(f'{dt_beauty} {username}\n{text}\n\n')
        print(dt_beauty, username)
        print(text)
        print()

    def show_text(self, text):
        self.textBrowser.append(text)
        self.textBrowser.repaint()


app = QtWidgets.QApplication([])
window = ExampleApp()
window.show()
app.exec_()
