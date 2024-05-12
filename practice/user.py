import datetime
from enum import Enum
import json
import secrets

from practice.bank import BankOperation


class AccountState(Enum):
    ACTIVE = 1
    CLOSED = 2
    FROZEN = 3
    ARCHIVED = 4


class AccountStateEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, AccountState):
            return o.value
        return super().default(o)

# inherit bank operation
class UserOperation(BankOperation):
    def __init__(self):
        super().__init__()

    def create_user(self, bank_id, account_type, name, email, password, pin):
        # Read the current state of all banks
        banks = self.read()
        # Check if the bank with the given bank_id exists
        bank = banks.get(bank_id)
        if not bank:
            return "Bank ID not found."
        
        # Generate a new user ID
        user_id = int(secrets.token_hex(5)[:8], 16)
        
        # Create the user dictionary
        new_user = {
            "id": user_id,
            "name": name,
            "email": email,
            "password": password,
            "balance": 0,
            "transaction_history": [],
            "transaction_pin": pin,
            "state": AccountState.ACTIVE.value,
            "state_change_date": str(datetime.date.today()),
            "state_change_time": str(datetime.datetime.now().time())
        }
        
        # Add the new user to the bank's "users" list
        bank["users"].update({user_id: new_user})
        # Save the updated state of banks
        self.save(banks)
        
        # Return the new user
        return new_user

    def update_user(self, user_id, **kwargs):
        users = self.read()
        for user in users:
            if user["id"] == user_id:
                for key, value in kwargs.items():
                    if key == "name" and not isinstance(value, str):
                        return "Invalid name, must be a string"
                    elif key == "email" and not isinstance(value, str):
                        return "Invalid email, must be a string"
                    elif key == "password" and not isinstance(value, str):
                        return "Invalid password, must be a string"
                    elif key == "pin" and not isinstance(value, int):
                        return "Invalid pin, must be an integer"
                    else:
                        user[key] = value
                user["last_modified"] = str(datetime.date.today())
                self.save(users, encoder=AccountStateEncoder)
                return json.dumps(user, cls=AccountStateEncoder)
        return None

    def delete_user(self, user_id):
        """Delete a user by id"""
        if not isinstance(user_id, int):
            return "Invalid user_id, must be an integer"
        users = self.read()
        for i, user in enumerate(users):
            if user["id"] == user_id:
                del users[i]
                self.save(users, encoder=AccountStateEncoder)
                return True
        return False

    def list_users(self):
        """List all users"""
        users = self.read()
        return "\n".join(
            f"{user['id']:<10} {user['name']} {user['state']}"
            for user in users
        )

    def read_user(self, user_id):
            """Read a user by id"""
            if not isinstance(user_id, int):
                return "Invalid user_id, must be an integer"
            users = self.read()
            for user in users:
                if user["id"] == user_id:
                    return json.dumps(user, cls=AccountStateEncoder)
            return None

    def freeze(self, account_id):
        """Freeze an account"""
        if not isinstance(account_id, int):
            return "Invalid account_id, must be an integer"

        users = self.read()
        for user in users:
            if user["id"] == account_id:
                if user["state"] != AccountState.ACTIVE.value:
                    return "Account is not active."

                user["state"] = AccountState.FROZEN.value
                user["state_change_date"] = str(datetime.date.today())
                user["state_change_time"] = str(
                    datetime.datetime.now().time())
                self.save(users, encoder=AccountStateEncoder)
                return f"Account {account_id} has been frozen."
        return "Account not found."

    def unfreeze(self, account_id, pin):
        """Unfreeze an account"""
        if not isinstance(account_id, int):
            return "Invalid account_id, must be an integer"
        if not isinstance(pin, int):
            return "Invalid pin, must be an integer"

        users = self.read()
        for user in users:
            if user["id"] == account_id:
                if user["transaction_pin"] != pin:
                    return "Invalid pin."
                if user["state"] != AccountState.FROZEN:
                    return "Account is not frozen."

                user["state"] = AccountState.ACTIVE.value
                user["state_change_date"] = str(datetime.date.today())
                user["state_change_time"] = str(datetime.datetime.now().time())
                self.save(users, encoder=AccountStateEncoder)
                return f"Account {account_id} has been unfrozen."
        return "Account not found."

    def close(self, account_id, pin):
        """Close an account"""
        if not isinstance(account_id, int):
            return "Invalid account_id, must be an integer"
        if not isinstance(pin, int):
            return "Invalid pin, must be an integer"

        users = self.read()
        for user in users:
            if user["id"] == account_id:
                if user["transaction_pin"] != pin:
                    return "Invalid pin."
                if user["state"] == AccountState.CLOSED.value:
                    return "Account is already closed."

                user["state"] = AccountState.CLOSED
                user["state_change_date"] = str(datetime.date.today())
                user["state_change_time"] = str(datetime.datetime.now().time())
                self.save(users, encoder=AccountStateEncoder)
                return f"Account {account_id} has been closed."
        return "Account not found."

    def archive(self, account_id, pin):
        """Archive an account"""
        if not isinstance(account_id, int):
            return "Invalid account_id, must be an integer"
        if not isinstance(pin, int):
            return "Invalid pin, must be an integer"

        users = self.read()
        for user in users:
            if user["id"] == account_id:
                if user["transaction_pin"] != pin:
                    return "Invalid pin."
                if user["state"] == AccountState.ARCHIVED.value:
                    return "Account is already archived."

                user["state"] = AccountState.ARCHIVED
                user["state_change_date"] = str(datetime.date.today())
                user["state_change_time"] = str(datetime.datetime.now().time())
                self.save(users, encoder=AccountStateEncoder)
                return f"Account {account_id} has been archived."
        return "Account not found."
    
    def unarchive(self, account_id, pin):
        """Unarchive an account"""
        if not isinstance(account_id, int):
            return "Invalid account_id, must be an integer"
        if not isinstance(pin, int):
            return "Invalid pin, must be an integer"

        users = self.read()
        for user in users:
            if user["id"] == account_id:
                if user["transaction_pin"] != pin:
                    return "Invalid pin."
                if user["state"] == AccountState.ACTIVE.value:
                    return "Account is already active."

                user["state"] = AccountState.ACTIVE
                user["state_change_date"] = str(datetime.date.today())
                user["state_change_time"] = str(datetime.datetime.now().time())
                self.save(users, encoder=AccountStateEncoder)
                return f"Account {account_id} has been unarchived."
        return "Account not found."
               

