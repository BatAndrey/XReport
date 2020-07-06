# -*- coding: utf-8 -*-

import sys
import configparser
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QTextEdit, QPushButton, QAction, QMainWindow, \
    QLineEdit, QApplication, QLayout, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QFormLayout, QStatusBar
from PyQt5.QtCore import (QTimer)
import XReportSettings

class XReportMainWindow(QMainWindow):
    tmpl_dir_path = ''
    check_frequence = 2000

    def __init__(self):
        super().__init__()
        self.read_config(file_name='config.ini')
        self.initGui()
        self.exchange_templates_combo()
        self.set_text_templates()
        self.set_timer_connect_email()
        self.action_with_settings()

    def read_config(self, file_name):
        config = configparser.ConfigParser()
        config.read(file_name)
        self.tmpl_dir_path = config['FILE_DIR_PATH']['dir_path']
        print(self.tmpl_dir_path)

    def initGui(self):
        self.main_window = QWidget()
        self.timer_connect_email = QTimer()


        self.setGeometry(400, 400, 700, 400)
        self.setWindowTitle('X-Report')

        self.templ_text_edid = QTextEdit()
        self.templ_combo_box = QComboBox()
        self.btn_connect = QPushButton("connect email")
        self.btn_compile_report = QPushButton("компилировать отчет")
        self.inicialis = QLineEdit()
        self.age = QLineEdit()
        self.data = QLineEdit()
        self.doctor = QLineEdit()

        self.vbox_text_combo = QVBoxLayout()
        self.vbox_text_combo.addWidget(self.templ_text_edid)
        self.vbox_text_combo.addWidget(self.templ_combo_box)
        self.vbox_text_combo.addWidget(self.btn_connect)

        self.vbox_data_person = QVBoxLayout()

        self.form_person = QFormLayout()
        self.form_person.addRow("ФИО", self.inicialis)
        self.form_person.addRow("Возраст", self.age)
        self.form_person.addRow("Дата", self.data)
        self.form_person.addRow("Врач", self.doctor)
        self.form_person.addRow(self.btn_compile_report)
        self.form_person.addRow(self.vbox_data_person)

        self.data.setInputMask("Дата приема: 99.B9.9999; _")
        self.age.setInputMask("Дата рождения: 99.B9.9999; _")

        self.hbox_all = QHBoxLayout()
        self.hbox_all.addLayout(self.vbox_text_combo)
        self.hbox_all.addLayout(self.form_person)

        self.main_window.setLayout(self.hbox_all)
        self.setCentralWidget(self.main_window)

        self.file_menu = self.menuBar().addMenu('File')

        self.show_settings_action = QAction('Settings')
        self.file_menu.addAction(self.show_settings_action)

    def exchange_templates_combo(self):
        item_for_combo = ['ogk', 'bone', 'air']
        self.templ_combo_box.addItems(item_for_combo)
        self.templ_combo_box.currentTextChanged.connect(self.set_text_templates)

    def set_text_templates(self):
        file_name = self.templ_combo_box.currentText()
        templ_text = self.read_file_templ(file_name=file_name)
        self.templ_text_edid.setText(templ_text)

        self.templ_text_edid.textChanged.connect(lambda: self.templ_combo_box.setDisabled(
            self.templ_text_edid.toPlainText() != ''))

    def read_file_templ(self, file_name):
        file_for_read = open(self.tmpl_dir_path + file_name + '.txt', 'r')
        tmp_text = file_for_read.readlines()
        file_for_read.close()
        return ' '.join(tmp_text)

    def set_timer_connect_email(self):
        self.timer_connect_email.timeout.connect(self.check_email)
        self.timer_connect_email.start(self.check_frequence)

    def check_email(self):
        print('mail exist')
        self.statusBar().showMessage('Checking mail...', 2000)
        connection = ConnectionEmail()
        if connection.exist_unread_msg():
            #self.statusBar().showMessage('Unread message exist')
            self.statusBar().messageChanged('Unread message exist')
            connection.download_msg()
            connection.close()
        else:
            print('Unread message unexist')
            connection.close()

    def ok_btn_connect_email(self):
        self.btn_connect.clicked.connect(self.check_email)

    def show_settings(self):
        self.settings_widget = XReportSettings.SettingsWidget()
        self.settings_widget.show()
        self.settings_widget.setAttribute(Qt.WA_DeleteOnClose)
        self.settings_widget.settings_changed.connect(self.apply_settings)

    def action_with_settings(self):
        self.show_settings_action.triggered.connect(self.show_settings)

    def apply_settings(self, freq, dir_path):
        self.tmpl_dir_path = dir_path
        self.check_frequency = freq
        print('apply settings', self.tmpl_dir_path)
        self.timer_connect_email.start(self.check_frequency)
        #dir_path_write = open('config.ini', 'a')
        #dir_path_write.writelines('\ndir_path={}'.format(self.tmpl_dir_path))
        #dir_path_write.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = XReportMainWindow()
    ex.show()
    # unittest.main()
    sys.exit(app.exec_())
