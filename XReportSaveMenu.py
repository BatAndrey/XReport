# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QTextEdit, QPushButton, QAction, QMainWindow, \
    QLineEdit, QApplication, QLayout, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QFormLayout, QStatusBar
from PyQt5.QtCore import (QTimer)

class SaveMenu(QWidget):

    def __init__(self):
        super().__init__()

    def initUi(self):

        self.save_menu_wedget = QtWidgets.QFileDialog.Options()

        #self.save_menu_wedget = QWidget

    # def saveToFile(self):
    #     options = QtWidgets.QFileDialog.Options()
    #     self.fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save To File", "", "Text Files (*.txt)", options=options)
    #     if self.fileName:
    #         self.writeFile = open(self.fileName, 'w', encoding='utf-8')
    #         self.writeFile.write(self.ui.plainTextEdit.toPlainText())
    #         self.writeFile.close()
    #         self.ui.statusbar.showMessage('Saved to %s' % self.fileName)