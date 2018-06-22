#Steps to make this work...
#1) in the terminal type "designer-qt4"
#2) open the relevant file and create the design for your GUI
#3) save it as WHATEVER.ui in the same folder as this file is located in
#4) type in the terminal "pyuic5 -x WHATEVER.ui -o pyqtdesigner.py"
#5) this module will inherit from that class, so just add the buttons to the
# "add_connectivity" function, and then create the relevant functions below
#6) Now you are finished 

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWizard
import sys
import subprocess
from pyqtdesigner import Ui_MainWindow
import time
import stat
import os
from pathlib import Path

#delete open later...
options = ['OPEN (or switch) project',
		   'EXEC- execute a specific file (not necessarily) in the project',
		   'REPEAT- re-run a specific job in the project',
		   'SHOW- show the displayed details of a specific execution',
		   'RM- delete a specific job',
		   'LIST- show all the jobs available']

class MyWizard(QtWidgets.QWizard):
	def __init__(self,mainW):
		super().__init__()
		self.mainW = mainW
		self.start_wizard()

	# This function is called every time the user hits "next"
	def initializePage(self,pageNumber):
		# as the API is quite confusing. If I can figure this out then change it back
		# for now this works although storing this list into memory is not great practice
		# however, without storing the dictionary, I just get an integer in return.

		if pageNumber == 1:
			self.project_selected = self.projects[self.page(pageNumber-1).field("projectName")]

		elif pageNumber == 2:
			self.option_selected = self.options[self.page(pageNumber-1).field("functionName")]
			subprocess.run(['sciunit','open',self.project_selected])

			#list 
			if self.option_selected == options[0]:	
				print ('you are done now')
			
			#exec
			elif self.option_selected == options[1]:
				self.page(pageNumber).setTitle("File Selection")
				self.page(pageNumber).setSubTitle("Choose an executable file")
				uploader = QtWidgets.QPushButton(self)
				name = QtWidgets.QFileDialog.getOpenFileName(uploader,'Choose File to Run')
				subprocess.run(['sciunit','exec',name[0]])

			#repeat, show, rm, list
			else:
				#first open the relevant project, then list all the process IDs
				result = subprocess.run(['sciunit','list'],stdout=subprocess.PIPE)
				cleaned_list = result.stdout.decode('utf-8').split('\n')
				del cleaned_list[-1] #get rid of white-space
				cleaned_list = [i.strip() for i in cleaned_list]

				#extract just the id number, not the details (i.e. just e1)
				self.process_numbers = [i.split(' ')[0] for i in cleaned_list]
				self.process_numbers_dict = {key:value for key,value in enumerate(self.process_numbers)}

				print (*cleaned_list,sep='\n')
				self.page(pageNumber).setTitle("Choose one of the options below")

				comboBox_jobs = QtWidgets.QComboBox(self)
				[comboBox_jobs.addItem(i) for i in cleaned_list] 
				layout = QtWidgets.QVBoxLayout()
				layout.addWidget(comboBox_jobs)
				self.page(pageNumber).setLayout(layout)
				self.page(pageNumber).registerField("job",comboBox_jobs)

		#repeat, rm, or show was selected
		elif pageNumber == 3:
			try:
				job_selected = self.process_numbers_dict[self.page(pageNumber-1).field("job")]
			#if you chose list or open then you can't choose a job, hence there will be attribute error
			except AttributeError as e:
				pass

			if self.option_selected == options[2]:
				subprocess.run(['sciunit','repeat',job_selected])

			elif self.option_selected == options[3]:
				subprocess.run(['sciunit','show',job_selected])

			elif self.option_selected == options[4]:
				subprocess.run(['sciunit','rm',job_selected])
				print ('You have deleted job '+str(job_selected))

	#see github.com/baoboa/pyqt5/blob/master/examples/dialogs/trivialwizard
	def start_wizard(self):
		
		def project_name():
			page = QtWidgets.QWizardPage()
			page.setTitle("Project Name")
			page.setSubTitle("Please select one of the available projects below")

			# get all the projects and then store index as key and the project name as the value
			l = get_projects()
			self.projects = {key:value for key,value in enumerate(l)} 

			comboBox = QtWidgets.QComboBox(self)
			[comboBox.addItem(i) for i in l]
			layout = QtWidgets.QGridLayout()
			layout.addWidget(comboBox)
			page.setLayout(layout)
			#register information
			page.registerField("projectName",comboBox)
			return page

		def command_type():
			page = QtWidgets.QWizardPage()
			page.setTitle("Sciunit Function Type")
			page.setSubTitle("Please select the command you wish to run")
			self.options = {key:value for key,value in enumerate(options)}
			#create drop down
			comboBox_func = QtWidgets.QComboBox(self)
			[comboBox_func.addItem(i) for i in options]
			#add objects to layout
			layout = QtWidgets.QVBoxLayout()
			layout.addWidget(comboBox_func)
			page.setLayout(layout)
			page.registerField('functionName',comboBox_func)
			return page

		def task_name():
			page = QtWidgets.QWizardPage()
			return page 

		def finish():
			page = QtWidgets.QWizardPage()
			page.setTitle("You have reached the end, click finish")
			return page

		self.addPage(project_name())
		self.addPage(command_type())
		self.addPage(task_name())
		self.addPage(finish())
		self.setWindowTitle("Sciunit helper")


#This is the main window that opens at the beginning
class Window (QtWidgets.QMainWindow,Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.add_connectivity()
		self.wiz = MyWizard(self)
		self.setWindowTitle("Sciunit helper")
		self.show()

	def add_connectivity(self):
		self.wizardBtn.clicked.connect(self.start_wizard)
		self.actionCreate.triggered.connect(self.create_project)
		self.createBtn.clicked.connect(self.create_project)

	def create_project(self):
		name, okPressed = QtWidgets.QInputDialog.getText(self,"New Project",
														"Enter a project name: ",
														QtWidgets.QLineEdit.Normal,
														"")
		if okPressed and name:
			old_result = subprocess.run(['sciunit','create',name],stdout=subprocess.PIPE)
			result = old_result.stdout.decode('utf-8')
			print (result)
			self.textEdit.setText(result)

	def start_wizard(self):
		self.wiz.show()

def get_projects():
	home = str(Path.home()) #get home directory
	p = Path(home+'/sciunit/')
	proj_list = []
	for x in p.iterdir():
		if os.path.isdir(str(x)):
			proj = str(x).split('/')[-1] #get just the folder name, not full path
			proj_list.append(proj)
	return proj_list

def run():
	app = QtWidgets.QApplication(sys.argv)
	GUI = Window()
	#a = MyWizard()
	sys.exit(app.exec_())

run()