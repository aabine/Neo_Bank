import uuid
from BankApp.fileStorage import DatabaseManager


class BankOperation(DatabaseManager):
    def __init__(self):
        super().__init__("bank.db")

    def create_admin(self, username, password, admin_name):
        admin_id = str(uuid.uuid4().hex)[:8]
        statement = "INSERT INTO admin (admin_id, username, password, admin_name, created_at) VALUES (?, ?, ?, ?, DATETIME('now'))"
        params = (admin_id, username, password, admin_name)
        self._execute_prepared_statement(statement, params)

    def update_admin(self, admin_id, username, password, admin_name):
        statement = "UPDATE admin SET username = ?, password = ?, admin_name = ? WHERE admin_id = ?"
        params = (username, password, admin_name, admin_id)
        self._execute_prepared_statement(statement, params)

    def delete_admin(self, admin_id):
        statement = "DELETE FROM admin WHERE admin_id = ?"
        params = (admin_id,)
        self._execute_prepared_statement(statement, params)

    def get_admin(self, admin_id):
        statement = "SELECT * FROM admin WHERE admin_id = ?"
        params = (admin_id,)
        return self._prepare_statement(statement).execute(params).fetchone()
    
    def get_admins(self):
        statement = "SELECT * FROM admin"
        return self._prepare_statement(statement).execute().fetchall()

    def create_bank(self, Bank_name, address, location, branch, ifsc, contact, email, account_types, admin_id):
        bank_registration_number = str(uuid.uuid4().hex)[:8]
        # Specify the column names for clarity and to avoid future errors if the table structure changes
        statement = """
        INSERT INTO banks (
            bank_registration_number, 
            Bank_name, 
            address, 
            created_at, 
            modified_at, 
            location, 
            branch, 
            ifsc, 
            contact, 
            email, 
            account_types, 
            admin_id
        ) VALUES (?, ?, ?, DATETIME('now'), DATETIME('now'), ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            bank_registration_number,
            Bank_name,
            address,
            location,
            branch,
            ifsc,
            contact,
            email,
            account_types,
            admin_id
        )
        self._execute_prepared_statement(statement, params)

    def update_bank(self, bank_registration_number, Bank_name, address, location, branch, ifsc, contact, email, account_types, admin_id):
        statement = "UPDATE banks SET Bank_name = ?, address = ?, location = ?, branch = ?, ifsc = ?, contact = ?, email = ?, account_types = ?, admin_id = ? WHERE registration_number = ?"
        params = (Bank_name, address, location, branch, ifsc, contact,
                  email, account_types, admin_id, bank_registration_number)
        self._execute_prepared_statement(statement, params)

    def delete_bank(self, bank_registration_number):
        statement = "DELETE FROM banks WHERE registration_number = ?"
        params = (bank_registration_number,)
        self._execute_prepared_statement(statement, params)

    def get_banks(self):
        statement = "SELECT * FROM banks"
        return self._prepare_statement(statement).execute().fetchall()

    def get_bank_by_id(self, bank_registration_number):
        statement = "SELECT * FROM banks WHERE registration_number = ?"
        params = (bank_registration_number,)
        return self._prepare_statement(statement).execute(params).fetchone()

    def create_staff(self, staff_name, staff_email, staff_contact, bank_registration_number):
        staff_id = str(uuid.uuid4().hex)[:8]
        statement = "INSERT INTO BankStaff VALUES (?, ?, ?, ?, ?, DATETIME('now'))"
        params = (staff_id, staff_name, staff_email,
                  staff_contact, bank_registration_number)
        self._execute_prepared_statement(statement, params)

    def update_staff(self, staff_id, staff_name, staff_email, staff_contact):
        statement = "UPDATE BankStaff SET staff_name = ?, staff_email = ?, staff_contact = ? WHERE staff_id = ?"
        params = (staff_name, staff_email, staff_contact, staff_id)
        self._execute_prepared_statement(statement, params)

    def delete_staff(self, staff_id):
        statement = "DELETE FROM BankStaff WHERE staff_id = ?"
        params = (staff_id,)
        self._execute_prepared_statement(statement, params)

    def get_staffs(self, bank_registration_number):
        statement = "SELECT * FROM BankStaff WHERE bank_registration_number = ?"
        params = (bank_registration_number,)
        return self._prepare_statement(statement).execute(params).fetchall()

    def get_staff_by_id(self, staff_id):
        statement = "SELECT * FROM BankStaff WHERE staff_id = ?"
        params = (staff_id,)
        return self._prepare_statement(statement).execute(params).fetchone()
