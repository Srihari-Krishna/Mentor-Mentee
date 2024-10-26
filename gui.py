import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QInputDialog, QFormLayout, QLineEdit, QComboBox, QDialog, QDialogButtonBox

# Establishing the database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="se2"
)

cursor = db.cursor()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mentor-Mentee System')
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        # Create login buttons
        self.admin_btn = QPushButton('Admin Login')
        self.mentor_btn = QPushButton('Mentor Login')
        self.mentee_btn = QPushButton('Mentee Login')

        # Connect buttons to respective dashboards
        self.admin_btn.clicked.connect(self.prompt_admin_login)
        self.mentor_btn.clicked.connect(self.prompt_mentor_login)
        self.mentee_btn.clicked.connect(self.prompt_mentee_login)

        # Add buttons to the layout
        self.layout.addWidget(self.admin_btn)
        self.layout.addWidget(self.mentor_btn)
        self.layout.addWidget(self.mentee_btn)

        self.setLayout(self.layout)

    def prompt_admin_login(self):
        # Prompt the user for admin ID from the list
        cursor.execute("SELECT id, name FROM management")
        admins = cursor.fetchall()
        admin_ids = [str(admin[0]) + ": " + admin[1] for admin in admins]

        # Ask user to select the admin
        admin_id, ok = QInputDialog.getItem(self, "Admin Login", "Select Admin:", admin_ids, 0, False)

        if ok and admin_id:
            # Extract just the ID from the selection
            selected_admin_id = int(admin_id.split(":")[0])
            # Proceed to the admin dashboard
            self.show_admin_dashboard(selected_admin_id)

    def prompt_mentor_login(self):
        # Prompt the user for mentor ID from the list
        cursor.execute("SELECT id, name FROM mentor")
        mentors = cursor.fetchall()
        mentor_ids = [str(mentor[0]) + ": " + mentor[1] for mentor in mentors]

        # Ask user to select the mentor
        mentor_id, ok = QInputDialog.getItem(self, "Mentor Login", "Select Mentor:", mentor_ids, 0, False)

        if ok and mentor_id:
            selected_mentor_id = int(mentor_id.split(":")[0])
            # Proceed to the mentor dashboard
            self.show_mentor_dashboard(selected_mentor_id)

    def prompt_mentee_login(self):
        # Prompt the user for mentee ID from the list
        cursor.execute("SELECT id, name FROM mentee")
        mentees = cursor.fetchall()
        mentee_ids = [str(mentee[0]) + ": " + mentee[1] for mentee in mentees]

        # Ask user to select the mentee
        mentee_id, ok = QInputDialog.getItem(self, "Mentee Login", "Select Mentee:", mentee_ids, 0, False)

        if ok and mentee_id:
            selected_mentee_id = int(mentee_id.split(":")[0])
            # Proceed to the mentee dashboard
            self.show_mentee_dashboard(selected_mentee_id)

    def show_admin_dashboard(self, admin_id):
        self.hide()
        self.admin_dashboard = Dashboard('Admin', admin_id)
        self.admin_dashboard.show()

    def show_mentor_dashboard(self, mentor_id):
        self.hide()
        self.mentor_dashboard = Dashboard('Mentor', mentor_id)
        self.mentor_dashboard.show()

    def show_mentee_dashboard(self, mentee_id):
        self.hide()
        self.mentee_dashboard = Dashboard('Mentee', mentee_id)
        self.mentee_dashboard.show()

class Dashboard(QWidget):
    def __init__(self, user_type, user_id=None):
        super().__init__()
        self.setWindowTitle(f'{user_type} Dashboard')
        self.setGeometry(100, 100, 800, 600)

        self.user_type = user_type
        self.user_id = user_id

        # Main layout
        self.main_layout = QHBoxLayout()

        # Left panel for buttons
        self.button_layout = QVBoxLayout()

        # Create and add buttons based on user_type
        self.create_dashboard_buttons()

        # Right side layout for user details and output
        self.right_layout = QVBoxLayout()

        # User details
        self.user_details = QLabel(f'{user_type} ID: {self.user_id}')
        self.right_layout.addWidget(self.user_details)

        # Output area
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.right_layout.addWidget(self.output)

        # Combine the layouts
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addLayout(self.right_layout)

        self.setLayout(self.main_layout)

    def create_dashboard_buttons(self):
        if self.user_type == 'Admin':
            self.add_button('Add Mentor', self.show_add_mentor_form)
            self.add_button('Add Mentee', self.show_add_mentee_form)
            self.add_button('View Mentors', self.view_mentors)
            self.add_button('View Mentees', self.view_mentees)
        elif self.user_type == 'Mentor':
            self.add_button('View Assigned Mentees', self.view_assigned_mentees)
            self.add_button('Schedule Session', self.show_schedule_session_form)
            self.add_button('Provide Feedback', self.show_provide_feedback_form)
        elif self.user_type == 'Mentee':
            self.add_button('View Scheduled Sessions', self.view_scheduled_sessions)
            self.add_button('Provide Feedback', self.show_provide_feedback_as_mentee_form)

    def add_button(self, label, function):
        button = QPushButton(label)
        button.clicked.connect(function)
        self.button_layout.addWidget(button)

    def show_add_mentor_form(self):
        form = AddMentorForm()
        if form.exec_() == QDialog.Accepted:
            name, highest_qual, dept_id = form.get_data()
            cursor.execute("INSERT INTO mentor (name, highest_qualification, department_id) VALUES (%s, %s, %s)", (name, highest_qual, dept_id))
            db.commit()
            self.output.setText("Mentor added successfully!")

    def show_add_mentee_form(self):
        form = AddMenteeForm(self.user_id)
        if form.exec_() == QDialog.Accepted:
            name, gpa, dept_id, mentor_id = form.get_data()
            cursor.execute("INSERT INTO mentee (name, GPA, department_id, mentor_id) VALUES (%s, %s, %s, %s)", (name, gpa, dept_id, mentor_id))
            mentee_id = cursor.lastrowid
            cursor.execute("INSERT INTO allocation (mngmt_id, mentor_id, mentee_id) VALUES (%s, %s, %s)", (self.user_id, mentor_id, mentee_id))
            db.commit()
            self.output.setText("Mentee added successfully!")

    def show_schedule_session_form(self):
        form = ScheduleSessionForm(self.user_id)
        if form.exec_() == QDialog.Accepted:
            mentee_id, time = form.get_data()
            cursor.execute("INSERT INTO session (mentor_id, mentee_id, time) VALUES (%s, %s, %s)", (self.user_id, mentee_id, time))
            db.commit()
            self.output.setText("Session scheduled successfully!")

    def show_provide_feedback_form(self):
        form = ProvideFeedbackForm(self.user_id)
        if form.exec_() == QDialog.Accepted:
            session_id, feedback = form.get_data()
            cursor.execute("INSERT INTO feedback (id, mentor_feedback) VALUES (%s, %s) ON DUPLICATE KEY UPDATE mentor_feedback = %s", (session_id, feedback, feedback))
            db.commit()
            self.output.setText("Feedback provided successfully!")

    def show_provide_feedback_as_mentee_form(self):
        form = ProvideFeedbackAsMenteeForm(self.user_id)
        if form.exec_() == QDialog.Accepted:
            session_id, feedback = form.get_data()
            cursor.execute("INSERT INTO feedback (id, mentee_feedback) VALUES (%s, %s) ON DUPLICATE KEY UPDATE mentee_feedback = %s", (session_id, feedback, feedback))
            db.commit()
            self.output.setText("Feedback provided successfully!")

    def view_mentors(self):
        cursor.execute("SELECT * FROM mentor")
        mentors = cursor.fetchall()
        result = "\n".join([str(mentor) for mentor in mentors])
        self.output.setText(result)

    def view_mentees(self):
        cursor.execute("SELECT * FROM mentee")
        mentees = cursor.fetchall()
        result = "\n".join([str(mentee) for mentee in mentees])
        self.output.setText(result)

    def view_assigned_mentees(self):
        cursor.execute("SELECT * FROM mentee WHERE mentor_id = %s", (self.user_id,))
        mentees = cursor.fetchall()
        result = "\n".join([str(mentee) for mentee in mentees])
        self.output.setText(result)

    def view_scheduled_sessions(self):
        cursor.execute("SELECT time FROM session WHERE mentee_id = %s", (self.user_id,))
        sessions = cursor.fetchall()
        result = "\n".join([str(session) for session in sessions])
        self.output.setText(result)

class AddMentorForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Mentor')
        self.setGeometry(100, 100, 400, 300)

        self.layout = QFormLayout()

        self.name_input = QLineEdit()
        self.highest_qual_input = QComboBox()
        self.highest_qual_input.addItems(['HS', 'UG', 'PG', 'PhD'])

        cursor.execute("SELECT id, department FROM department")
        departments = cursor.fetchall()
        self.dept_input = QComboBox()
        for dept in departments:
            self.dept_input.addItem(dept[1], dept[0])

        self.layout.addRow('Name:', self.name_input)
        self.layout.addRow('Highest Qualification:', self.highest_qual_input)
        self.layout.addRow('Department:', self.dept_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def get_data(self):
        return self.name_input.text(), self.highest_qual_input.currentText(), self.dept_input.currentData()

class AddMenteeForm(QDialog):
    def __init__(self, mngmt_id):
        super().__init__()
        self.setWindowTitle('Add Mentee')
        self.setGeometry(100, 100, 400, 300)
        self.mngmt_id = mngmt_id

        self.layout = QFormLayout()

        self.name_input = QLineEdit()
        self.gpa_input = QLineEdit()

        cursor.execute("SELECT id, department FROM department")
        departments = cursor.fetchall()
        self.dept_input = QComboBox()
        for dept in departments:
            self.dept_input.addItem(dept[1], dept[0])

        cursor.execute("SELECT id, name FROM mentor")
        mentors = cursor.fetchall()
        self.mentor_input = QComboBox()
        for mentor in mentors:
            self.mentor_input.addItem(mentor[1], mentor[0])

        self.layout.addRow('Name:', self.name_input)
        self.layout.addRow('GPA:', self.gpa_input)
        self.layout.addRow('Department:', self.dept_input)
        self.layout.addRow('Mentor:', self.mentor_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def get_data(self):
        return self.name_input.text(), float(self.gpa_input.text()), self.dept_input.currentData(), self.mentor_input.currentData()

class ScheduleSessionForm(QDialog):
    def __init__(self, mentor_id):
        super().__init__()
        self.setWindowTitle('Schedule Session')
        self.setGeometry(100, 100, 400, 300)
        self.mentor_id = mentor_id

        self.layout = QFormLayout()

        cursor.execute("SELECT id, name FROM mentee WHERE mentor_id = %s", (self.mentor_id,))
        mentees = cursor.fetchall()
        self.mentee_input = QComboBox()
        for mentee in mentees:
            self.mentee_input.addItem(mentee[1], mentee[0])

        self.time_input = QLineEdit()

        self.layout.addRow('Mentee:', self.mentee_input)
        self.layout.addRow('Time:', self.time_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def get_data(self):
        return self.mentee_input.currentData(), self.time_input.text()

class ProvideFeedbackForm(QDialog):
    def __init__(self, mentor_id):
        super().__init__()
        self.setWindowTitle('Provide Feedback')
        self.setGeometry(100, 100, 400, 300)
        self.mentor_id = mentor_id

        self.layout = QFormLayout()

        cursor.execute("SELECT id, time FROM session WHERE mentor_id = %s", (self.mentor_id,))
        sessions = cursor.fetchall()
        self.session_input = QComboBox()
        for session in sessions:
            self.session_input.addItem(session[1], session[0])

        self.feedback_input = QLineEdit()

        self.layout.addRow('Session:', self.session_input)
        self.layout.addRow('Feedback:', self.feedback_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def get_data(self):
        return self.session_input.currentData(), self.feedback_input.text()

class ProvideFeedbackAsMenteeForm(QDialog):
    def __init__(self, mentee_id):
        super().__init__()
        self.setWindowTitle('Provide Feedback')
        self.setGeometry(100, 100, 400, 300)
        self.mentee_id = mentee_id

        self.layout = QFormLayout()

        cursor.execute("SELECT id, time FROM session WHERE mentee_id = %s", (self.mentee_id,))
        sessions = cursor.fetchall()
        self.session_input = QComboBox()
        for session in sessions:
            self.session_input.addItem(session[1], session[0])

        self.feedback_input = QLineEdit()

        self.layout.addRow('Session:', self.session_input)
        self.layout.addRow('Feedback:', self.feedback_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def get_data(self):
        return self.session_input.currentData(), self.feedback_input.text()

if __name__ == '__main__':
    app = QApplication.instance()  # Prevent multiple instances of QApplication
    if app is None:
        app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())