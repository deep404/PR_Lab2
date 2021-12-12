# Importing all needed libraries.
import sqlite3
from sqlite3 import Error

# Defining the Data Base Manager class.
class DataBaseManager:
    def __init__(self, db_path : str):
        '''
            The constructor of the Data Base Manager.
        :param db_path: str
            The pth to the data base file.
        '''
        # Trying to connect to the data base.
        try:
            self.conn = sqlite3.connect(db_path)
        except Error as e:
            print(e)

        # Creating the cursor.
        self.cursor = self.conn.cursor()

        # Defining the remainder table creation query.
        self.remainder_table_creation_query = '''CREATE TABLE IF NOT EXISTS remainders(
                                                 id integer PRIMARY KEY,
                                                 name text NOT NULL,
                                                 body text NOT NULL,
                                                 time text NOT NULL);'''

        # Defining the task table creation query.
        self.task_table_creation_query = '''CREATE TABLE IF NOT EXISTS tasks(
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            body text NOT NULL,
                                            due_date text NOT NULL);'''

        # Defining the remainder insert query.
        self.remainder_insert_query = '''INSERT INTO remainders (name,
                                                                 body,
                                                                 time)
                                         VALUES (?, ?, ?)'''

        # Defining the task insert query.
        self.task_insert_query = '''INSERT INTO tasks (name,
                                                       body,
                                                       due_date)
                                    VALUES (?, ?, ?)'''

        # Creating the remainder and task query and committing the changes.
        self.cursor.execute(self.remainder_table_creation_query)
        self.cursor.execute(self.task_table_creation_query)
        self.conn.commit()

    def add_remainder(self, name, body, time):
        '''
            The remainder insertion function.
        :param name: str
            The name of the remainder.
        :param body: str
            The body of the remainder.
        :param time: str
            The time of the remainder.
        '''
        self.cursor.execute(self.remainder_insert_query, (name, body, time))
        self.conn.commit()

    def add_task(self, name, body, due_date):
        '''
            The task insertion function.
        :param name: str
            The name of the task.
        :param body: str
            The body of the task.
        :param due_date: str
            The due date and time of the task.
        '''
        self.cursor.execute(self.task_insert_query, (name, body, due_date))
        self.conn.commit()

    def close(self):
        '''
            This function closes the access to the data base.
        '''
        self.cursor.close()
        self.conn.close()