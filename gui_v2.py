import sys
from PyQt5.QtWidgets import QFormLayout,QLineEdit,QComboBox,QApplication,QMainWindow,QWidget,QHBoxLayout,QVBoxLayout,QPushButton,QLabel,QTabWidget,QStackedLayout,QSizePolicy,QGridLayout,QTableWidget,QTableWidgetItem, QDesktopWidget
from PyQt5.QtGui import QPalette,QColor
from PyQt5.QtCore import QSize
import mysql.connector
from PyQt5.QtCore import Qt
db = mysql.connector.connect(
             host="localhost",
             user="root",
             password="password"
        )
        
cursor = db.cursor()
cursor.execute("USE se2")


class M_M(QWidget):
    def __init__(self, type):
        super().__init__()
        self.layout1 = QStackedLayout(self)  # Initialize the QStackedLayout

        if type == 'Mentor':
            layout = QVBoxLayout()
            self.widget_temp = QWidget()
            view_mentors = QPushButton('View Mentors')
            add_mentors = QPushButton('Add Mentors')
            layout.addWidget(view_mentors)
            layout.addWidget(add_mentors)
            self.widget_temp.setLayout(layout)
            self.layout1.addWidget(self.widget_temp)  # Add to the QStackedLayout

            view_mentors.clicked.connect(self.mentor_print)
            add_mentors.clicked.connect(self.mentor_add)

        if type == 'Mentee':
            layout = QVBoxLayout()
            view_mentees = QPushButton('View Mentee')
            add_mentees = QPushButton('Add Mentee')
            layout.addWidget(view_mentees)
            layout.addWidget(add_mentees)

            # Add the layout to a widget and then add it to QStackedLayout
            mentee_widget = QWidget()
            mentee_widget.setLayout(layout)
            self.layout1.addWidget(mentee_widget)

            view_mentees.clicked.connect(self.mentee_print)
            add_mentees.clicked.connect(self.mentee_add)

    def mentor_print(self):
        widget_temp = QWidget()
        layout = QGridLayout()
    
    # Create table
        table = QTableWidget()
        table.setColumnCount(3)  # Set number of columns
        table.setHorizontalHeaderLabels(['Name', 'Department_ID', 'Qualification'])  # Set headers
    
        data = []
        cursor.execute("SELECT * FROM mentor")
        mentors = cursor.fetchall()
        for mentor in mentors:
            data.append((str(mentor[1]), str(mentor[2]), str(mentor[3])))       
        #cursor.close()
        #db.close()
        print(data)
        # Set number of rows
        table.setRowCount(len(data))
    
        for row, (name, dept, qual) in enumerate(data):
            table.setItem(row, 0, QTableWidgetItem(name))
            table.setItem(row, 1, QTableWidgetItem(dept))
            table.setItem(row, 2, QTableWidgetItem(qual))
    
        # Resize columns to content
        table.resizeColumnsToContents()
    
        # Add table to layout
        layout.addWidget(table, 0, 0, 1, 4)  # Span across all 4 columns

        back_button = QPushButton('Back')
        back_button.setStyleSheet("""QPushButton{
        background-color: #000000;
        color: white;
        font-size: 26px;
        font-family: "Times New Roman", Times, serif;
        border-radius: 50px;
        border: 3px solid #D3D3D3;
        }
        QPushButton:hover {
        background-color: #45a049;
        }""")

        # Add back button at the bottom
        layout.addWidget(back_button, 1, 0)
        layout.addWidget(QWidget(), 1, 2)
        layout.addWidget(QWidget(), 1, 3)
    
        widget_temp.setLayout(layout)
        self.layout1.addWidget(widget_temp)
        self.layout1.setCurrentIndex(self.layout1.count() - 1)
        back_button.clicked.connect(self.go_back_mentor)

    def go_back_mentor(self):
        self.layout1.setCurrentIndex(0)  # Back to the first screen

    def mentor_add(self):
        add_widget = QWidget()
        layout = QVBoxLayout()

        # form_label = QLabel('Add Mentor Form')
        # layout.addWidget(form_label)

        # Create a form layout for Name, Department, and Qualification
        form_layout = QFormLayout()

        # Name Input
        self.name_input = QLineEdit()
        form_layout.addRow('Name:', self.name_input)

        # Department Dropdown
        self.department_input = QComboBox()
        self.department_input.addItems(['CSE', 'ECE', 'MECH', 'CIVIL', 'IT', 'EEE'])
        form_layout.addRow('Department:', self.department_input)

        # Qualification Dropdown
        self.qualification_input = QComboBox()
        self.qualification_input.addItems(['HS', 'UG', 'PG', 'PhD'])
        form_layout.addRow('Highest Qualification:', self.qualification_input)

        # Add form layout to the main layout
        layout.addLayout(form_layout)

        # Back button
        back_button = QPushButton('Back')
        back_button.setStyleSheet("""QPushButton{
            background-color: #000000;
            color: white;
            font-size: 26px;
            font-family: "Times New Roman", Times, serif;
            border-radius: 50px;
            border: 3px solid #D3D3D3;
        }
        QPushButton:hover {
            background-color: #45a049;
        }""")
        self.name_input.setStyleSheet("""
            QLineEdit {
                background-color: #000000;
                color: white;
                font-size: 26px;
                font-family: "Times New Roman", Times, serif;
                padding: 10px;
                border-radius: 10px;
                border: 3px solid #D3D3D3;
            }
            QLineEdit:hover {
                background-color: #45a049;
            }
        """)
        self.department_input.setStyleSheet("""
            QComboBox {
                background-color: #000000;
                color: white;
                font-size: 26px;
                font-family: "Times New Roman", Times, serif;
                padding: 10px;
                border-radius: 10px;
                border: 3px solid #D3D3D3;
            }
            QComboBox:hover {
                background-color: #45a049;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(/path/to/arrow.png); /* Optional: custom arrow */
            }
        """)
        self.qualification_input.setStyleSheet("""
            QComboBox {
                background-color: #000000;
                color: white;
                font-size: 26px;
                font-family: "Times New Roman", Times, serif;
                padding: 10px;
                border-radius: 10px;
                border: 3px solid #D3D3D3;
            }
            QComboBox:hover {
                background-color: #45a049;
            }
        """)
            
        
        # Save button
        save_button = QPushButton('Save')
        save_button.setStyleSheet("""QPushButton{
            background-color: #000000;
            color: white;
            font-size: 26px;
            font-family: "Times New Roman", Times, serif;
            border-radius: 50px;
            border: 3px solid #D3D3D3;
        }
        QPushButton:hover {
            background-color: #45a049;
        }""")

        # Add buttons to layout
        layout.addWidget(back_button)
        layout.addWidget(save_button)

        add_widget.setLayout(layout)

        self.layout1.addWidget(add_widget)
        self.layout1.setCurrentIndex(self.layout1.count() - 1)  # Show the new form widget
        
        # Connect buttons to actions
        back_button.clicked.connect(self.go_back_mentor)
        save_button.clicked.connect(self.save_mentor_info)

    def save_mentor_info(self):
        # Retrieve data from the form fields
        name = self.name_input.text()
        department = self.department_input.currentText()
        qualification = self.qualification_input.currentText()
        if department == 'CSE':
            department_id = 1
        elif department == 'ECE':
            department_id = 2
        elif department == 'MECH':
            department_id = 3
        elif department == 'CIVIL':
            department_id = 4
        elif department == 'IT':
            department_id = 5
        elif department == 'EEE':
            department_id = 6
        # Print values to verify (replace this with your database code to save the info)
        print(f"Name: {name}, Department: {department_id}, Qualification: {qualification}")
        cursor.callproc('AddMentor', (name, qualification, department_id))
        db.commit()
        print("Mentor added successfully!")
        # You can now use these variables to insert into the database or perform other actions

    # New methods for Mentee functionality
    def mentee_print(self):
        widget_temp = QWidget()
        layout = QGridLayout()
    
    # Create table
        table = QTableWidget()
        table.setColumnCount(4)  # Set number of columns
        table.setHorizontalHeaderLabels(['Name', 'GPA', 'Mentor', 'Department'])  # Set headers
    
        data = []
        cursor.execute("SELECT * FROM mentee")
        mentees = cursor.fetchall()
        for mentee in mentees:
            if(mentee[4] == 1):
                dept = 'CSE'
            elif(mentee[4] == 2):
                dept = 'ECE'
            elif(mentee[4] == 3):
                dept = 'MECH'
            elif(mentee[4] == 4):
                dept = 'CIVIL'
            elif(mentee[4] == 5):
                dept = 'IT'
            elif(mentee[4] == 6):
                dept = 'EEE'

            cursor.execute(f"select name from mentor where id = {mentee[3]}")
            mentor_name = cursor.fetchone()[0]

            data.append((str(mentee[1]), str(mentee[2]), str(mentor_name), dept))       
        #cursor.close()
        #db.close()
        #print(data)
        # Set number of rows
        table.setRowCount(len(data))
    
        for row, (name, gpa, ment, dept) in enumerate(data):
            table.setItem(row, 0, QTableWidgetItem(name))
            table.setItem(row, 1, QTableWidgetItem(gpa))
            table.setItem(row, 2, QTableWidgetItem(ment))
            table.setItem(row, 3, QTableWidgetItem(dept))
    
        # Resize columns to content
        table.resizeColumnsToContents()
    
        # Add table to layout
        layout.addWidget(table, 0, 0, 1, 4)  # Span across all 4 columns

        back_button = QPushButton('Back')
        back_button.setStyleSheet("""QPushButton{
        background-color: #000000;
        color: white;
        font-size: 26px;
        font-family: "Times New Roman", Times, serif;
        border-radius: 50px;
        border: 3px solid #D3D3D3;
        }
        QPushButton:hover {
        background-color: #45a049;
        }""")

        # Add back button at the bottom
        layout.addWidget(back_button, 1, 0)
        layout.addWidget(QWidget(), 1, 2)
        layout.addWidget(QWidget(), 1, 3)
    
        widget_temp.setLayout(layout)
        self.layout1.addWidget(widget_temp)
        self.layout1.setCurrentIndex(self.layout1.count() - 1)
        back_button.clicked.connect(self.go_back_mentee)

    def go_back_mentee(self):
        self.layout1.setCurrentIndex(0)  # Back to the first screen

    def mentee_add(self):
        add_widget = QWidget()
        layout = QVBoxLayout()

        # form_label = QLabel('Add Mentor Form')
        # layout.addWidget(form_label)

        # Create a form layout for Name, Department, and Qualification
        form_layout = QFormLayout()

        # Name Input
        self.name_input = QLineEdit()
        form_layout.addRow('Name:', self.name_input)

        self.gpa_input = QLineEdit()
        form_layout.addRow('GPA:', self.gpa_input)

        # Department Dropdown
        self.department_input = QComboBox()
        self.department_input.addItems(['CSE', 'ECE', 'MECH', 'CIVIL', 'IT', 'EEE'])
        form_layout.addRow('Department:', self.department_input)

        # Qualification Dropdown
        # self.qualification_input = QComboBox()
        # self.qualification_input.addItems(['HS', 'UG', 'PG', 'PhD'])
        # form_layout.addRow('Highest Qualification:', self.qualification_input)

        mentor_names = []
        cursor.execute(f"select * from mentor")
        mentors = cursor.fetchall()
        for mentor in mentors:
            mentor_names.append(mentor[1])

        self.mentor_input = QComboBox()
        self.mentor_input.addItems(mentor_names)
        form_layout.addRow('Mentor', self.mentor_input)

        # Add form layout to the main layout
        layout.addLayout(form_layout)

        # Back button
        back_button = QPushButton('Back')
        back_button.setStyleSheet("""QPushButton{
            background-color: #000000;
            color: white;
            font-size: 26px;
            font-family: "Times New Roman", Times, serif;
            border-radius: 50px;
            border: 3px solid #D3D3D3;
        }
        QPushButton:hover {
            background-color: #45a049;
        }""")
        self.name_input.setStyleSheet("""
            QLineEdit {
                background-color: #000000;
                color: white;
                font-size: 26px;
                font-family: "Times New Roman", Times, serif;
                padding: 10px;
                border-radius: 10px;
                border: 3px solid #D3D3D3;
            }
            QLineEdit:hover {
                background-color: #45a049;
            }
        """)
        self.gpa_input.setStyleSheet("""
            QLineEdit {
                background-color: #000000;
                color: white;
                font-size: 26px;
                font-family: "Times New Roman", Times, serif;
                padding: 10px;
                border-radius: 10px;
                border: 3px solid #D3D3D3;
            }
            QLineEdit:hover {
                background-color: #45a049;
            }
        """)
        self.department_input.setStyleSheet("""
            QComboBox {
                background-color: #000000;
                color: white;
                font-size: 26px;
                font-family: "Times New Roman", Times, serif;
                padding: 10px;
                border-radius: 10px;
                border: 3px solid #D3D3D3;
            }
            QComboBox:hover {
                background-color: #45a049;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(/path/to/arrow.png); /* Optional: custom arrow */
            }
        """)
        self.mentor_input.setStyleSheet("""
            QComboBox {
                background-color: #000000;
                color: white;
                font-size: 26px;
                font-family: "Times New Roman", Times, serif;
                padding: 10px;
                border-radius: 10px;
                border: 3px solid #D3D3D3;
            }
            QComboBox:hover {
                background-color: #45a049;
            }
        """)
            
        
        # Save button
        save_button = QPushButton('Save')
        save_button.setStyleSheet("""QPushButton{
            background-color: #000000;
            color: white;
            font-size: 26px;
            font-family: "Times New Roman", Times, serif;
            border-radius: 50px;
            border: 3px solid #D3D3D3;
        }
        QPushButton:hover {
            background-color: #45a049;
        }""")

        # Add buttons to layout
        layout.addWidget(back_button)
        layout.addWidget(save_button)

        add_widget.setLayout(layout)

        self.layout1.addWidget(add_widget)
        self.layout1.setCurrentIndex(self.layout1.count() - 1)  # Show the new form widget
        
        # Connect buttons to actions
        back_button.clicked.connect(self.go_back_mentor)
        save_button.clicked.connect(self.save_mentee_info)

    def save_mentee_info(self):
        # Retrieve data from the form fields
        name = self.name_input.text()
        gpa = self.gpa_input.text()
        department = self.department_input.currentText()
        if department == 'CSE':
            department_id = 1
        elif department == 'ECE':
            department_id = 2
        elif department == 'MECH':
            department_id = 3
        elif department == 'CIVIL':
            department_id = 4
        elif department == 'IT':
            department_id = 5
        elif department == 'EEE':
            department_id = 6
        # Print values to verify (replace this with your database code to save the info)
        mentor_name = self.mentor_input.currentText()
        cursor.execute(f"select id from mentor where name = '{mentor_name}'")
        mentor_id = cursor.fetchone()[0]
        cursor.execute(f"INSERT INTO mentee (name, GPA, department_id, mentor_id) VALUES ('{name}', {float(gpa)}, {department_id}, {mentor_id})")
        mentee_id = cursor.lastrowid
        cursor.execute(f"insert into allocation values(1,{mentor_id},{mentee_id})")
        db.commit()
        print("Mentee added successfully!")

class Mentor(QWidget):
    def __init__(self,type):
        super().__init__()
        self.layout1 = QStackedLayout(self)  # Initialize the QStackedLayout

        if type == 'Sessions':
            layout = QVBoxLayout()
            self.widget_temp = QWidget()
            view_ssn = QPushButton('View Sessions')
            add_ssn = QPushButton('Add sessions')
            layout.addWidget(view_ssn)
            layout.addWidget(add_ssn)
            self.widget_temp.setLayout(layout)
            self.layout1.addWidget(self.widget_temp)  # Add to the QStackedLayout

            view_ssn.clicked.connect(self.ssn_print)
            add_ssn.clicked.connect(self.session_add)

        if type == 'Feedback':
            layout = QVBoxLayout()
            view_feedback = QPushButton('View Feedback')
            add_feedback = QPushButton('Add Feedback')
            layout.addWidget(view_feedback)
            layout.addWidget(add_feedback)

            # Add the layout to a widget and then add it to QStackedLayout
            mentee_widget = QWidget()
            mentee_widget.setLayout(layout)
            self.layout1.addWidget(mentee_widget)

            view_feedback.clicked.connect(self.feedback_print)
            add_feedback.clicked.connect(self.feedback_add)

    def ssn_print(self):
        widget_temp = QWidget()
        layout = QGridLayout()
        printer = QLabel('session list')
        layout.addWidget(printer, 0, 1)

        back_button = QPushButton('Back')
        back_button.setStyleSheet("""QPushButton{
            background-color: #000000;
            color: white;
            font-size: 26px;
            font-family: "Times New Roman", Times, serif;
            border-radius: 50px;
            border: 3px solid #D3D3D3;
        }
        QPushButton:hover {
            background-color: #45a049;
        }""")

        layout.addWidget(back_button, 1, 0)
        layout.addWidget(QWidget(), 1, 2)
        layout.addWidget(QWidget(), 1, 3)
        widget_temp.setLayout(layout)

        self.layout1.addWidget(widget_temp)
        self.layout1.setCurrentIndex(self.layout1.count() - 1)  # Show new widget
        back_button.clicked.connect(self.go_back_mentor)

    def go_back_mentor(self):
        self.layout1.setCurrentIndex(0)  # Back to the first screen

    def session_add(self):
        add_widget = QWidget()
        layout = QVBoxLayout()
        form_label = QLabel('Form to Add sessions')
        layout.addWidget(form_label)

        back_button = QPushButton('Back')
        back_button.setStyleSheet("""QPushButton{
            background-color: #000000;
            color: white;
            font-size: 26px;
            font-family: "Times New Roman", Times, serif;
            border-radius: 50px;
            border: 3px solid #D3D3D3;
        }
        QPushButton:hover {
            background-color: #45a049;
        }""")

        layout.addWidget(back_button)
        add_widget.setLayout(layout)

        self.layout1.addWidget(add_widget)
        self.layout1.setCurrentIndex(self.layout1.count() - 1)  # Show the new form widget
        back_button.clicked.connect(self.go_back_mentor)

    # New methods for Mentee functionality
    def feedback_print(self):
        widget_temp = QWidget()
        layout = QGridLayout()
        printer = QLabel('feedback List')
        layout.addWidget(printer, 0, 1)

        back_button = QPushButton('Back')
        back_button.setStyleSheet("""QPushButton{
            background-color: #000000;
            color: white;
            font-size: 26px;
            font-family: "Times New Roman", Times, serif;
            border-radius: 50px;
            border: 3px solid #D3D3D3;
        }
        QPushButton:hover {
            background-color: #45a049;
        }""")

        layout.addWidget(back_button, 1, 0)
        layout.addWidget(QWidget(), 1, 2)
        layout.addWidget(QWidget(), 1, 3)
        widget_temp.setLayout(layout)

        self.layout1.addWidget(widget_temp)
        self.layout1.setCurrentIndex(self.layout1.count() - 1)  # Show new widget
        back_button.clicked.connect(self.go_back_mentee)

    def go_back_mentee(self):
        self.layout1.setCurrentIndex(0)  # Back to the first screen

    def feedback_add(self):
        add_widget = QWidget()
        layout = QVBoxLayout()
        form_label = QLabel('Form to Add feedback')
        layout.addWidget(form_label)

        back_button = QPushButton('Back')
        back_button.setStyleSheet("""QPushButton{
            background-color: #000000;
            color: white;
            font-size: 26px;
            font-family: "Times New Roman", Times, serif;
            border-radius: 50px;
            border: 3px solid #D3D3D3;
        }
        QPushButton:hover {
            background-color: #45a049;
        }""")

        layout.addWidget(back_button)
        add_widget.setLayout(layout)

        self.layout1.addWidget(add_widget)
        self.layout1.setCurrentIndex(self.layout1.count() - 1)  # Show the new form widget
        back_button.clicked.connect(self.go_back_mentee)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mentor Mentee System')
        self.setGeometry(800,800,800,800)
        self.center()
        layout1=QVBoxLayout()
        layout2=QVBoxLayout()
        
        admin_button=QPushButton('Admin')
        admin_button.clicked.connect(self.admin_login_1)
        layout2.addWidget(admin_button)
        mentor_button=QPushButton('Mentor')
        layout2.addWidget(mentor_button)
        mentor_button.clicked.connect(self.Mentor_login)

        layout2.addWidget(QPushButton('Mentee'))
        layout2.setSpacing(20) 
        image=QLabel('bg')     
        image.setFixedSize(10, 10)
        layout1.addWidget(image)
        layout1.addLayout(layout2)


        widget = QWidget()
        # widget.setGeometry(500, 500, 500, 500)
        
        widget.setLayout(layout1)
        self.setCentralWidget(widget)
    # def login_page(self,type):   #func for login page
    #     if self.centralWidget() is not None:
    #         self.centralWidget().deleteLater()
    def center(self):
        # Get the screen geometry
        screen_geometry = QDesktopWidget().availableGeometry()
        # Get the geometry of the main window
        window_geometry = self.frameGeometry()
        # Calculate the center point
        center_point = screen_geometry.center()
        # Move the window's center to the screen's center
        window_geometry.moveCenter(center_point)
        # Move the top-left point of the window to the top-left point of the frame geometry
        self.move(window_geometry.topLeft())

    def admin_login_1(self):
        layout2=QVBoxLayout()
        
        new_container = QWidget(self)
        layout = QFormLayout()
        layout.setSpacing(0)  # Remove spacing between rows
        layout.setContentsMargins(20, 20, 20, 20)

    # Create widgets
        username_label = QLabel('Username:')
        self.admin_input = QLineEdit()
    
        password_label = QLabel('Password:')
        self.admin_password = QLineEdit()
        self.admin_password.setEchoMode(QLineEdit.Password)
    
        submit_button = QPushButton('Login')
        submit_button.clicked.connect(self.admin_login_2)

    # Add to form layout
        layout.addRow(username_label, self.admin_input)
        layout.addRow(password_label, self.admin_password)
        layout.addRow('', submit_button)  # Empty label for button row
    
    # Label style
        label_style = '''
        QLabel {
            color: #333333;
            font-size: 23px;
            font-family: "Times New Roman", Times, serif;
            
        }
        '''
    
    # Input style
        input_style = '''
        QLineEdit {
            background-color: #000000;
            color: white;
            font-size: 26px;
            font-family: "Times New Roman", Times, serif;
            padding: 10px;
            border-radius: 10px;
            border: 3px solid #D3D3D3;
            margin: 0px;
        }
        QLineEdit:hover {
            background-color: #45a049;
            border-color: #357a38;
        }
        QLineEdit:focus {
            border-color: #2196F3;
        }
        '''
    
    # Button style
        button_style = '''
        QPushButton {
            background-color: #000000;
            color: white;
            font-size: 23px;
            font-family: "Times New Roman", Times, serif;
            padding: 10px 20px;
            border-radius: 10px;
            border: none;
            min-height: 45px;
            margin-top: 10px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #357a38;
        }
        '''

    # Apply styles
        username_label.setStyleSheet(label_style)
        password_label.setStyleSheet(label_style)
        self.admin_input.setStyleSheet(input_style)
        self.admin_password.setStyleSheet(input_style)
        submit_button.setStyleSheet(button_style)

    # Set form layout properties to minimize spacing
        layout.setLabelAlignment(Qt.AlignLeft)
        layout.setFormAlignment(Qt.AlignLeft)
        layout.setHorizontalSpacing(10)  # Space between label and field
        layout.setVerticalSpacing(0)     # Space between rows

        layout2.addWidget(QWidget())
        layout2.addLayout(layout)
        layout2.addWidget(QWidget())
        new_container.setLayout(layout2)
        self.setCentralWidget(new_container)
    def admin_login_2(self):
        # Remove and delete all widgets from the central widget or layout
        # if self.centralWidget() is not None:
        #     self.centralWidget().deleteLater()  # Deletes current central widget

        # Set the new layout with the new widgets
        new_container = QWidget(self) 
        layout=QVBoxLayout(new_container)
        tabs=QTabWidget(new_container)
        tabs.setStyleSheet("""
            QTabWidget::pane { /* The tab widget frame */
                border: 2px solid #C2C7CB;
                background: #f8f8f8;
            }
            QTabBar::tab {
                background: #E0E0E0; /* Normal tab background */
                color: black;        /* Text color */
                padding: 20px;       /* Increase space around the text */
                font-size: 26px;           /* Font size */
                font-family: "Times New Roman", Times, serif;
                min-height: 40px;    /* Minimum height of the tab */
                min-height:300px;
                border: 1px solid #C2C7CB;
                border-bottom-color: #f8f8f8; /* Same as pane color */
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected { /* When the tab is selected */
                background: #D1D1D1;  /* Selected tab background */
                color: #333;          /* Selected tab text color */
                font-weight: bold;
            }
            QTabBar::tab:hover { /* When hovering over the tab */
                background: #CCCCCC;
            }
        """)
        tabs.setTabPosition(QTabWidget.West)
        tabs.setMovable(True)

        
        tabs.addTab(M_M('Mentor'),'Mentor')
        tabs.addTab(M_M('Mentee'),'Mentee')
        layout.addWidget(tabs)
        new_container.setLayout(layout)
        self.setCentralWidget(new_container)

    def Mentor_login(self):
        # Remove and delete all widgets from the central widget or layout
        # if self.centralWidget() is not None:
        #     self.centralWidget().deleteLater()  # Deletes current central widget

        # Set the new layout with the new widgets
        new_container = QWidget(self) 
        layout=QVBoxLayout(new_container)
        tabs=QTabWidget(new_container)
        tabs.setStyleSheet("""
            QTabWidget::pane { /* The tab widget frame */
                border: 2px solid #C2C7CB;
                background: #f8f8f8;
            }
            QTabBar::tab {
                background: #E0E0E0; /* Normal tab background */
                color: black;        /* Text color */
                padding: 20px;       /* Increase space around the text */
                font-size: 26px;           /* Font size */
                font-family: "Times New Roman", Times, serif;
                min-height: 40px;    /* Minimum height of the tab */
                min-height:300px;
                border: 1px solid #C2C7CB;
                border-bottom-color: #f8f8f8; /* Same as pane color */
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected { /* When the tab is selected */
                background: #D1D1D1;  /* Selected tab background */
                color: #333;          /* Selected tab text color */
                font-weight: bold;
            }
            QTabBar::tab:hover { /* When hovering over the tab */
                background: #CCCCCC;
            }
        """)
        tabs.setTabPosition(QTabWidget.West)
        tabs.setMovable(True)

        
        tabs.addTab(Mentor('Sessions'),'Sessions')
        tabs.addTab(Mentor('Feedback'),'Feedback')
        layout.addWidget(tabs)
        new_container.setLayout(layout)
        self.setCentralWidget(new_container)
    
        
        

app=QApplication([])
app.setStyleSheet("""
    QMainWindow{
           background-color: #D3D3D3;
                 
    }
    QPushButton {
        background-color: #000000; /* Green background */
        color: white;              /* White text */
        font-size: 26px;           /* Font size */
        font-family: "Times New Roman", Times, serif;
        border-radius: 50px;       /* Rounded corners */
        padding: 40px 20px;        /* Padding */
        border: 3px solid #D3D3D3;
        
        
    }
    QPushButton:hover {
        background-color: #45a049; /* Darker green on hover */
    }
    QPushButton:pressed {
        background-color: #3e8e41; /* Even darker green when pressed */
    }
""")
window=MainWindow()
window.show()

app.exec()