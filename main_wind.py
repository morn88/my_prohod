import sys
import datetime
from request_to_base import my_request
from PyQt4 import QtGui, QtCore


class OtkGui(QtGui.QWidget):
    def __init__(self):
        super(OtkGui, self).__init__()

        self.setGeometry(50, 50, 720, 500)
        self.setWindowTitle('Просмотр событий проходной')
        self.setWindowIcon(QtGui.QIcon('kpp.png'))

        self.btn = QtGui.QPushButton("Выбор даты", self)
        self.btn.move(10, 5)
        self.btn.resize(100, 25)
        self.btn.clicked.connect(self.show_date_choice)
        self.label1 = QtGui.QLabel('Тут будет дата', self)
        self.label1.move(120, 10)

        self.table = QtGui.QTableWidget(5, 5, self)
        self.table.move(10, 35)
        self.table.resize(700, 400)
        self.table.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem("Дата"))
        self.table.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("Время"))
        self.table.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem("ФИО"))


        self.show()

    # Вызов модального окна, для выбора диапазона дат
    # todo сделать возможность выбора нескольких дат
    def show_date_choice(self):
        global modalWindow
        modalWindow = QtGui.QWidget(self, QtCore.Qt.Window)
        modalWindow.setWindowTitle("Выберите дату")
        # modalWindow.resize(500, 300)
        modalWindow.setFixedHeight(300)
        modalWindow.setFixedWidth(500)
        modalWindow.setWindowModality(QtCore.Qt.WindowModal)
        modalWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        modalWindow.move(self.geometry().center() - modalWindow.rect().center() - QtCore.QPoint(4, 30))
        modalWindow.cld1 = QtGui.QCalendarWidget(modalWindow)
        modalWindow.cld1.setFirstDayOfWeek(1)
        modalWindow.cld1.setGridVisible(True)
        modalWindow.cld1.resize(modalWindow.size())
        modalWindow.cld1.setMaximumDate(QtCore.QDate.currentDate())
        modalWindow.cld1.setMinimumDate(QtCore.QDate.currentDate().addDays(-120))
        modalWindow.cld1.selectionChanged.connect(self.give_date)
        modalWindow.show()

        modalWindow.cld1.setHorizontalHeaderFormat(2)
    # todo добавить функцию выполняющую запрос, для диапазона дат, выбранных в функции show_date_choice
    def give_date(self):
        my_date = modalWindow.cld1.selectedDate()
        self.label1.setText(my_date.toString('dd.MM.yyyy'))
        my_date = my_date.toPyDate()
        print(my_date)
        my_list = my_request(my_date, my_date)
        if len(my_list) != 0:
            print('List was created')
            print(len(my_list))
            self.table.setRowCount(len(my_list))
            for i in my_list:
                print(len(i.split('/')))

                print(i)
        else:
            print("List wasn't create")


def run():
    app = QtGui.QApplication(sys.argv)
    main_wind = OtkGui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
