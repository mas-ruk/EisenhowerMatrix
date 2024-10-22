## hessian matrix 
import sys
from PyQt6.QtWidgets import *
from datetime import datetime

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Hessian Matrix'
        self.left = 0
        self.top = 0
        self.width = 1000
        self.height = 700

        self.today = datetime.today().strftime('%Y-%m-%d')
        
        ## tasks
        self.tasks = 0

        # setting main window title and shape
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.createTable()

        # add button to add tasks
        self.addButton = QPushButton("Add Issue")
        self.addButton.clicked.connect(self.addTask)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.layout.addWidget(self.addButton)
        self.setLayout(self.layout)

        # window shows
        self.show()

    def createTable(self):
        self.tableWidget = QTableWidget()
        
        ## status, date open closed, comments, id
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(("ID;Issue;Status (open/closed);Date Closed;Date Opened;Urgency (0 .. 10);Impact (0 .. 10);Comments").split(";"))
        
        # number of rows should be dependent on the no. of tasks
        self.tableWidget.setRowCount(self.tasks)

        ## should automatically resize 
        self.tableWidget.horizontalHeader().setStretchLastSection(True) 
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def addTask(self):
        # 
        rowPos = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPos)
        
        # ID can be set to row pos
        self.tableWidget.setItem(rowPos, 0, QTableWidgetItem(str(rowPos + 1)))

        issueList = QListWidget()

        addSubIssueButton = QPushButton("Add Sub-Issue")
        addSubIssueButton.clicked.connect(lambda: self.addSubIssue(issueList))

        issueLayout = QVBoxLayout()
        issueLayout.addWidget(issueList)
        issueLayout.addWidget(addSubIssueButton)

        issueWidget = QWidget()
        issueWidget.setLayout(issueLayout)
        self.tableWidget.setCellWidget(rowPos, 1, issueWidget)

        # checkbox init
        cb = QCheckBox()
        cb.setText("Open") # default
        cb.setChecked(False)
        cb.stateChanged.connect(lambda state, row = rowPos: self.updateStatus(cb, row))
        
        # unedited values
        self.tableWidget.setCellWidget(rowPos, 2, cb) # status
        self.tableWidget.setItem(rowPos, 3, QTableWidgetItem("N/A"))
        self.tableWidget.setItem(rowPos, 4, QTableWidgetItem(self.today))
        self.tableWidget.setItem(rowPos, 5, QTableWidgetItem("0"))
        self.tableWidget.setItem(rowPos, 6, QTableWidgetItem("0"))
        self.tableWidget.setItem(rowPos, 7, QTableWidgetItem(""))

        self.tableWidget.resizeRowsToContents()

    def addSubIssue(self, issueList):
        subIssue, ok = QInputDialog.getText(self, "Add Sub-Issue", "Enter sub-issue: ")

        if ok and subIssue:
            issueList.addItem(subIssue)

    def updateStatus(self, cb, row):
        if cb.isChecked():
            cb.setText("Closed")
            self.tableWidget.setItem(row, 3, QTableWidgetItem(self.today)) # sets date closed to N/a while not closed
        else:
            cb.setText("Open")
            self.tableWidget.setItem(row, 3, QTableWidgetItem("N/A")) 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
