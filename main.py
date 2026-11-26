import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6 import uic


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels([
            "ID", "Название сорта", "Степень обжарки",
            "Молотый/В зернах", "Описание вкуса", "Цена", "Объем упаковки"
        ])

        self.load_data()

    def load_data(self):
        try:
            con = sqlite3.connect('coffee.sqlite')
            cur = con.cursor()
            cur.execute(
                "SELECT id, name, roast, ground, description, price, volume FROM coffee"
            )
            rows = cur.fetchall()

            self.tableWidget.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    self.tableWidget.setItem(
                        row_idx, col_idx, QTableWidgetItem(str(value))
                    )

            con.close()
        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")
            self.statusBar().showMessage(f"Ошибка БД: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
