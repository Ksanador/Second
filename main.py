import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6 import uic

from addEditCoffeeForm import AddEditCoffeeForm


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels([
            "ID", "Название сорта", "Степень обжарки",
            "Молотый/В зернах", "Описание вкуса", "Цена", "Объем упаковки"
        ])
        self.tableWidget.setColumnHidden(0, False)  # ID можно показывать

        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)
        self.tableWidget.doubleClicked.connect(self.edit_coffee)

        self.load_data()

    def load_data(self):
        try:
            con = sqlite3.connect('coffee.sqlite')
            cur = con.cursor()
            cur.execute(
                "SELECT id, name, roast, ground, description, price, volume "
                "FROM coffee ORDER BY id"
            )
            rows = cur.fetchall()
            con.close()

            self.tableWidget.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    self.tableWidget.setItem(
                        row_idx, col_idx, QTableWidgetItem(str(value))
                    )
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка БД", str(e))

    def add_coffee(self):
        dialog = AddEditCoffeeForm(coffee_id=None, parent=self)
        if dialog.exec():
            self.load_data()

    def edit_coffee(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.information(self, "Информация",
                                    "Выберите запись для редактирования")
            return

        coffee_id = int(self.tableWidget.item(row, 0).text())
        dialog = AddEditCoffeeForm(coffee_id=coffee_id, parent=self)
        if dialog.exec():
            self.load_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())