from datetime import datetime
import enum
import uuid
from BankApp.BankOp import BankOperation
import bcrypt


class AccountStatus(enum.Enum):
    ACTIVE = 1
    INACTIVE = 0
    FROZEN = 2
    SUSPENDED = 3

class AccountType(enum.Enum):
    SAVING = 1
    CURRENT = 2
    FIXED_DEPOSIT = 3
    RECURRING_DEPOSIT = 4

class UserOperations(BankOperation):
    def __init__(self, db_manager):
        super().__init__(db_manager)

    def register_user(self, username, password, first_name, last_name, bank_name, email):
        with self.db_manager.pool.item() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
                if cursor.fetchone() is not None:
                    return "Username already exists in this bank."
                user_account_number = uuid.uuid4().hex[:8]

                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                # Retrieve the bank_registration_number based on the bank_name
                cursor.execute("SELECT bank_registration_number FROM banks WHERE bank_name = ?", (bank_name,))
                bank_registration_number = cursor.fetchone()

                if bank_registration_number is None:
                    return "Bank not found."

                account_type_value = AccountType.SAVING.value
                account_status_value = AccountStatus.ACTIVE.value
                created_at = datetime.datetime.now().strftime('%Y-%m-%d - %H:%M:%S')
                updated_at = datetime.datetime.now().strftime('%Y-%m-%d - %H:%M:%S')

                cursor.execute(
                    """
                    INSERT INTO users (username, password, first_name, last_name, bank_id, email, account_type, status, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (username, hashed_password, first_name, last_name, bank_registration_number[0], email, account_type_value, account_status_value, created_at, updated_at)
                )
                conn.commit()
        return "User registration successful!"
    
    def update_user(self, user_account_number, username, first_name, last_name, email, account_type):
        with self.db_manager.pool.item() as conn:
            with conn.cursor() as cursor:
                # Check if the username is taken by another user
                cursor.execute(
                    "SELECT 1 FROM users WHERE (username = ? OR email = ?) AND user_account_number != ?", 
                    (username, email, user_account_number)
                )
                if cursor.fetchone() is not None:
                    return "Username or email already exists in this bank."
    
                # Update the user information in a single query
                statement = """
                UPDATE users
                SET
                    username = ?,
                    first_name = ?,
                    last_name = ?,
                    email = ?,
                    account_type = ?
                WHERE user_account_number = ?
                """
                params = (username, first_name, last_name, email, account_type, user_account_number)
    
                cursor.execute(statement, params)
                conn.commit()
    
        return "User updated successfully."
    
    def delete_user(self, user_account_number):
        with self.db_manager.pool.item() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE user_account_number = ?", (user_account_number,))
                conn.commit()
        return "User deleted successfully."
    
    def __del__(self):
        self.db_manager.close()
    
    def login(self, username, password):
        try:
            with self.db_manager.pool.item() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT password, bank_id, account_type, status FROM users WHERE username = ?", (username,))
                    user_data = cursor.fetchone()
    
                    if user_data is None:
                        return None
    
                    hashed_password = user_data['password'].encode('utf-8')
                    if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                        return None
    
                    # Remove the password from user_data before returning
                    del user_data['password']
                    return user_data
        except Exception as e:
            # Log the exception or handle it as needed
            return None
        
    def logout(self, username):
        return "User logged out successfully."
    
    def reset_password(self, username, new_password, old_password):
        # Hash the new password
        hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    
        with self.db_manager.pool.item() as conn:
            with conn.cursor() as cursor:
                # Retrieve the current hashed password for the username
                cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
                user_record = cursor.fetchone()
                if user_record is None:
                    return "User not found."
    
                # Check if the provided old password matches the stored hashed password
                if not bcrypt.checkpw(old_password.encode('utf-8'), user_record['password'].encode('utf-8')):
                    return "Old password is incorrect."
   
                # Update the database with the new hashed password
                cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_new_password, username))
                conn.commit()
        return "Password reset successful!"

    
    def get_user_by_username(self, username):
        # Prepare the SQL statement and parameters
        statement = "SELECT * FROM users WHERE username = ?"
        params = (username,)
        return self._prepare_statement(statement).execute(params).fetchone()

    def get_user_by_id(self, user_id):
        # Prepare the SQL statement and parameters
        statement = "SELECT * FROM users WHERE user_id = ?"
        params = (user_id,)
        return self._prepare_statement(statement).execute(params).fetchone()
    
    def change_user_status(self, user_id, status, admin_id):
        try:
            with self.db_manager.pool.item() as conn:
                with conn.cursor() as cursor:
                    # Check if the admin_id is associated with an admin user
                    cursor.execute("SELECT 1 FROM admins WHERE admin_id = ?", (admin_id,))
                    if cursor.fetchone() is None:
                        return "Admin privileges required."
    
                    # Check if the user exists
                    cursor.execute("SELECT 1 FROM users WHERE user_account_number = ?", (user_id,))
                    if cursor.fetchone() is None:
                        return "User not found."
    
                    # Prepare the SQL statement and parameters
                    statement = "UPDATE users SET status = ? WHERE user_account_number = ?"
                    params = (status, user_id)
    
                    # Execute the prepared statement
                    self._execute_prepared_statement(statement, params)
                    return "User status updated successfully."
    
        except Exception as e:
            # Log the exception or handle it as needed
            return f"An error occurred: {e}"