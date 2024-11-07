import mysql.connector

# Establish connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password"
)

cursor = db.cursor()

# Drop and recreate the database
cursor.execute("DROP DATABASE IF EXISTS se2")
cursor.execute("CREATE DATABASE se2")
cursor.execute("USE se2")

# Create management table
cursor.execute("""
        CREATE TABLE management(
            id INT AUTO_INCREMENT PRIMARY KEY, 
            name VARCHAR(25), 
            position VARCHAR(25)
            )
""")

# Create department table
cursor.execute("""
        CREATE TABLE department(
            id INT AUTO_INCREMENT PRIMARY KEY, 
            department ENUM('CSE','ECE','MECH','CIVIL','IT','EEE')
            )
""")

# Create mentor table
cursor.execute("""
    CREATE TABLE mentor(
        id INT AUTO_INCREMENT PRIMARY KEY, 
        name VARCHAR(25), 
        department_id INT, 
        highest_qualification ENUM('HS','UG','PG','PhD'), 
        FOREIGN KEY(department_id) REFERENCES department(id) ON DELETE CASCADE
    )
""")

# Create mentee table
cursor.execute("""
    CREATE TABLE mentee(
        id INT AUTO_INCREMENT PRIMARY KEY, 
        name VARCHAR(25), 
        GPA FLOAT, 
        mentor_id INT, 
        department_id INT, 
        FOREIGN KEY(department_id) REFERENCES department(id) ON DELETE CASCADE, 
        FOREIGN KEY(mentor_id) REFERENCES mentor(id) ON DELETE CASCADE
    )
""")

# Create allocation table
cursor.execute("""
    CREATE TABLE allocation(
        mngmt_id INT, 
        mentor_id INT, 
        mentee_id INT, 
        FOREIGN KEY(mngmt_id) REFERENCES management(id) ON DELETE CASCADE, 
        FOREIGN KEY(mentor_id) REFERENCES mentor(id) ON DELETE CASCADE, 
        FOREIGN KEY(mentee_id) REFERENCES mentee(id) ON DELETE CASCADE
    )
""")

# Create session table 
cursor.execute("""
    CREATE TABLE session(
        id INT AUTO_INCREMENT PRIMARY KEY, 
        mentor_id INT, 
        mentee_id INT, 
        time timestamp, 
        FOREIGN KEY(mentor_id) REFERENCES mentor(id) ON DELETE CASCADE, 
        FOREIGN KEY(mentee_id) REFERENCES mentee(id) ON DELETE CASCADE
    )
""")

# Create feedback table with id as PRIMARY KEY
cursor.execute("""
    CREATE TABLE feedback(
        id INT PRIMARY KEY, 
        mentor_feedback VARCHAR(40), 
        mentee_feedback VARCHAR(40), 
        FOREIGN KEY(id) REFERENCES session(id) ON DELETE CASCADE
    )
""")

# Insert initial values into management table
cursor.execute("INSERT INTO management(name, position) VALUES('Srihari Krishna', 'admin')")
cursor.execute("INSERT INTO management(name, position) VALUES('Shreyas Karthik', 'admin')")

# Insert initial values into department table
cursor.execute("INSERT INTO department(department) VALUES('CSE')")
cursor.execute("INSERT INTO department(department) VALUES('ECE')")
cursor.execute("INSERT INTO department(department) VALUES('MECH')")
cursor.execute("INSERT INTO department(department) VALUES('CIVIL')")
cursor.execute("INSERT INTO department(department) VALUES('IT')")
cursor.execute("INSERT INTO department(department) VALUES('EEE')")

# Create trigger to insert a row into feedback table when a new session is created
# Trigger for after session insert
cursor.execute("DROP TRIGGER IF EXISTS after_session_insert;")
cursor.execute("""
    CREATE TRIGGER after_session_insert
    AFTER INSERT ON session
    FOR EACH ROW
    BEGIN
        INSERT INTO feedback (ID, mentor_feedback, mentee_feedback) VALUES (NEW.ID, NULL, NULL);
    END;
""")

# Create procedure to add a new mentor
cursor.execute("DROP PROCEDURE IF EXISTS AddMentor;")  # Optional: Drops procedure if it exists
cursor.execute("""
    CREATE PROCEDURE AddMentor(IN name VARCHAR(255), IN highest_qualification VARCHAR(255), IN dept_id INT)
    BEGIN
        INSERT INTO mentor (Name, Highest_Qualification, department_id) VALUES (name, highest_qualification, dept_id);
    END;
""")

# Create function to calculate the average GPA of mentees for a given mentor
cursor.execute("DROP FUNCTION IF EXISTS AvgGPA;")
cursor.execute("""
    CREATE FUNCTION AvgGPA(mentor_id INT) RETURNS FLOAT
    READS SQL DATA
    BEGIN
        DECLARE avg_gpa FLOAT;
        SELECT AVG(GPA) INTO avg_gpa 
        FROM mentee 
        WHERE mentee.mentor_id = mentor_id;
        RETURN avg_gpa;
    END;
""")


# Commit the transaction
db.commit()

# Close the connection
cursor.close()
db.close()