from datetime import datetime
import sqlite3
import uuid

class DatabaseManager:
    """Manages the SQLite database connection and table creation."""

    def __init__(self, db_path: str) -> None:
        """Initialize the database manager."""
        self.db_path = db_path
        self._ensure_connection()
        self._ensure_tables_exist()

    def _ensure_connection(self) -> None:
        """Ensure a connection to the SQLite database exists."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Allow accessing data by column names
        except sqlite3.Error as e:
            print(f"An error occurred while connecting to the database: {e}")
            raise

    def _ensure_tables_exist(self) -> None:
        """Ensure the required tables exist in the database."""
        cursor = self.conn.cursor()
        try:
            cursor.executescript("""
                CREATE TABLE IF NOT EXISTS admin (
                    admin_id INTEGER UNIQUE PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT,
                    admin_name TEXT,
                    created_at TEXT
                );
                                 
                CREATE TABLE IF NOT EXISTS banks (
                    bank_registration_number INTEGER PRIMARY KEY,
                    Bank_name TEXT UNIQUE,
                    address TEXT,
                    created_at TEXT,
                    modified_at TEXT,
                    location TEXT,
                    branch TEXT,
                    ifsc TEXT,
                    contact TEXT,
                    email TEXT,
                    account_types TEXT,
                    admin_id INTEGER,
                    FOREIGN KEY (admin_id) REFERENCES admin(admin_id)
                );

                CREATE TABLE IF NOT EXISTS BankStaff (
                    staff_id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    staff_name TEXT,
                    role TEXT CHECK (role IN ('admin', 'user')),
                    Staff_role TEXT CHECK (type IN ('Junior_staff', 'manager', 'vault_manager')),
                    email TEXT,
                    phone TEXT,
                    password TEXT,
                    created_at TEXT,
                    modified_at TEXT,
                    bank_id INTEGER,
                    FOREIGN KEY (bank_id) REFERENCES banks(bank_registration_number)
                );

                CREATE TABLE IF NOT EXISTS users (
                    user_account_number INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    email TEXT,
                    phone TEXT,
                    password TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    bank_id INTEGER,
                    created_at TEXT,
                    updated_at TEXT,
                    status TEXT CHECK (status IN ('active', 'inactive', 'Freeze', 'Suspended')),
                    account_type TEXT CHECK (account_type IN ('saving', 'current', 'fixed_deposit', 'recurring_deposit')),
                    balance REAL,
                    FOREIGN KEY (bank_id) REFERENCES banks(bank_registration_number)
                );

                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id TEXT PRIMARY KEY,
                    user_id INTEGER,
                    amount REAL,
                    type TEXT CHECK (type IN ('withdrawal', 'deposit', 'credit', 'debit')),
                    description TEXT,
                    created_at TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_account_number)
                );
            """)
            self.conn.commit()
        except sqlite3.Error as e:
          # Print a more specific error message
          error_msg = f"An error occurred creating tables: {e}. \nFailed table creation might be due to: \n - Syntax errors in CREATE TABLE statements. \n - Name conflicts with existing tables."
          print(error_msg)
          raise

    def close_connection(self) -> None:
        """Close the database connection."""
        self.conn.close()

    def _prepare_statement(self, statement: str) -> sqlite3.PreparedStatement:
        """Prepare an SQL statement."""
        return self.conn.cursor().execute(statement)

    def _execute_prepared_statement(self, statement: sqlite3.PreparedStatement, params: tuple) -> None:
        """Execute a prepared statement with the given parameters."""
        statement.execute(params)
        self.conn.commit()

    def _execute_prepared_statement_with_fetchall(self, statement: sqlite3.PreparedStatement, params: tuple) -> list:
        """Execute a prepared statement with the given parameters and return the result."""
        statement.execute(params)
        return statement.fetchall()
    
