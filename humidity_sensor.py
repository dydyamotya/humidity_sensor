from PySide2 import QtWidgets

import serial
import logging
import datetime
import threading
import time

logger = logging.getLogger(__name__)


def get_logging_name():
    return datetime.datetime.now().strftime("%Y.%m.%d-%H.%M.%S.log")


class MainWidget(QtWidgets.QWidget):
    def __init__(self):

        super().__init__()
        self.stopped = True

        layout = QtWidgets.QVBoxLayout()

        self.port_box = QtWidgets.QLineEdit()
        layout.addWidget(self.port_box)

        start_button = QtWidgets.QPushButton(text="Start")
        start_button.clicked.connect(self.start_thread)
        layout.addWidget(start_button)

        stop_button = QtWidgets.QPushButton(text="Stop")
        stop_button.clicked.connect(self.stop_thread)
        layout.addWidget(stop_button)

        self.status_label = QtWidgets.QLabel()
        layout.addWidget(self.status_label)
        

        self.setLayout(layout)
        self.show()

    def start_thread(self):
        self.stopped = False

        thread = threading.Thread(target=self.cycle)
        thread.daemon = True
        thread.start()

    def stop_thread(self):
        self.stopped = True

    def cycle(self):
        try:
            ser = serial.Serial(port=self.port_box.text(), baudrate=9600)
        except:
            self.stopped = True
        else:
            while not self.stopped:
                try:
                    ser.flushInput()
                    ser.readline()
                    line = ser.readline().decode("ascii").strip()
                    self.status_label.setText(line)
                    logger.info(line)
                    time.sleep(1)
                except:
                    pass
            ser.close()


def main():
    logging.basicConfig(filename=get_logging_name(), level=logging.INFO, format='%(asctime)s  %(message)s')
    app = QtWidgets.QApplication([])
    widget = MainWidget()
    app.exec_()


if __name__ == "__main__":
    main()
