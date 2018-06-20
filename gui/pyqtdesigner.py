# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sciunit_gui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(507, 487)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.createBtn = QtWidgets.QPushButton(self.centralwidget)
        self.createBtn.setGeometry(QtCore.QRect(30, 10, 181, 131))
        self.createBtn.setObjectName("createBtn")
        self.wizardBtn = QtWidgets.QPushButton(self.centralwidget)
        self.wizardBtn.setGeometry(QtCore.QRect(240, 10, 201, 131))
        self.wizardBtn.setObjectName("wizardBtn")
        self.availableProjects = QtWidgets.QComboBox(self.centralwidget)
        self.availableProjects.setGeometry(QtCore.QRect(30, 150, 181, 41))
        self.availableProjects.setObjectName("availableProjects")
        self.availableProjects.addItem("")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(30, 210, 451, 231))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 507, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionCreate = QtWidgets.QAction(MainWindow)
        self.actionCreate.setObjectName("actionCreate")
        self.openFile = QtWidgets.QAction(MainWindow)
        self.openFile.setObjectName("openFile")
        self.actionExecute = QtWidgets.QAction(MainWindow)
        self.actionExecute.setObjectName("actionExecute")
        self.menuFile.addAction(self.actionCreate)
        self.menuFile.addAction(self.openFile)
        self.menuFile.addAction(self.actionExecute)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.createBtn.setText(_translate("MainWindow", "Create Project"))
        self.wizardBtn.setText(_translate("MainWindow", "Start Wizard"))
        self.availableProjects.setItemText(0, _translate("MainWindow", "View All Projects"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionCreate.setText(_translate("MainWindow", "Create"))
        self.actionCreate.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.openFile.setText(_translate("MainWindow", "Open"))
        self.openFile.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionExecute.setText(_translate("MainWindow", "Execute"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

