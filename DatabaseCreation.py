import sqlite3
import pandas as pd
import bcrypt

def connect():
    conn = sqlite3.connect("project.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Project")
    cur.execute("DROP TABLE IF EXISTS Tasks")
    cur.execute("DROP TABLE IF EXISTS ProjectMembers")
    cur.execute("DROP TABLE IF EXISTS Login")
    cur.execute("DROP TABLE IF EXISTS ProjectMessages")
    cur.execute("DROP TABLE IF EXISTS TaskMessages")

    # create projects table
    cur.execute("CREATE TABLE IF NOT EXISTS Project("
                "PROJECT_ID INTEGER PRIMARY KEY AUTOINCREMENT, "
                "PROJECT_NAME TEXT UNIQUE, "
                "START_DATE DATETIME, "
                "END_DATE DATETIME, "
                "STATUS TEXT, "
                "DESCRIPTION TEXT, "
                "PERCENTAGE_COMPLETE INTEGER, "
                "OWNER TEXT)")

    cur.execute("INSERT INTO Project ("
                "PROJECT_NAME, "
                "STATUS,"
                "DESCRIPTION,"
                "PERCENTAGE_COMPLETE, "
                "OWNER) "
                "VALUES ('myProject' ,'In-Progress', 'Building a fishing boat', 28, 'Karl Gospel')")

    print (pd.read_sql("SELECT * FROM Project", conn))

    # create Tasks table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Tasks("
        "TASK_ID INTEGER PRIMARY KEY AUTOINCREMENT, "
        "TASK_NAME TEXT, "
        "PROJECT_ID INTEGER NOT NULL, "
        "DESCRIPTION TEXT, "
        "STATUS TEXT, "
        "PERCENTAGE_COMPLETE INTEGER, "
        "ASSIGNED_TO TEXT,"
        "START_DATE DATETIME,"
        "END_DATE DATETIME, "
        "COMMENT TEXT, "
        "CONSTRAINT FK_PROJECT FOREIGN KEY (PROJECT_ID) REFERENCES Project(PROJECT_ID) ON DELETE CASCADE"
        ")")

    cur.execute("INSERT INTO Tasks ("
                "TASK_NAME, "
                "PROJECT_ID,"
                "DESCRIPTION, "
                "STATUS,"
                "PERCENTAGE_COMPLETE, "
                "ASSIGNED_TO) VALUES ('Build Something please', 1, 'make something' ,'Completed', 28, 'Karl Gospel')")
    print(pd.read_sql("SELECT * FROM Tasks", conn))

    # create Login table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Login("
        "USER_ID INTEGER PRIMARY KEY AUTOINCREMENT, "
        "USERNAME TEXT UNIQUE, "
        "PASSWORD TEXT,"
        "EMAIL TEXT,"
        "ADMIN BOOLEAN NOT NULL "
        ")")
    cur.execute("INSERT INTO Login (USERNAME, PASSWORD, ADMIN,EMAIL) VALUES ('Karl Gospel', 'iii', True, 'karl.gospel25@gmail.com')")
    print(pd.read_sql("SELECT * FROM Login", conn))

    # Create Project Messages table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS ProjectMessages("
        "MESSAGE_ID INTEGER PRIMARY KEY AUTOINCREMENT, "
        "PROJECT_ID INTEGER NOT NULL, "
        "MESSAGE TEXT, "
        "DATE_ADDED DATETIME DEFAULT CURRENT_TIMESTAMP,"
        "CONSTRAINT FK_PROJECT FOREIGN KEY (PROJECT_ID) REFERENCES Project(PROJECT_ID) ON DELETE CASCADE"
        ")")

    cur.execute("INSERT INTO ProjectMessages ("
                "PROJECT_ID,"
                "MESSAGE) VALUES ( 1, 'too hard')")
    print(pd.read_sql("SELECT * FROM ProjectMessages", conn))

    # Create Project Members table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS ProjectMembers("
        "MEMBER_ID INTEGER PRIMARY KEY AUTOINCREMENT, "
        "USERNAME TEXT NOT NULL, "
        "PROJECT_ID INTEGER NOT NULL,"
        "PROJECT_NAME INTEGER NOT NULL,"
        "DATE_ADDED DATETIME DEFAULT CURRENT_TIMESTAMP,"
        "CONSTRAINT FK_PROJECT FOREIGN KEY (PROJECT_ID) REFERENCES Project(PROJECT_ID) ON DELETE CASCADE"
        ")")

    cur.execute("INSERT INTO ProjectMembers ("
                "USERNAME,"
                "PROJECT_NAME,"
                "PROJECT_ID) VALUES ('Karl Gospel','Save Bubba', 1)")
    print(pd.read_sql("SELECT * FROM ProjectMembers", conn))

    # Create Task Messages table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS TaskMessages("
        "MESSAGE_ID INTEGER PRIMARY KEY AUTOINCREMENT, "
        "USERNAME TEXT NOT NULL, "
        "TASK_ID INTEGER NOT NULL, "
        "MESSAGE TEXT, "
        "DATE_ADDED DATETIME DEFAULT CURRENT_TIMESTAMP,"
        "CONSTRAINT FK_TASKS FOREIGN KEY (TASK_ID) REFERENCES Tasks(TASK_ID) ON DELETE CASCADE"
        ")")

    print(pd.read_sql("SELECT * FROM TaskMessages", conn))

    conn.commit()
    conn.close()





def View():
    conn = sqlite3.connect("profile.db")
    cur = conn.cursor()
    #Choose what to display from database here
    cur.execute("SELECT * FROM profile")
    rows = cur.fetchall()
    for row in rows:
        print(row) # it print all records in the database
        #tree.insert("", tk.END, values=row)
    conn.close()

connect()
