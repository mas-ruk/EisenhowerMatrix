## hessian matrix 
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QFont
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
        
        self.use_max_values = True

        ## tasks
        self.tasks = 0

        # setting main window title and shape
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.createTable()

        # Toggle between max and average for urgency and impact
        self.toggleMaxAvg = QCheckBox("Use Max for Urgency/Impact")
        self.toggleMaxAvg.setChecked(True)
        self.toggleMaxAvg.stateChanged.connect(self.updateUrgencyImpact)

        # add button to add tasks
        self.addButton = QPushButton("Add Issue")
        self.addButton.clicked.connect(self.addTask)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.layout.addWidget(self.toggleMaxAvg)
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
        addSubIssueButton.clicked.connect(lambda: self.addSubIssue(issueList, rowPos))

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

        self.resizeColsRows()

    def addSubIssue(self, issueList, rowPos):
        # Get the sub-task description
        subIssue, ok = QInputDialog.getText(self, "Add Sub-Issue", "Enter sub-issue:")

        if ok and subIssue:
            # Get the urgency rating (0-10)
            urgency, okUrgency = QInputDialog.getInt(self, "Add Urgency", "Enter urgency (0-10):", min=0, max=10)
            
            if okUrgency:
                # Get the impact rating (0-10)
                impact, okImpact = QInputDialog.getInt(self, "Add Impact", "Enter impact (0-10):", min=0, max=10)
                
                if okImpact:
                    # Combine the sub-issue with urgency and impact ratings
                    issueText = f"{subIssue} (Urgency: {urgency}, Impact: {impact})"
                    issueList.addItem(issueText)
                    
                    # Store urgency and impact as data for future calculations
                    issueList.item(issueList.count()-1).setData(Qt.ItemDataRole.UserRole, (urgency, impact))

                    # Update urgency and impact of the parent task based on toggle
                    self.updateUrgencyImpact()

                    # Resize rows and columns to fit new content
                    self.resizeColsRows()
            
    def resizeColsRows(self):
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def updateStatus(self, cb, row):
        if cb.isChecked():
            cb.setText("Closed")
            self.tableWidget.setItem(row, 3, QTableWidgetItem(self.today)) # sets date closed to N/a while not closed
        else:
            cb.setText("Open")
            self.tableWidget.setItem(row, 3, QTableWidgetItem("N/A")) 

    def updateUrgencyImpact(self):
        # Update the toggle value based on checkbox state
        self.use_max_values = self.toggleMaxAvg.isChecked()

        # Loop through all rows (tasks) and update their urgency and impact
        for row in range(self.tableWidget.rowCount()):
            # Get the issue widget for this row
            issueWidget = self.tableWidget.cellWidget(row, 1)
            if issueWidget:
                # Get the QListWidget containing the sub-issues
                issueList = issueWidget.layout().itemAt(0).widget()  # First widget in the layout
                urgencies = []
                impacts = []
                
                # Iterate over all items in the issueList (sub-issues)
                for i in range(issueList.count()):
                    urgency, impact = issueList.item(i).data(Qt.ItemDataRole.UserRole)
                    urgencies.append(urgency)
                    impacts.append(impact)
                
                # Determine urgency and impact based on max or average
                if self.use_max_values:
                    final_urgency = max(urgencies) if urgencies else 0
                    final_impact = max(impacts) if impacts else 0
                else:
                    final_urgency = sum(urgencies) // len(urgencies) if urgencies else 0
                    final_impact = sum(impacts) // len(impacts) if impacts else 0

                # Update the parent task's urgency and impact
                self.tableWidget.setItem(row, 5, QTableWidgetItem(str(final_urgency)))  # Update Urgency column
                self.tableWidget.setItem(row, 6, QTableWidgetItem(str(final_impact)))  # Update Impact column


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
