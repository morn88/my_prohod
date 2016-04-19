import sys
from request_to_base import my_request
from PyQt4 import QtGui, QtCore


class OtkGui(QtGui.QWidget):
    def __init__(self):
        super(OtkGui, self).__init__()

        self.setGeometry(50, 50, 900, 600)
        self.setWindowTitle('Просмотр событий проходной')
        self.setWindowIcon(QtGui.QIcon('kpp.png'))

        self.btn = QtGui.QPushButton("Выбор даты", self)
        self.btn.resize(100, 25)
        self.btn.clicked.connect(self.show_date_choice)

        self.label = QtGui.QLabel('Выбранная дата: ', self)
        self.label1 = QtGui.QLabel(self)

        self.style_sheet = "::section{Background-color:#cdc8e3;color:black;}"

        self.table = QtGui.QTableWidget(0, 5, self)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem("Дата"))
        self.table.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("Время"))
        self.table.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem("Данные о сотруднике"))
        self.table.setColumnWidth(2, 200)
        self.table.setHorizontalHeaderItem(3, QtGui.QTableWidgetItem('Событие'))
        self.table.setHorizontalHeaderItem(4, QtGui.QTableWidgetItem('Место'))
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setStyleSheet(self.style_sheet)
        self.table.verticalHeader().setStyleSheet(self.style_sheet)
        self.table.setDisabled(True)

        self.my_grid = QtGui.QGridLayout(self)
        self.my_grid.addWidget(self.btn, 0, 0)
        self.my_grid.addWidget(self.label, 0, 1)
        self.my_grid.addWidget(self.label1, 0, 2)
        self.my_grid.addWidget(self.table, 1, 0, 1, 15)

        self.show()

    # Вызов модального окна, для выбора диапазона дат
    # todo сделать возможность выбора нескольких дат
    def show_date_choice(self):
        global modalWindow
        modalWindow = QtGui.QWidget(self, QtCore.Qt.Window)
        modalWindow.setWindowTitle("Выберите дату")
        modalWindow.setFixedSize(500, 300)
        modalWindow.setWindowModality(QtCore.Qt.WindowModal)
        modalWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        modalWindow.move(self.geometry().center() - modalWindow.rect().center() - QtCore.QPoint(4, 30))

        modalWindow.cld1 = QtGui.QCalendarWidget(modalWindow)
        modalWindow.cld1.setFirstDayOfWeek(1)
        modalWindow.cld1.setGridVisible(True)
        modalWindow.cld1.resize(modalWindow.size())
        modalWindow.cld1.setDateRange(QtCore.QDate.currentDate().addDays(-120), QtCore.QDate.currentDate())
        modalWindow.cld1.selectionChanged.connect(self.give_date)
        modalWindow.cld1.setHorizontalHeaderFormat(2)
        modalWindow.cld1.setVerticalHeaderFormat(0)

        modalWindow.show()

    # todo изменить функцию для диапазона дат, выбранных в функции show_date_choice
    def give_date(self):
        my_date = modalWindow.cld1.selectedDate()
        my_date2 = modalWindow.cld1.selectedDate()
        modalWindow.close()
        self.label1.setText(my_date.toString('dd.MM.yyyy') + ' - ' + my_date2.toString('dd.MM.yyyy'))
        my_date = my_date.toPyDate()
        print(my_date)
        my_list = my_request(my_date, my_date)
        if len(my_list) != 0:
            print('List was created')
            print(len(my_list))
            self.table.setRowCount(len(my_list))
            for i in range(len(my_list)):
                # print(len(my_list[i].split('/')))
                my_ready_list = my_list[i].split('#')
                for j in range(len(my_ready_list)):
                    self.table.setItem(i, j, QtGui.QTableWidgetItem(my_ready_list[j]))

            self.table.setAlternatingRowColors(True)
            self.table.setStyleSheet("alternate-background-color: #bdc4e2;background-color: #8f8c9e;");
            self.table.resizeColumnsToContents()
            self.table.setDisabled(False)

            # print(my_ready_list)

        else:
            print("List wasn't create")


def run():
    app = QtGui.QApplication(sys.argv)
    main_wind = OtkGui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
