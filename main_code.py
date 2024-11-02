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
    
    if choice == 1: # add mentor
        name = input("Enter mentor name: ")
        highest_qual = input("Enter highest qualification: (HS,UG,PG,PhD) ")

        # For printing the department names. Remove them when implementing gui
        cursor.execute("SELECT * FROM department")
        departments = cursor.fetchall()
        for department in departments:
            print(f"{department[0]}: {department[1]}")

        dept_id = int(input("Enter department ID: "))

        add_mentor(name,highest_qual,dept_id)

    elif choice == 2: # add mentee
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
        add_mentee(mngmt_id, name, gpa, dept_id, mentor_id)

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

        cursor.execute(f"SELECT * FROM mentee WHERE Mentor_ID = {mentor_id}")
        mentees = cursor.fetchall()
        for mentee in mentees:
            print(mentee)
        
        mentee_id = int(input("Enter Mentee ID: "))
        session_time = input("Enter session time (YYYY-MM-DD HH:MM:SS): ")

        schedule_session(mentor_id, mentee_id, session_time)
    
    elif choice == 3:
        cursor.execute(f"""
            SELECT session.id, session.time, mentee.name
            FROM session
            JOIN mentee ON session.mentee_id = mentee.id
            WHERE session.mentor_id = {mentor_id}
        """)
        sessions = cursor.fetchall()
        for session in sessions: 
            print(session)
        
        session_id = int(input("Enter Session ID: "))
        feedback = input("Enter feedback: ")
        provide_feedback(mentor_id, session_id, feedback)
    
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

        cursor.execute(f"SELECT * FROM session WHERE Mentee_ID = {mentee_id}")
        sessions = cursor.fetchall()
        for session in sessions:
            print(session)
        
        session_id = int(input("Enter Session ID: "))
        feedback = input("Enter feedback: ")

        provide_feedback_as_mentee(mentee_id, session_id, feedback)
    else:
        print("Invalid choice!")

# Add Mentor
def add_mentor(name,highest_qual,dept_id):
    cursor.callproc('AddMentor', (name, highest_qual, dept_id))
    db.commit()
    print("Mentor added successfully!")

# Add Mentee
def add_mentee(mngmt_id, name, gpa, dept_id, mentor_id): 
    cursor.execute(f"INSERT INTO mentee (name, GPA, department_id, mentor_id) VALUES ('{name}', {gpa}, {dept_id}, {mentor_id})")
    mentee_id = cursor.lastrowid
    cursor.execute(f"insert into allocation values({mngmt_id},{mentor_id},{mentee_id})")
    db.commit()
    print("Mentee added successfully!")

# View all mentors
def view_mentors():
    cursor.execute("""
        SELECT mentor.id, mentor.name, mentor.highest_qualification, department.department, COUNT(session.id) AS session_count
        FROM mentor
        LEFT JOIN department ON mentor.department_id = department.id
        LEFT JOIN session ON mentor.id = session.mentor_id
        GROUP BY mentor.id, mentor.name, mentor.highest_qualification, department.department
    """)
    mentors = cursor.fetchall()
    for mentor in mentors:
        print(f"{mentor[0]}: {mentor[1]} {mentor[2]} {mentor[3]} Sessions: {mentor[4]}")

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
def schedule_session(mentor_id, mentee_id, session_time):
    
    cursor.execute(f"INSERT INTO session (Time, Mentor_ID, Mentee_ID) VALUES ('{session_time}', {mentor_id}, {mentee_id})")
    db.commit()
    print("Session scheduled successfully!")

# Provide feedback
def provide_feedback(mentor_id, session_id, feedback):
    
    cursor.execute(f"UPDATE feedback SET mentor_feedback = '{feedback}' WHERE ID = {session_id}")    
    db.commit()
    print("Feedback submitted successfully!")

# Mentee's view scheduled sessions
def view_scheduled_sessions(mentee_id):
    cursor.execute(f"""
        SELECT session.time, mentor.name
        FROM session
        JOIN mentor ON session.mentor_id = mentor.id
        WHERE session.mentee_id = {mentee_id}
    """)
    sessions = cursor.fetchall()
    for session in sessions:
        print(session)

# Mentee provide feedback
def provide_feedback_as_mentee(mentee_id, session_id, feedback):
    cursor.execute(f"UPDATE feedback SET mentee_feedback = '{feedback}' WHERE ID = {session_id}")
    db.commit()
    print("Feedback submitted successfully!")

# Nested query to get sessions for a mentor
def get_sessions_for_mentor(mentor_id):
    cursor.execute(f"""
        SELECT session.id, session.time, mentee.name
        FROM session
        WHERE session.mentor_id = {mentor_id}
        AND session.id IN (SELECT id FROM session WHERE mentor_id = {mentor_id})
    """)
    sessions = cursor.fetchall()
    for session in sessions:
        print(session)

# Aggregate query to get the average GPA of mentees for a mentor
def get_avg_gpa_for_mentor(mentor_id):
    cursor.execute(f"SELECT AvgGPA({mentor_id})")
    avg_gpa = cursor.fetchone()[0]
    print(f"Average GPA for mentor {mentor_id}: {avg_gpa}")

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