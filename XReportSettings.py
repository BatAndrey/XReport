# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QTextEdit, QComboBox, QVBoxLayout, QHBoxLayout,
                             QApplication, QMainWindow, QLabel, QLineEdit, QSpinBox, QPushButton)
from PyQt5.QtCore import (pyqtSignal)
from PyQt5 import QtCore
from PyQt5.QtCore import (QTimer)


class SettingsWidget(QWidget):
    settings_changed = pyqtSignal(int, str)
    #settings_changed_dir = pyqtSignal(str)
    settings_cancel = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.initGui()
        self.action_with_btn()


    def initGui(self):
        self.dir_lable = QLabel('dir path:')
        self.dir_line = QLineEdit()

        self.frequency_lable = QLabel('Check_frequency:')
        self.frequency_spin_box = QSpinBox()
        self.frequency_spin_box.setRange(500, 10000)
        self.frequency_spin_box.setSingleStep(250)

        self.ok_btn = QPushButton("SAVE")
        self.cancle_btn = QPushButton("CANCLE")

        vbox_lable = QVBoxLayout()
        vbox_lable.addWidget(self.dir_lable)
        vbox_lable.addWidget(self.frequency_lable)
        vbox_lable.addWidget(self.ok_btn)

        vbox_dir_freq = QVBoxLayout()
        vbox_dir_freq.addWidget(self.dir_line)
        vbox_dir_freq.addWidget(self.frequency_spin_box)
        vbox_dir_freq.addWidget(self.cancle_btn)

        hbox_btn = QHBoxLayout()
        hbox_btn.addLayout(vbox_lable)
        hbox_btn.addLayout(vbox_dir_freq)

        self.setLayout(hbox_btn)

        #self.ok_btn.pressed.connect(self.on_ok_btn)

    def on_ok_btn(self):
        self.settings_changed.emit(self.frequency_spin_box.value(), self.dir_line.text())
        #self.settings_changed_dir.emit(self.dir_line.text())
        self.deleteLater()
        self.close()

    def on_cancle_btn(self):
        self.settings_cancel.emit()
        #self.deleteLater()
        #self.close()

    def action_with_btn(self):
        self.ok_btn.pressed.connect(self.on_ok_btn)
        self.cancle_btn.clicked.connect(self.close)
        #self.cancle_btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        #self.cancle_btn.pressed.conncet(self.on_cancle_btn)
