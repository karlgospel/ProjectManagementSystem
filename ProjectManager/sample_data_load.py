import sqlite3
import pandas as pd
from super_admin import SuperAdmin
from project import Project
from task import Task


def load_login_data():
    # Create a test database and run create login function for each row
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Login")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Login("
        "USER_ID INTEGER PRIMARY KEY AUTOINCREMENT, "
        "USERNAME TEXT UNIQUE, "
        "PASSWORD TEXT,"
        "EMAIL TEXT,"
        "ADMIN BOOLEAN NOT NULL "
        ")")
    test_data = [
        ('karl_gospel', 'pass', 'user1@test.com', 1),
        ('indiana_jones', 'pass', 'user2@test.com', 0),
        ('andy_dufresne', 'pass', 'user3@test.com', 1),
        ('marty_mcfly', 'pass', 'user4@test.com', 0),
        ('james_bond', 'pass', 'user5@test.com', 0),
        ('han_solo', 'pass', 'user6@test.com', 1),
        ('tyler_durden', 'pass', 'user7@test.com', 0),
        ('ellen_ripley', 'pass', 'user8@test.com', 0),
        ('john_mcClane', 'pass', 'user9@test.com', 1),
        ('michael_corleone', 'pass', 'user10@test.com', 0),
        ('tony_stark', 'pass', 'user11@test.com', 0),
        ('jack_sparrow', 'pass', 'user12@test.com', 1),
        ('ron_burgundy', 'pass', 'user13@test.com', 0),
        ('forrest_gump', 'pass', 'user14@test.com', 0),
        ('john_connor', 'pass', 'user15@test.com', 1),
        ('ferris_bueller', 'pass', 'user16@test.com', 0),
        ('keyser_soze', 'pass', 'user17@test.com', 0),
        ('luke_skywalker', 'pass', 'user18@test.com', 1),
        ('bilbo_baggins', 'pass', 'user19@test.com', 0),
    ]
    sa = SuperAdmin()
    for i in test_data:
        #print(*i)
        sa.create_login(*i)
    #Print the SQL query and contents of the Login table
    print("Login data inserted:")
    print(pd.read_sql("SELECT * FROM Login", conn))
    conn.commit()
    conn.close()

def load_project_data():
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Project")
    # create projects table
    cur.execute("CREATE TABLE IF NOT EXISTS Project("
                "PROJECT_ID INTEGER PRIMARY KEY AUTOINCREMENT, "
                "PROJECT_NAME TEXT UNIQUE ON CONFLICT REPLACE, "
                "START_DATE DATETIME, "
                "END_DATE DATETIME, "
                "STATUS TEXT, "
                "DESCRIPTION TEXT, "
                "PERCENTAGE_COMPLETE INTEGER, "
                "OWNER TEXT)")

    test_data = [
        ('Product Launch Bonanza', 'tony_stark', 'Not Started', 'We''re launching a new type of suit which is strong, durable and possibly deadly'),
        ('AI Safety Initiative', 'john_connor', 'Not Started', 'With all this AI hype we want to ensure our new robots are safe and won''t bring about the total annihilation of the human race'),
        ('Retro Website Redesign', 'marty_mcfly', 'In-Progress','We think our website is too modern. Let''s turn back time and bring more of an old school feel'),
        ('Sales Training Program', 'forrest_gump', 'In-Progress', 'Selling shrimp is the future. We want to train a team on how to sell this smelly gold'),
        ('Staff Exercise Plan', 'bilbo_baggins', 'In-Progress', 'Our staff are looking a bit chunky. We''d like an exercise programme to help get those beach bods back. We''re thinking possibly a really long walk'),
        ('Social Club Campaign', 'tyler_durden', 'Not Started', 'We want to bring people together. Organise a club where members can let off some steam'),
        ('Ancient Relic Recovery', 'indiana_jones', 'In-Progress', 'Our clients have lost one of their cups and need help to find it'),

    ]

    p =Project()
    for i in test_data:
        p.create_project(*i)
    print("Project data inserted:")
    print(pd.read_sql("SELECT * FROM Project", conn))

def load_task_data():
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Tasks")
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

    test_data = [
        ('Product Launch Bonanza','Choose a nice colour','We need this suit to pop! Create a survey to find out what colour the public like for a suit', 'Not Started', 'james_bond'),
        ('Product Launch Bonanza', 'Make it fly',
         'Let''s make the suit really stand out from the crowd. Design and build some thrusters for a little extra oomph', 'In-Progress',
         'han_solo'),
        ('AI Safety Initiative', 'Safety manual',
         'Write a safety manual for our new robot friends',
         'In-Progress',
         'keyser_soze'),
        ('AI Safety Initiative', 'New friendly look',
         'Design a new style for our new T-1000 model. Maybe quite large with an accent and make them friendly',
         'In-Progress',
         'ron_burgundy'),
        ('Retro Website Redesign', 'Research different eras',
         'Find out which eras are most popular so we can apply this style. Maybe 50''s or western',
         'In-Progress',
         'han_solo'),
        ('Retro Website Redesign', 'Wireframe website',
         'After we have an era to focus on, create a wireframe fot the big boss',
         'Not Started',
         'andy_dufresne'),
        ('Sales Training Program', 'Train some monkeys',
         'We have some new egyptian monkey that are raring to go. Train them how to sell and let them loose',
         'In-Progress',
         'jack_sparrow'),
        ('Staff Exercise Plan', 'Map out a walk',
         'Find a good path for a walk. Make it long and hilly',
         'In-Progress',
         'ellen_ripley'),
        ('Staff Exercise Plan', 'Snacks to bring',
         'Research some good snacks to bring for the walk',
         'In-Progress',
         'ron_burgundy'),
        ('Social Club Campaign', 'Create an activity plan',
         'Find some games to play for our new friends. Nothing too intense',
         'In-Progress',
         'james_bond'),
        ('Ancient Relic Recovery', 'Create a map',
         'We need to find this cup. Do some research and create a map to locate it',
         'In-Progress',
         'jack_sparrow'),
        ('Ancient Relic Recovery', 'Find a comfortable outfit',
         'This trip will be long and tough. We need some good clothes to handle whatever is thrown at us. Add a hat to look cool',
         'In-Progress',
         'michael_corleone'),
    ]
    t=Task()
    for i in test_data:
        t.create_task(*i)
    print("Task data inserted:")
    print(pd.read_sql("SELECT * FROM Tasks", conn))


load_login_data()
# load_project_data()
# load_task_data()