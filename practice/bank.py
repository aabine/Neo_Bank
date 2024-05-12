from practice.fileStorage import FileOperation, DataBase
import datetime
import uuid
import json


class BankDb(DataBase, FileOperation):
    """Handles database operations with a SQLite database."""

    def __init__(self, db_file):
        """Initialize the DataBase with a path to the database file."""
        super().__init__(db_file)
        self.create_tables()

    def create_tables(self):
        self._execute("""
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
        self._execute("""
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

    def create_bank(self, bank):
        self._execute(
            """
            INSERT INTO banks (
                id, creation_datetime, last_modified, name, location, branch, ifsc, contact, email, account_types
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                bank["id"],
                bank["creation_datetime"],
                bank["last_modified"],
                bank["name"],
                bank["location"],
                bank["branch"],
                bank["ifsc"],
                bank["contact"],
                bank["email"],
                json.dumps(bank["account_types"]),
            ),
        )

    def update_bank(self, bank_id, **kwargs):
        bank = self.read_bank(bank_id)
        for key, value in kwargs.items():
            bank[key] = value
        self._execute(
            """
            UPDATE banks SET
                last_modified = ?,
                name = ?,
                location = ?,
                branch = ?,
                ifsc = ?,
                contact = ?,
                email = ?,
                account_types = ?
            WHERE id = ?
            """,
            (
                bank["last_modified"],
                bank["name"],
                bank["location"],
                bank["branch"],
                bank["ifsc"],
                bank["contact"],
                bank["email"],
                json.dumps(bank["account_types"]),
                bank_id,
            ),
        )
        return bank

    def delete_bank(self, bank_id):
        self._execute("DELETE FROM banks WHERE id = ?", (bank_id,))
        return self._execute("SELECT * FROM banks WHERE id = ?", (bank_id,)).fetchone() is None

    def list_banks(self):
        return [
            {
                "id": row["id"],
                "name": row["name"],
            }
            for row in self._execute("SELECT id, name FROM banks")
        ]

    def read_bank(self, bank_id):
        bank = self._execute("SELECT * FROM banks WHERE id = ?", (bank_id,)).fetchone()
        if not bank:
            raise ValueError("Bank not found")
        bank = dict(bank)
        bank["account_types"] = json.loads(bank["account_types"])
        return bank

    def add_staff(self, bank_id, name, email, contact, role):
        self._execute(
            """
            INSERT INTO users (id, bank_id, name, email, contact, role)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                str(uuid.uuid4()),
                bank_id,
                name,
                email,
                contact,
                role,
            ),
        )
        return self.read_staff(bank_id, str(uuid.uuid4()))

    def list_staff(self, bank_id):
        return [
            {
                "id": row["id"],
                "name": row["name"],
                "email": row["email"],
                "contact": row["contact"],
                "role": row["role"],
            }
            for row in self._execute("SELECT id, name, email, contact, role FROM users WHERE bank_id = ?", (bank_id,))
        ]

    def read_staff(self, bank_id, staff_id):
        staff = self._execute("SELECT * FROM users WHERE id = ? AND bank_id = ?", (staff_id, bank_id)).fetchone()
        if not staff:
            raise ValueError("Staff not found")
        return dict(staff)
