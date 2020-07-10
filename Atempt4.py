# -*- coding: utf-8 -*-

# Здесь будет класс, который позволит работать с почтой.
# Авторизация, проверка наличия непрочитанных сообщений, проверка адреса отправителя, парсинг необходимых данных,
# Скачивание вложений письма.

import configparser
import imaplib
import email
import yadisk
import shutil
import re
import time
import sys
import os
from PyQt5.QtCore import QTimer


class DialogWithEmail:
    login = ''
    password = ''
    dir_download = ''

    def __init__(self):
        super().__init__()
        self.config_read(file_name='config_email_end.ini')
        self.connect = self.open_connection_email()
        self.main_logic()
        #self.connect.close()

    def config_read(self, file_name):
        self.config = configparser.ConfigParser()
        self.config.read(file_name)
        self.dir_download = self.config['FILE_DIR_DOWNLOAD']['dir_download']
        self.hostname = self.config.get('server', 'hostname')
        self.login = self.config.get('account', 'username')
        self.password = self.config.get('account', 'password')
        print('dir download--->', self.dir_download)

    def open_connection_email(self):
        print('connection to...', self.hostname)
        connection = imaplib.IMAP4_SSL(self.hostname)
        connection.login(self.login, self.password)
        print('login...', self.login)
        return connection

    def main_logic(self):
        while self.check_exist_unseen_msg() is True:
            file_name_download = self.download_other_file()
            file_part, file_exstansion = os.path.splitext(file_name_download)
            if file_exstansion != '.html':
                os.startfile(file_name_download)
            else:
                html_file = os.path.basename(file_name_download)
                ref = self.pars_ref(html_file)
                self.download_zip_archive(ref)
                self.unpack_zip()
                self.del_zip()
        else:
            print("unread file is not exist")

    def check_exist_unseen_msg(self):
        """Looking in email and make verifications the existence of unread messages"""

        response_server, status_box = self.connect.status('INBOX', '(MESSAGES UNSEEN)')
        print('STATUS BOX INBOX', status_box)
        decod_status = status_box[0].decode()
        print('decode status = ', decod_status)
        if 'UNSEEN 0' in decod_status:
            return False
        else:
            return True

    def download_other_file(self):
        msg_id_unseen = self.find_uread_msg()

        if msg_id_unseen[0] != '':
            #connect = self.open_connection_email()
            self.connect.select("INBOX", readonly=True)
            print('---->>', msg_id_unseen)

            for unread_msg in msg_id_unseen:
                response, msg_data = self.connect.fetch(unread_msg, 'RFC822')
                msg = email.message_from_string(msg_data[0][1].decode('utf-8'))

                for header in msg.walk():
                    if header.get_content_maintype() == 'multipart':
                        continue
                    if header.get('Content-Disposition') is None:
                        continue

                    filename_msg_create = unread_msg + '_' + header.get_filename()
                    print("File message", filename_msg_create)
                    path_filename = os.path.join(self.dir_download, filename_msg_create)

                    if not os.path.isfile(path_filename):
                        fp = open(path_filename, 'wb')
                        fp.write(header.get_payload(decode=True))
                        fp.close()
                    print('file path udo return', path_filename)
                    return path_filename
            #self.connect.close()
        else:
            print("We have not unseen msg")

    def pars_ref(self, file_name_html):
        """This function found url in .html file for using in function of download_zip_archive"""
        path_file = r'C:\Users\Днс\Desktop\протоколы\photo_research\\'
        with open(path_file + file_name_html, 'r')as f:
            line_ref = f.read()
            http_search = re.search('(https:/\S+)(\")', line_ref)
            group = http_search.group(1)
            file_name_search = re.search('([^>][u]\S+\s)', line_ref)
        return group

    def download_zip_archive(self, url):
        """Function for download .zip the attachment if we have url on yandex.disk.
        This function requires parsing .html"""

        path_file = self.dir_download.format('name.zip')
        y = yadisk.YaDisk()
        y.download_public(url, path_file)

    def unpack_zip(self):
        path_for_clean = self.dir_download
        path_for_unpack_archive = self.dir_download + r'\name'
        zip_file = r'\name.zip'

        if os.path.isfile(path_for_clean + zip_file):
            shutil.unpack_archive(path_for_clean + zip_file, path_for_unpack_archive)
        else:
            print('что то погло не так')

    def del_zip(self):
        path_for_clean = self.dir_download
        zip_file = r'\name.zip'
        os.remove(path_for_clean + zip_file)

    def find_uread_msg(self):
        #connect = self.open_connection_email()
        self.connect.select("INBOX", readonly=True)
        respons, msg_id_unseen = self.connect.search(None, 'UNSEEN')
        msg_id_unseen = msg_id_unseen[0].decode()
        self.connect.close()
        return msg_id_unseen.split(' ')

    def pars_data_person(self):
        self.inicials = ''
        self.data = ''
        self.age = ''
        self.organ = ''
        pass


x = DialogWithEmail()
print('--->', x)

