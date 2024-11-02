import mysql.connector

# Establishing the database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="se2"
)

cursor = db.cursor()

def admin_menu():
    print("\nAdmin Menu")

    # print the management table
    cursor.execute("SELECT * FROM management")
    management = cursor.fetchall()
    for mngmt in management:
        print(mngmt)

    print("Enter your ID")
    mngmt_id = int(input())

    print("1) Add Mentor")
    print("2) Add Mentee")
    print("3) View Mentors")
    print("4) View Mentees")
    choice = int(input("Enter your choice: "))
    
    if choice == 1:
        add_mentor()
    elif choice == 2:
        add_mentee(mngmt_id)
    elif choice == 3:
        view_mentors()
    elif choice == 4:
        view_mentees()
    else:
        print("Invalid choice!")

def mentor_menu(mentor_id):
    print("\nMentor Menu")
    print("1) View Assigned Mentees")
    print("2) Schedule Session")
    print("3) Provide Feedback")
    choice = int(input("Enter your choice: "))
    
    if choice == 1:
        view_assigned_mentees(mentor_id)
    elif choice == 2:
        schedule_session(mentor_id)
    elif choice == 3:
        provide_feedback(mentor_id)
    else:
        print("Invalid choice!")

def mentee_menu(mentee_id):
    print("\nMentee Menu")
    print("1) View Scheduled Sessions")
    print("2) Provide Feedback")
    choice = int(input("Enter your choice: "))
    
    if choice == 1:
        view_scheduled_sessions(mentee_id)
    elif choice == 2:
        provide_feedback_as_mentee(mentee_id)
    else:
        print("Invalid choice!")

# Add Mentor
def add_mentor():
    name = input("Enter mentor name: ")
    highest_qual = input("Enter mentor highest qualification: (HS,UG,PG,PhD) ") 
    
    cursor.execute("SELECT * FROM department")
    departments = cursor.fetchall()
    for department in departments:
        print(f"{department[0]}: {department[1]}")

    dept_id = int(input("Enter department ID: "))
    cursor.execute(f"INSERT INTO mentor (name, highest_qualification, department_id) VALUES ('{name}', '{highest_qual}', {dept_id})")
    db.commit()
    print("Mentor added successfully!")

# Add Mentee
def add_mentee(mngmt_id):
    name = input("Enter mentee name: ")
    gpa = float(input("Enter GPA: "))
    
    cursor.execute("SELECT * FROM department")
    departments = cursor.fetchall()
    for department in departments:
        print(f"{department[0]}: {department[1]}")

    dept_id = int(input("Enter department ID: "))
    
    print("Allocating mentee to mentor\n\n")
    cursor.execute(f"select * from mentor")
    mentors = cursor.fetchall()
    for mentor in mentors:
        print(mentor)

    mentor_id = int(input("\nEnter mentor ID: "))
    cursor.execute(f"INSERT INTO mentee (name, GPA, department_id, mentor_id) VALUES ('{name}', {gpa}, {dept_id}, {mentor_id})")
    mentee_id = cursor.lastrowid
    cursor.execute(f"insert into allocation values({mngmt_id},{mentor_id},{mentee_id})")
    db.commit()
    print("Mentee added successfully!")

# View all mentors
def view_mentors():
    cursor.execute("SELECT * FROM mentor")
    mentors = cursor.fetchall()
    for mentor in mentors:
        print(f"{mentor[0]}: {mentor[1]} {mentor[2]} {mentor[3]}")

# View all mentees
def view_mentees():
    cursor.execute("SELECT * FROM mentee")
    mentees = cursor.fetchall()
    for mentee in mentees:
        print(f"{mentee[0]}: {mentee[1]}")

# View assigned mentees
def view_assigned_mentees(mentor_id):
    cursor.execute(f"SELECT * FROM mentee WHERE Mentor_ID = {mentor_id}")
    mentees = cursor.fetchall()
    for mentee in mentees:
        print(mentee)

# Schedule session
def schedule_session(mentor_id):
    cursor.execute(f"SELECT * FROM mentee WHERE Mentor_ID = {mentor_id}")
    mentees = cursor.fetchall()
    for mentee in mentees:
        print(mentee)
    
    mentee_id = int(input("Enter Mentee ID: "))
    session_time = input("Enter session time (YYYY-MM-DD HH:MM:SS): ")
    cursor.execute(f"INSERT INTO session (Time, Mentor_ID, Mentee_ID) VALUES ('{session_time}', {mentor_id}, {mentee_id})")
    cursor.execute(f"Insert into feedback values({cursor.lastrowid},NULL,NULL)")
    db.commit()
    print("Session scheduled successfully!")

# Provide feedback
def provide_feedback(mentor_id):

    cursor.execute(f"select * from session where Mentor_ID = {mentor_id}")
    sessions = cursor.fetchall()
    for session in sessions: 
        print(session)
    
    session_id = int(input("Enter Session ID: "))
    feedback = input("Enter feedback: ")
    cursor.execute(f"UPDATE feedback SET mentor_feedback = '{feedback}' WHERE ID = {session_id}")    
    db.commit()
    print("Feedback submitted successfully!")

# Mentee's view scheduled sessions
def view_scheduled_sessions(mentee_id):
    cursor.execute(f"SELECT time FROM session WHERE Mentee_ID = {mentee_id}")
    sessions = cursor.fetchall()
    for session in sessions:
        print(session)

# Mentee provide feedback
def provide_feedback_as_mentee(mentee_id):
    
    cursor.execute(f"SELECT * FROM session WHERE Mentee_ID = {mentee_id}")
    sessions = cursor.fetchall()
    for session in sessions:
        print(session)
    
    session_id = int(input("Enter Session ID: "))
    feedback = input("Enter feedback: ")
    
    cursor.execute(f"UPDATE feedback SET mentee_feedback = '{feedback}' WHERE ID = {session_id}")
    db.commit()
    print("Feedback submitted successfully!")

# Main logic
print("Welcome to the Mentor-Mentee System\n")
print("1) Admin Login")
print("2) Mentor Login")
print("3) Mentee Login\n")
choice = int(input("Enter your choice: "))

if choice == 1:
    admin_menu()

elif choice == 2:
    cursor.execute(f"SELECT * FROM mentor")
    mentors = cursor.fetchall()
    for mentor in mentors:
        print(mentor)

    mentor_id = int(input("Enter your Mentor ID: "))
    mentor_menu(mentor_id)

elif choice == 3:
    cursor.execute(f"SELECT * FROM mentee")
    mentees = cursor.fetchall()
    for mentee in mentees:
        print(mentee)
    mentee_id = int(input("Enter your Mentee ID: "))
    mentee_menu(mentee_id)

else:
    print("Invalid choice!")
