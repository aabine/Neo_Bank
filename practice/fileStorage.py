import json
import logging
import sqlite3
from pathlib import Path

class DataHandler:
    """Handles data operations with both JSON files and SQLite database."""
    
    def __init__(self, db_file, json_file):
        """Initialize the DataHandler with paths to the database file and JSON file."""
        self.db_file = db_file
        self.json_file = json_file
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.db_file)
            self._ensure_files_exist()
        except sqlite3.DatabaseError as e:
            logging.error(f"Error connecting to {self.db_file}: {e}")
            if self.conn:
                self.close()
            raise

    def _ensure_files_exist(self):
        """Ensure both files exist on the filesystem."""
        for file_path in [self.db_file, self.json_file]:
            if not Path(file_path).exists():
                if file_path == self.db_file:
                    self._initialize_database()
                else:
                    self.save({})

    def _initialize_database(self):
        """Initialize the SQLite database."""
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS banks (
                    id TEXT PRIMARY KEY,
                    creation_datetime TEXT,
                    last_modified TEXT,
                    name TEXT,
                    location TEXT,
                    branch TEXT,
                    ifsc TEXT,
                    contact TEXT,
                    email TEXT,
                    account_types TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    bank_id TEXT,
                    name TEXT,
                    email TEXT,
                    contact TEXT,
                    role TEXT,
                    FOREIGN KEY (bank_id) REFERENCES banks(id)
                )
            """)

    def save(self, data):
        """Save data to the JSON file."""
        try:
            with open(self.json_file, 'w') as f:
                json.dump(data, f, indent=4)
        except OSError as e:
            logging.error(f"Error saving to {self.json_file}: {e}")
            raise

    def read(self):
        """Read data from the JSON file."""
        try:
            with open(self.json_file, 'r') as f:
                return json.load(f)
        except (OSError, IOError, json.JSONDecodeError) as e:
            logging.error(f"Error reading from {self.json_file}: {e}")
            raise

    def execute_query(self, query, args=None):
        """Execute a query on the SQLite database."""
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query, args or ())
            return cursor

    def fetch_all(self, query, args=None):
        """Fetch all rows after executing a query on the SQLite database."""
        cursor = self.execute_query(query, args)
        return cursor.fetchall()

    def fetch_one(self, query, args=None):
        """Fetch a single row after executing a query on the SQLite database."""
        cursor = self.execute_query(query, args)
        return cursor.fetchone()

    def commit(self):
        """Commit changes to the SQLite database."""
        try:
            self.conn.commit()
        except sqlite3.DatabaseError as e:
            logging.error(f"Error committing to {self.db_file}: {e}")
            raise

    def close(self):
        """Close the SQLite database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
