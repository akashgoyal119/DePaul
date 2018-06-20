#Steps to make this work...
#1) in the terminal type "designer-qt4"
#2) open the relevant file and create the design for your GUI
#3) save it as WHATEVER.ui in the same folder as this file is located in
#4) type in the terminal "pyuic5 -x WHATEVER.ui -o pyqtdesigner.py"
#5) this module will inherit from that class, so just add the buttons to the
# "add_connectivity" function, and then create the relevant functions below
#6) Now you are finished 

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import subprocess
from pyqtdesigner import Ui_MainWindow
import time
import stat
import os
from pathlib import Path


class MyWizard(QtWidgets.QWizard):
	def __init__(self):
		super().__init__()
		self.start_wizard()
		self.show()

	#see github.com/baoboa/pyqt5/blob/master/examples/dialogs/trivialwizard
	def start_wizard(self):
		
		def command_type(self):
			page = QtWidgets.QWizardPage()
			page.setTitle("Sciunit Function Type")
			label = QtWidgets.QLabel("Select the type of function")
			label.setWordWrap(True)
			layout = QtWidgets.QVBoxLayout()
			layout.addWidget(label)
			page.setLayout(layout)
			return page

		def project_name(self):
			page = QtWidgets.QWizardPage()
			page.setTitle("Project")
			page.setSubTitle("Please select one of the available projects below")
			nameLabel = QtWidgets.QLabel("Name:")
			nameLineEdit = QtWidgets.QLineEdit()
			self.entered_name = nameLineEdit.text()
			emailLabel = QtWidgets.QLabel("Email Address: ")
			emailLineEdit = QtWidgets.QLineEdit()
			layout = QtWidgets.QGridLayout()
			layout.addWidget(nameLabel,0,0)
			layout.addWidget(nameLineEdit,0,1)
			layout.addWidget(emailLabel,1,0)
			layout.addWidget(emailLineEdit,1,1)
			page.setLayout(layout)
			return page

		def task_name(self):
			page = QtWidgets.QWizardPage()
			page.setTitle("Job number")
			label = QtWidgets.QLabel("You are now registered.")
			label.setWordWrap(True)
			layout = QtWidgets.QVBoxLayout()
			layout.addWidget(label)
			page.setLayout(layout)
			return page 

		#wizard = QtWidgets.QWizard()
		self.addPage(command_type(self))
		self.addPage(project_name(self))
		self.addPage(task_name(self))
		self.setWindowTitle("Sciunit helper")
		self.show()
		print (self.entered_name)

class Window (QtWidgets.QMainWindow,Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.add_connectivity()
		self.show()

	def add_connectivity(self):
		self.actionCreate.triggered.connect(self.create_project)

		# this part finds a list of all available projects to open
		home = str(Path.home()) #get home directory
		p = Path(home+'/sciunit/')
		for x in p.iterdir():
			if os.path.isdir(str(x)):
				proj = str(x).split('/')[-1] #get the folder name
				self.availableProjects.addItem(proj)

		self.openFile.triggered.connect(self.open_project)
		self.availableProjects.activated.connect(self.open_project)
		self.wizardBtn.clicked.connect(self.start_wizard)


	def create_project(self):
		name, okPressed = QtWidgets.QInputDialog.getText(self,"New Project",
														"Enter a project name: ",
														QtWidgets.QLineEdit.Normal,
														"")
		if okPressed and name:
			subprocess.run(['sciunit','create',name])


	def run_job(self):
		'''
			For a given open project, it will choose which job to run
			by calling "sciunit list" 

			The user should be given a combo-box with all options listed.
			From there, it will do something 
		'''

	def open_project(self):
		print (self.availableProjects.highlighted())

	def get_version(self):
		result = subprocess.run(['sciunit','--version'],stdout=subprocess.PIPE)
		#from there we need to decode it into a human-readable string
		print (result.stdout.decode('utf-8')[:-1])

def run():
	app = QtWidgets.QApplication(sys.argv)
	#GUI = Window()
	a = MyWizard()
	sys.exit(app.exec_())

run()
