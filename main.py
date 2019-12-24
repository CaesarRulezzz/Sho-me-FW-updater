#!/usr/bin/python3
import urllib.request
from bs4 import BeautifulSoup
import re
from tkinter import messagebox
import sys
import subprocess
import os

#firmware_download_link = "https://sho-me.ru/downloads/obnovleniya/firmware/{0}-{1}-{2}/sho-me-combo-N1-signature-firmware.zip"
firmware_download_link = "https://sho-me.ru/downloads/obnovleniya/firmware/{0}-{1}-{2}/sho-me-combo-N1-signature-firmware-sw.zip"

# read version from file
try:
    config = open('version.txt', 'r')
    version = config.read()
    config.close()
    print('Last checked version:', version)
except:
    print('Could not open version file!')
    version = '0.0.0'

# open forum page with FW posts
update_page = urllib.request.urlopen('https://sho-me.ru/novosti/novye-proshivki-dlya-kombo-ustroystv-sho-me-combo-n1-signature-smart-signature')

str_var = ''
new_str = ''
version_latest = ''

# parsing with BeautifulSoup4
soup = BeautifulSoup(update_page.read().decode(), "html.parser")
first_font_tag = soup.find('p', string=re.compile(r'Список изменений от '))
if first_font_tag is not None:
    version_latest = first_font_tag.text.split(' ')[3][:-2]

# check version
if version_latest != version:
    print('FOUND NEW FW VERSION!!!', version_latest)
    messagebox.showinfo(message="Обнаружена новая версия прошивки SHO-ME Combo №1 Signature!", icon='info', title='Внимание!')
    if messagebox.askyesno(message='Скачать новую версию прошивки сейчас?', icon='question', title='Обновление SHO-ME Combo №1 Signature') is False:
        sys.exit(0)
else:
    print('NO NEW VERSION!')
    sys.exit(0)

# Generate download link
link = firmware_download_link.format(version_latest.split('.')[0], version_latest.split('.')[1], version_latest.split('.')[2])

# Download firmware from server
try:
    fw = urllib.request.urlopen(link)
    # trying to save fw file
    try:
        print('Downloading data...')
        data = fw.read()
        print('Saving FW to file...')
        config = open('sho-me-combo-N1-signature-firmware.zip', 'wb')
        config.write(data)
        config.close()
        print('FW saved to sho-me-combo-N1-signature-firmware.zip')
        messagebox.showinfo(message="Прошивка успешно сохранена", icon='info',
                            title='Обновление SHO-ME Combo №1 Signature')

        if messagebox.askyesno(message='Открыть папку с файлом прошивки (sho-me-combo-N1-signature-firmware.zip)?', icon='question',
                               title='Обновление SHO-ME Combo №1 Signature') is True:
            fw_path = os.getcwd() + '/sho-me-combo-N1-signature-firmware.zip'
            print(fw_path)
            subprocess.Popen(r'explorer /select, ' + fw_path)
    except:
        print('Could not write FW file!')
        messagebox.showinfo(message="Ошибка при сохранении прошивки!", icon='error',
                            title='Обновление SHO-ME Combo №1 Signature')
    # trying to save version to file
    try:
        config = open('version.txt', 'w')
        config.write(version_latest)
        config.close()
        print('Latest version saved')
    except:
        print('Could not open version file!')
        messagebox.showinfo(message="Ошибка при запоминании прошивки!", icon='error',
                            title='Обновление SHO-ME Combo №1 Signature')
except urllib.error.HTTPError:
    print('No FW found :(')
    messagebox.showinfo(message="Не удалось скачать прошивку!", icon='error',
                        title='Ошибка!')
    pass
