import unittest
import pytest
import sqlite3
from unittest.mock import patch
import pandas as pd

class MyTestCase(unittest.TestCase):

    def setUp(self):
        # Create a test database and insert test data into Login table
        conn = sqlite3.connect("test.db")
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
            ('john_smith', 'password', 'user1@test.com', 0),
            ('joe_bloggs', 'password2', 'user2@test.com', 1),
            ('ben_dover', 'password3', 'user3@test.com', 0),
        ]
        cur.executemany(
            "INSERT INTO Login (USERNAME, PASSWORD, ADMIN,EMAIL) VALUES (?,?,?,?)", test_data)
        # Print the SQL query and contents of the Login table
        #print("Test data inserted:")
        #print(pd.read_sql("SELECT * FROM Login", conn))
        conn.commit()
        conn.close()



    def check_username_distinct(self, username):
        conn = sqlite3.connect("test.db")
        cur = conn.cursor()
        sql = ("SELECT USERNAME FROM Login WHERE USERNAME = (?)")
        #print("Executing SQL query:", sql)
        cur.execute(sql, [username])
        user = cur.fetchone()
        #print("User:", user)
        if user is None:
            conn.commit()
            conn.close()
            #print("Returning True")
            return True
        else:
            conn.commit()
            conn.close()
            #print("Returning False")
            return False

    def test_check_username_distinct(self):
        # Test cases
        assert self.check_username_distinct("mary_jones") == True
        assert self.check_username_distinct("john_smith") == False
        assert self.check_username_distinct("john smith") == True
        assert self.check_username_distinct("joe_bloggs") == False
        assert self.check_username_distinct("John_smith") == True
        assert self.check_username_distinct("ben_dover") == False


if __name__ == '__main__':
    unittest.main()
