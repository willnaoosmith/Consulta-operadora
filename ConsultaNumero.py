# coding: utf-8

import sys, os, time, datetime, ctypes
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QMessageBox, QPlainTextEdit
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from threading import Thread
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
import urllib.request
from ctypes import wintypes

lpBuffer = wintypes.LPWSTR()
AppUserModelID = ctypes.windll.shell32.GetCurrentProcessExplicitAppUserModelID
AppUserModelID(ctypes.cast(ctypes.byref(lpBuffer), wintypes.LPWSTR))
appid = lpBuffer.value
ctypes.windll.kernel32.LocalFree(lpBuffer)

if os.path.exists('C:/Program Files/ConsultaNumero/') == False:
   os.system('mkdir "C:/Program Files/ConsultaNumero/"')
   pass

if os.path.exists('C:/Program Files/ConsultaNumero/geckodriver.exe') == False:
   urllib.request.urlretrieve('https://github.com/willnaoosmit/GoogleAccountCreator/raw/master/geckodriver.exe', 'C:/Program Files/ConsultaNumero/geckodriver.exe')
   pass
   
if os.path.exists('C:/Program Files/ConsultaNumero/icone.ico') == False:
   urllib.request.urlretrieve('https://raw.githubusercontent.com/willnaoosmit/Consulta-operadora/master/CellTower.ico', 'C:/Program Files/ConsultaNumero/icone.ico')
   pass

def window():
   app = QApplication(sys.argv)
   global widget
   widget = QWidget()

   global MultiInput
   MultiInput = QPlainTextEdit(widget)
   MultiInput.move(10, 10)
   MultiInput.setFixedWidth(280)
   MultiInput.setFixedHeight(75)
   MultiInput.setPlaceholderText("Números") 

   global LogInput
   LogInput = QPlainTextEdit(widget)
   LogInput.move(10, 100)
   LogInput.setFixedWidth(280)
   LogInput.setFixedHeight(200)
   LogInput.setPlaceholderText("logs")
   LogInput.setReadOnly(True)

   global ExecutarButton
   ExecutarButton = QPushButton(widget)
   ExecutarButton.setText("Executar")
   ExecutarButton.move(10,310)
   ExecutarButton.setFixedWidth(280)
   ExecutarButton.clicked.connect(run_clicked)

   widget.setGeometry(50,50,300,350)
   widget.setWindowTitle("Consulta Número")
   widget.setFixedSize(300,350)
   widget.setWindowIcon(QtGui.QIcon('C:/Program Files/ConsultaNumero/icone.ico'))
   widget.show()
   sys.exit(app.exec_())

def run_clicked():

   lista = MultiInput.toPlainText()
   ValidCount = 0

   if len(lista.splitlines()) == 0:
      QMessageBox.about(widget, "Atenção", "Você precisa preencher todos os campos antes de executar!")
      return

   for line in lista.splitlines():

      if line.rstrip() and len(line) == 10:
         ValidCount += 1

   if ValidCount != len(lista.splitlines()):

      if len(lista.splitlines()) == 1:
         QMessageBox.about(widget, "Atenção", "Todos números não batem com os critérios de 10 caractéres por linha")

      elif abs(len(lista.splitlines()) - ValidCount) == 1:
         QMessageBox.about(widget, "Atenção", "Existe 1 dentre os " + str(len(lista.splitlines())) + " números que não bate com os critérios de 10 caractéres por linha")

      else: 
         QMessageBox.about(widget, "Atenção", "Existem " + str(abs(len(lista.splitlines()) - ValidCount)) + " dentre os " + str(len(lista.splitlines())) + " números que não batem com os critérios de 10 caractéres por linha")

      return

   ThreadRun = Thread(target=Run)
   ThreadRun.start()

def Run():

   LogInput.clear()
   lista = MultiInput.toPlainText()
   ExecutarButton.setEnabled(False)
   Progress = 0

   options = Options()
   options.headless = False
   browser = webdriver.Firefox(options=options, executable_path=r'C:/Program Files/ConsultaNumero/geckodriver.exe')

   browser.get('https://www.qualoperadora.net/')
   browser.maximize_window()

   for numero in lista.splitlines():
      try:
      	ExecutarButton.setText(str(Progress) + " de " + str(len(lista.splitlines())))
      	NumberInput = browser.find_element_by_name('telefone')
      	NumberInput.clear()
      	NumberInput.send_keys(numero)
      	time.sleep(2)
      	SearchButton = browser.find_element_by_id('consultar').click()
      	time.sleep(4)
      	Operadora = browser.find_element_by_class_name('dados').text
      	Estado = browser.find_element_by_class_name('cidade').text
      	LogInput.insertPlainText(" ".join(str(x) for x in Operadora.split('-')[:-1]) + ", " + str(Estado.split('-')[0]) + "\n")

      except Exception as error:
      	print(error)
      	LogInput.insertPlainText("Erro, " + str(numero) + "\n")

      Progress += 1
      continue

   ExecutarButton.setText("Executar")
   ExecutarButton.setEnabled(True)
   browser.close()

window()