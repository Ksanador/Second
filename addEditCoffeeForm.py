import sqlite3
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic


class AddEditCoffeeForm(QDialog):
    def __init__(self, coffee_id=None, parent=None):
        """
        coffee_id = None  -> режим добавления
        coffee_id = int   -> режим редактирования
        """
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.coffee_id = coffee_id

        if coffee_id is None:
            self.setWindowTitle("Добавление кофе")
        else:
            self.setWindowTitle("Редактирование кофе")
            self.load_existing()

        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.reject)

    def load_existing(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        cur.execute(
            "SELECT name, roast, ground, description, price, volume "
            "FROM coffee WHERE id = ?", (self.coffee_id,)
        )
        row = cur.fetchone()
        con.close()

        if row is None:
            QMessageBox.warning(self, "Ошибка", "Запись не найдена")
            self.reject()
            return

        name, roast, ground, description, price, volume = row
        self.nameEdit.setText(name)
        self.roastCombo.setCurrentText(roast)
        self.groundCombo.setCurrentText(ground)
        self.descEdit.setPlainText(description)
        self.priceSpin.setValue(price)
        self.volumeSpin.setValue(volume)

    def save(self):
        name = self.nameEdit.text().strip()
        description = self.descEdit.toPlainText().strip()

        if not name or not description:
            QMessageBox.warning(self, "Ошибка",
                                "Заполните название и описание вкуса")
            return

        roast = self.roastCombo.currentText()
        ground = self.groundCombo.currentText()
        price = self.priceSpin.value()
        volume = self.volumeSpin.value()

        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()

        if self.coffee_id is None:
            cur.execute(
                "INSERT INTO coffee (name, roast, ground, description, price, volume) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (name, roast, ground, description, price, volume)
            )
        else:
            cur.execute(
                "UPDATE coffee SET name=?, roast=?, ground=?, description=?, "
                "price=?, volume=? WHERE id=?",
                (name, roast, ground, description, price, volume, self.coffee_id)
            )

        con.commit()
        con.close()
        self.accept()
