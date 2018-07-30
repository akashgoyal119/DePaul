#!/usr/bin/env python3.5


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWizard
import sys
import subprocess
import time
import stat
import os
from pathlib import Path
import json 

def get_projects():
	home = str(Path.home()) #get home directory
	p = Path(home+'/sciunit/')
	proj_list = []
	for x in p.iterdir():
		if os.path.isdir(str(x)):
			proj = str(x).split('/')[-1] #get just the folder name, not full path
			proj_list.append(proj)
	return proj_list

class IntroductionPage(QtWidgets.QWizardPage):
	def __init__(self,*args,**kwargs):
		super().__init__()
		self.setTitle("Project Name")
		self.setSubTitle("Please select one of the available projects below")
		l = get_projects()

		comboBox = QtWidgets.QComboBox(self)
		[comboBox.addItem(i) for i in l]
		layout = QtWidgets.QGridLayout()
		layout.addWidget(comboBox)
		self.setLayout(layout)
		self.registerField("projectName",comboBox,"currentText")

	def nextId(self):
		subprocess.run(['sciunit','open',self.field("projectName")])
		return Real_Wizard.task 

class TaskPage(QtWidgets.QWizardPage):
	def __init__(self,*args,**kwargs):
		super().__init__()
		
	def initializePage(self):
		self.setTitle("Sciunit Function Type")
		self.setSubTitle("Please select the command you wish to run")
		self.radioList = QtWidgets.QRadioButton('List')
		self.radioExec = QtWidgets.QRadioButton('Exec')
		self.radioRepeat = QtWidgets.QRadioButton('Repeat')
		self.radioShow = QtWidgets.QRadioButton('Show')
		self.radioRm = QtWidgets.QRadioButton('Remove')
		self.layout = QtWidgets.QVBoxLayout()
		self.layout.addWidget(self.radioList)
		self.layout.addWidget(self.radioExec)
		self.layout.addWidget(self.radioRepeat)
		self.layout.addWidget(self.radioShow)
		self.layout.addWidget(self.radioRm)
		self.setLayout(self.layout)

	def nextId(self):
		if self.radioList.isChecked():
			self.registerField("list",self.radioList)
			return Real_Wizard.conclusion
		elif self.radioExec.isChecked():
			return Real_Wizard.exec_helper
		elif self.radioRepeat.isChecked():
			return Real_Wizard.repeat
		elif self.radioShow.isChecked():
			return Real_Wizard.show_page 
		elif self.radioRm.isChecked():
			return Real_Wizard.remove_page 
		else:
			return Real_Wizard.conclusion


class ExecuteHelperPage(QtWidgets.QWizardPage):
	def __init__(self,*args,**kwargs):
		super().__init__()
		
	def initializePage(self):
		self.setTitle("Type of File")
		self.setSubTitle("Do you wish to execute a regular script or a Jupyter Notebook Script")
		self.add_dropdown("type_of_execution",['Jupyter Notebook','Regular'])

	def add_dropdown(self,field_title,args):
		comboBox_jobs = QtWidgets.QComboBox(self)
		[comboBox_jobs.addItem(i) for i in args] 
		layout = QtWidgets.QVBoxLayout()
		layout.addWidget(comboBox_jobs)
		self.setLayout(layout)
		self.registerField(field_title,comboBox_jobs,"currentText")

	def nextId(self):
		return Real_Wizard.execute

class ExecutePage(QtWidgets.QWizardPage):
	def __init__(self,*args,**kwargs):
		super().__init__()

	def initializePage(self):
		self.setTitle("Choose file to execute")
		self.setSubTitle("Please choose a file to execute")
		self.uploader = QtWidgets.QPushButton("upload",self)
		self.uploader.clicked.connect(self.get_file_name)
		
		self.myTextBox = QtWidgets.QTextEdit(self)
		
		self.myTextBox.setReadOnly(True)
		self.layout = QtWidgets.QVBoxLayout()
		self.layout.addWidget(self.uploader)
		self.layout.addWidget(self.myTextBox)
		self.uploader.setGeometry(QtCore.QRect(20,40,151,81))
		self.myTextBox.setGeometry(QtCore.QRect(190, 40, 241, 81))
		self.setLayout(self.layout)
		
		if self.field("type_of_execution")=='Jupyter Notebook':
			self.line_number_text = QtWidgets.QLineEdit(
				"Enter the last execution number here",self)
			self.line_number_text.setGeometry(QtCore.QRect(10,240,321,81))
			self.layout.addWidget(self.line_number_text)
			self.registerField("last_number",self.line_number_text)
		
	# https://stackoverflow.com/questions/51273301/pyqt-trouble-passing-filenames-across-qwizardpage
	def get_file_name(self):
		name, _ = QtWidgets.QFileDialog.getOpenFileName(self.uploader,'Choose File to Run')
		self.wizard().file_name = name
		self.myTextBox.setText(name)

	def nextId(self):
		return Real_Wizard.conclusion

class RepeatPage(QtWidgets.QWizardPage):
	def __init__(self,*args,**kwargs):
		super().__init__()
		
	def initializePage(self):
		self.setTitle("Execution Number")
		self.setSubTitle("Please Choose the execution that you wish to run")
		result = subprocess.run(['sciunit','list'],stdout=subprocess.PIPE)
		cleaned_list = result.stdout.decode('utf-8').split('\n')
		del cleaned_list[-1] #get rid of white-space
		cleaned_list = [i.strip() for i in cleaned_list]
		self.add_dropdown("repeat_execution_number",cleaned_list)

	def add_dropdown(self,field_title,args):
		comboBox_jobs = QtWidgets.QComboBox(self)
		[comboBox_jobs.addItem(i) for i in args] 
		layout = QtWidgets.QVBoxLayout()
		layout.addWidget(comboBox_jobs)
		self.setLayout(layout)
		self.registerField(field_title,comboBox_jobs,"currentText")

	def nextId(self):
		return Real_Wizard.conclusion

class ShowPage(QtWidgets.QWizardPage):
	def __init__(self,*args,**kwargs):
		super().__init__()

	def initializePage(self):
		self.setTitle("Job Number")
		self.setSubTitle("Please choose the execution number whose details you wish to view")
		result = subprocess.run(['sciunit','list'],stdout=subprocess.PIPE)
		cleaned_list = result.stdout.decode('utf-8').split('\n')
		del cleaned_list[-1] #get rid of white-space
		cleaned_list = [i.strip() for i in cleaned_list]
		self.add_dropdown("show_job_number",cleaned_list)

	def add_dropdown(self,field_title,args):
		comboBox_jobs = QtWidgets.QComboBox(self)
		[comboBox_jobs.addItem(i) for i in args] 
		layout = QtWidgets.QVBoxLayout()
		layout.addWidget(comboBox_jobs)
		self.setLayout(layout)
		self.registerField(field_title,comboBox_jobs,"currentText")

	def nextId(self):
		return Real_Wizard.conclusion

class RemovePage(QtWidgets.QWizardPage):
	def __init__(self,*args,**kwargs):
		super().__init__()

	def initializePage(self):
		self.setTitle("Remove Number")
		self.setSubTitle("Please choose the execution number whose job you wish to remove")
		result = subprocess.run(['sciunit','list'],stdout=subprocess.PIPE)
		cleaned_list = result.stdout.decode('utf-8').split('\n')
		del cleaned_list[-1] #get rid of white-space
		cleaned_list = [i.strip() for i in cleaned_list]
		self.add_dropdown("remove_job_number",cleaned_list)

	def add_dropdown(self,field_title,args):
		comboBox_jobs = QtWidgets.QComboBox(self)
		[comboBox_jobs.addItem(i) for i in args] 
		layout = QtWidgets.QVBoxLayout()
		layout.addWidget(comboBox_jobs)
		self.setLayout(layout)
		self.registerField(field_title,comboBox_jobs,"currentText")

	def nextId(self):
		return Real_Wizard.conclusion

class ConclusionPage(QtWidgets.QWizardPage):
	def __init__(self,*args,**kwargs):
		super().__init__()
		self.setTitle("You have finished your task")

	def initializePage(self):
		# exec
		if hasattr(self.wizard(),'file_name'):
			file_name = self.wizard().file_name
			if self.field("type_of_execution")=='Regular':
				subprocess.run(['sciunit','exec',file_name])
			else:
				new_file_name = self.convert_jupyter_to_regular(file_name,
																int(self.field('last_number')))
				subprocess.run(['sciunit','exec',new_file_name])
		
		elif self.field("repeat_execution_number"):
			self.myTextBox = QtWidgets.QTextEdit(self)
			self.myTextBox.setReadOnly(True)
			job_number = self.field("repeat_execution_number").split(' ')[0]
			result = subprocess.run(['sciunit','repeat',job_number],stdout=subprocess.PIPE)
			cleaned_result = result.stdout.decode('utf-8')
			self.myTextBox.setText(cleaned_result)

		elif self.field("remove_job_number"):
			job = self.field("remove_job_number").split(' ')[0]
			subprocess.run(['sciunit','rm',job])
			self.setSubTitle("You have successfully removed task "+job)

		# list 
		elif self.field("list"):
			self.myTextBox = QtWidgets.QTextEdit(self)
			self.myTextBox.setReadOnly(True)
			self.myTextBox.setText(self.sciunit_list())
			self.layout = QtWidgets.QVBoxLayout()
			self.layout.addWidget(self.myTextBox)
			self.setLayout(self.layout)

		# show
		elif self.field("show_job_number"):
			self.myTextBox = QtWidgets.QTextEdit(self)
			self.myTextBox.setReadOnly(True)
			job_number = self.field("show_job_number").split(' ')[0]
			result = subprocess.run(['sciunit','show',job_number],stdout=subprocess.PIPE)
			cleaned_result = result.stdout.decode('utf-8')
			self.myTextBox.setText(cleaned_result)

		else:
			self.setSubTitle("Please go back and enter a file")
	
	def sciunit_list(self):
		result = subprocess.run(['sciunit','list'],stdout=subprocess.PIPE)
		cleaned_list = result.stdout.decode('utf-8')
		return cleaned_list

	def convert_jupyter_to_regular(self,file_name,last_input=100):
		if file_name[-6:]!= '.ipynb':
			print ('This only works for .ipynb files')
			sys.exit()

		with open(file_name,'r') as f:
			data = f.read()
			newData = json.loads(data)
			mapping = []
			for cell_number,item in enumerate(newData['cells']):
				# i.e. the user did not execute the code 
				if item['execution_count'] == None:
					continue
				elif item['execution_count'] > last_input:
					continue
				else:
					mapping.append((item['execution_count'],item['source']))


			mapping = sorted(mapping,key=lambda tup: tup[0])
			mapping = [i[1] for i in mapping]

			#change from .ipynb to .py
			new_jupyter_name = file_name[:-6]+'-from-Jupyter.py'
			with open (new_jupyter_name,'w') as f2:
				f2.write('#!/usr/bin/env python\n')
				for user_input in mapping:
					for line in user_input:
						# ignore bash lines 
						if line[0]=='!': 
							continue
						else:
							f2.write(line)
					f2.write('\n')
				os.chmod(new_jupyter_name,stat.S_IRWXU)
		return new_jupyter_name

class Real_Wizard(QtWidgets.QWizard):
	num_of_pages = 8
	(intro,task,repeat,show_page,remove_page,exec_helper,execute,conclusion) = range(num_of_pages)

	def __init__(self,*args,**kwargs):
		super(Real_Wizard,self).__init__(*args,**kwargs)
		self.setPage(self.intro,IntroductionPage(self))
		self.setPage(self.task,TaskPage(self))
		self.setPage(self.repeat,RepeatPage(self))
		self.setPage(self.show_page,ShowPage(self))
		self.setPage(self.remove_page,RemovePage(self))
		self.setPage(self.exec_helper,ExecuteHelperPage(self))
		self.setPage(self.execute,ExecutePage(self))
		self.setPage(self.conclusion, ConclusionPage(self))
		self.setStartId(self.intro)

def run():
	app = QtWidgets.QApplication(sys.argv)
	a = Real_Wizard()
	a.setWindowTitle("Sciunit GUI")
	a.show()
	sys.exit(app.exec_())

run()



#Steps to make this work (OLD--PLEASE IGNORE)
#1) in the terminal type "designer-qt4"
#2) open the relevant file and create the design for your GUI
#3) save it as WHATEVER.ui in the same folder as this file is located in
#4) type in the terminal "pyuic5 -x WHATEVER.ui -o pyqtdesigner.py"
#5) this module will inherit from that class, so just add the buttons to the
# "add_connectivity" function, and then create the relevant functions below
#6) Now you are finished 