# database.py
import sqlite3
import pymysql
from config import DB_CONFIG


class Database:
    def __init__(self):
        self.engine = "mysql"
        self.connection = None
        self.cursor = None

        try:
            self.connection = pymysql.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor()
        except Exception as exc:
            print(f"MySQL unavailable, falling back to SQLite: {exc}")
            self.engine = "sqlite"
            self.connection = sqlite3.connect("resume_app.db")
            self.cursor = self.connection.cursor()

        self._initialize_database()

    def _initialize_database(self):
        """Initialize database and tables"""
        if self.engine == "mysql":
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS CV;")
            self.connection.select_db("CV")
            table_sql = """CREATE TABLE IF NOT EXISTS user_data (
                            ID INT NOT NULL AUTO_INCREMENT,
                            Name varchar(500) NOT NULL,
                            Email_ID VARCHAR(500) NOT NULL,
                            resume_score VARCHAR(8) NOT NULL,
                            Timestamp VARCHAR(50) NOT NULL,
                            Page_no VARCHAR(5) NOT NULL,
                            Predicted_Field TEXT NOT NULL,
                            User_level TEXT NOT NULL,
                            Actual_skills TEXT NOT NULL,
                            Recommended_skills TEXT NOT NULL,
                            Recommended_courses TEXT NOT NULL,
                            PRIMARY KEY (ID));
                        """
        else:
            table_sql = """CREATE TABLE IF NOT EXISTS user_data (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            Name TEXT NOT NULL,
                            Email_ID TEXT NOT NULL,
                            resume_score TEXT NOT NULL,
                            Timestamp TEXT NOT NULL,
                            Page_no TEXT NOT NULL,
                            Predicted_Field TEXT NOT NULL,
                            User_level TEXT NOT NULL,
                            Actual_skills TEXT NOT NULL,
                            Recommended_skills TEXT NOT NULL,
                            Recommended_courses TEXT NOT NULL
                        );
                    """

        self.cursor.execute(table_sql)
        self.connection.commit()

    def insert_candidate_data(self, data):
        """Insert candidate data into database"""
        if self.engine == "mysql":
            sql = """INSERT INTO user_data 
                    VALUES (0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            self.cursor.execute(sql, data)
        else:
            sql = """INSERT INTO user_data (
                    Name, Email_ID, resume_score, Timestamp, Page_no,
                    Predicted_Field, User_level, Actual_skills,
                    Recommended_skills, Recommended_courses)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            self.cursor.execute(sql, data)
        self.connection.commit()

    def get_all_candidates(self):
        """Retrieve all candidate data"""
        self.cursor.execute('''SELECT * FROM user_data''')
        columns = [col[0] for col in self.cursor.description]
        data = self.cursor.fetchall()
        return columns, data

    def close(self):
        """Close database connection"""
        self.connection.close()