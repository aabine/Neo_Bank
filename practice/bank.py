# bank class with crud operation
import datetime
from enum import Enum
import json
import uuid, math

import json
import logging
from pathlib import Path

class BankOperation:
    def __init__(self, filename='banks.json'):
        self.banks_file = Path(filename)
        # Ensure the file exists on initialization.
        if not self.banks_file.is_file():
            self.save({})

    def save(self, data):
        try:
            with self.banks_file.open('w') as f:
                json.dump(data, f, indent=4)
        except OSError as e:
            logging.error(f"Error saving {self.banks_file}: {e}")

    def read(self):
        try:
            with self.banks_file.open('r') as f:
                return json.load(f)
        except (OSError, IOError) as e:
            logging.error(f"Error reading {self.banks_file}: {e}")
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing {self.banks_file}: {e}")
        return {}
        

    def create_bank(self, name, location, branch, ifsc, contact, email, account_types):
        banks = self.read()
        if not isinstance(name, str):
            return "Invalid name, must be a string"
        if not isinstance(location, str):
            return "Invalid location, must be a string"
        if not isinstance(branch, str):
            return "Invalid branch, must be a string"
        if not isinstance(ifsc, str):
            return "Invalid ifsc, must be a string"
        if not isinstance(contact, str):
            return "Invalid contact, must be a string"
        if not isinstance(email, str):
            return "Invalid email, must be a string"
        if not isinstance(account_types, list):
            return "Invalid account_types, must be a list"
        for account_type in account_types:
            if not isinstance(account_type, str):
                return "Invalid account_type, must be a string"
        bank_id = str(uuid.uuid4())[:15]
        banks[bank_id] = {
            "id": bank_id,
            "creation_date": str(datetime.date.today()),
            "creation_time": str(datetime.datetime.now().time()),
            "last_modified": str(datetime.date.today()),
            "name": name,
            "location": location,
            "branch": branch,
            "ifsc": ifsc,
            "contact": contact,
            "email": email,
            "account_types": account_types["Savings", "Current"],
            "users": {},
        }
        self.save(banks)
        return banks[bank_id]

    def update_bank(self, bank_id, name, location, branch, ifsc, contact, email, account_types):
        banks = self.read()
        bank = banks.get(bank_id)
        if bank:
            if not isinstance(name, str):
                return "Invalid name, must be a string"
            if not isinstance(location, str):
                return "Invalid location, must be a string"
            if not isinstance(branch, str):
                return "Invalid branch, must be a string"
            if not isinstance(ifsc, str):
                return "Invalid ifsc, must be a string"
            if not isinstance(contact, str):
                return "Invalid contact, must be a string"
            if not isinstance(email, str):
                return "Invalid email, must be a string"
            if not isinstance(account_types, list):
                return "Invalid account_types, must be a list"
            for account_type in account_types:
                if not isinstance(account_type, str):
                    return "Invalid account_type, must be a string"
            bank["name"] = name
            bank["location"] = location
            bank["branch"] = branch
            bank["ifsc"] = ifsc
            bank["contact"] = contact
            bank["email"] = email
            bank["account_types"] = account_types
            bank["last_modified"] = str(datetime.date.today())
            self.save(banks)
            return bank
        return None

    def delete_bank(self, bank_id):
        banks = self.read()
        return banks.pop(bank_id, None)

    def list_banks(self):
        banks = self.read()
        return "\n".join(
            f"{bank['id']:<10} {bank['name']}"
            for bank in banks.values()
        )

    def read_bank(self, bank_id):
        banks = self.read()
        return banks.get(bank_id)

class AccountState(Enum):
  ACTIVE = 1
  CLOSED = 2
  FROZEN = 3
  ARCHIVED = 4

# inherit bank operation
class UserOperation(BankOperation):
    def __init__(self, account_type, name, email, password, pin):
        super().__init__()
        self.account_type = account_type
        self.name = name
        self.email = email
        self.password = password
        self.pin = pin

    def create_user(self, bank_id):
        banks = self.read()
        bank = banks.get(bank_id)
        if bank:
            if self.account_type not in bank["account_types"]:
                return "Invalid account_type, must be one of " + ", ".join(bank["account_types"])
            if not isinstance(self.name, str):
                return "Invalid name, must be a string"
            if not isinstance(self.email, str):
                return "Invalid email, must be a string"
            if not isinstance(self.password, str):
                return "Invalid password, must be a string"
            if not isinstance(self.pin, int):
                return "Invalid pin, must be an integer"
            user_id = str(uuid.uuid4())[:10]
            user = {
                "id": user_id,
                "bank_id": bank_id,
                "creation_date": str(datetime.date.today()),
                "creation_time": str(datetime.datetime.now().time()),
                "last_modified": str(datetime.date.today()),
                "bank_name": bank["name"],
                "account_type": self.account_type,
                "name": self.name,
                "email": self.email,
                "password": self.password,
                "balance": 0,
                "transaction_history": [],
                "transaction_pin": self.pin,
                "state": AccountState.ACTIVE,
                "state_change_date": str(datetime.date.today()),
                "state_change_time": str(datetime.datetime.now().time())
            }
            bank["users"][user_id] = user
            self.save(banks)
            return user
        else:
            return None
        
    def update_user(self, user_id, name, email, password, pin):
        banks = self.read()
        for bank in banks.values():
            user = bank['users'].get(user_id)
            if user:
                if not isinstance(name, str):
                    return "Invalid name, must be a string"
                if not isinstance(email, str):
                    return "Invalid email, must be a string"
                if not isinstance(password, str):
                    return "Invalid password, must be a string"
                if not isinstance(pin, int):
                    return "Invalid pin, must be an integer"
                user["name"] = name
                user["email"] = email
                user["password"] = password
                user["transaction_pin"] = pin
                user["last_modified"] = str(datetime.date.today())
    
                self.save(banks)
                return user
        return None
      
    def delete_user(self, user_id: str):
            """Delete a user by id"""
            if not isinstance(user_id, str):
                return "Invalid user_id, must be a string"
            banks = self.read()
            for bank in banks.values():
                if user_id in bank['users']:
                    user = bank['users'][user_id]
                    bank['users'].pop(user_id)
                    if user["state"] == AccountState.ACTIVE:
                        user["state"] = AccountState.CLOSED
                        user["state_change_date"] = str(datetime.date.today())
                        user["state_change_time"] = str(datetime.datetime.now().time())
                    self.save(banks)
                    return True
            return False

    def list_users(self, bank_id: str):
            """List all users in a bank"""
            if not isinstance(bank_id, str):
                return "Invalid bank_id, must be a string"
            banks = self.read()
            bank = banks.get(bank_id)
            if bank:
                return "\n".join(
                    f"{user['id']:<10} {user['name']} {user['state']}"
                    for user in bank['users'].values()
                )
            return None

    def read_user(self, user_id: str):
            """Read a user by id"""
            if not isinstance(user_id, str):
                return "Invalid user_id, must be a string"
            banks = self.read()
            for bank in banks.values():
                user = bank['users'].get(user_id)
                if user:
                    return user
            return None


    # send and receive money
class TransactionOperation(UserOperation):
        def __init__(self):
            super().__init__()

        def transfer(self, amount: int, sender: str, receiver: str, pin: int, description: str):
            """Transfer money between accounts"""
            if not isinstance(amount, int) or amount <= 0:
                return "Invalid amount, must be a positive integer"
            if not isinstance(sender, str):
                return "Invalid sender, must be a string"
            if not isinstance(receiver, str):
                return "Invalid receiver, must be a string"
            if not isinstance(pin, int):
                return "Invalid pin, must be an integer"
            if not isinstance(description, str):
                return "Invalid description, must be a string"

            banks = self.read()
            sender_account = banks.get(sender)
            receiver_account = banks.get(receiver)
            if sender_account is None or receiver_account is None:
                return "Account not found."
            if sender == receiver:
                return "Cannot transfer to the same account."
            if sender_account["transaction_pin"] != pin:
                return "Invalid pin."
            if sender_account["state"] != AccountState.ACTIVE:
                return "Sender's account is not active."
            if receiver_account["state"] != AccountState.ACTIVE:
                return "Receiver's account is not active."
            if sender_account["balance"] < amount:
                return "Insufficient balance."
            if sender_account["state"] == AccountState.FROZEN:
                return "Sender's account is frozen."
            if receiver_account["state"] == AccountState.FROZEN:
                return "Receiver's account is frozen."

            sender_account["balance"] = math.floor(sender_account["balance"] - amount)
            receiver_account["balance"] = math.floor(receiver_account["balance"] + amount)
            transaction_id = str(uuid.uuid4())
            transaction = {
                "type": "deposit",
                "amount": amount,
                "date": str(datetime.date.today()),
                "time": str(datetime.datetime.now().time()),
                "TransactionDetails": f"Deposited {amount} from {sender_account['name']}",
                "TransactionType": "credit",
                "TransactionDescription": description,
            }
            sender_account["transaction_history"].append(transaction)
            receiver_account["transaction_history"].append(transaction)
            self.save(banks)
            return f"Transaction successful. Transaction ID: {transaction_id}"

        def withdraw(self, amount: int, account_id: str, pin: int, description: str):
            """Withdraw money from an account"""
            if not isinstance(amount, int) or amount <= 0:
                return "Invalid amount, must be a positive integer"
            if not isinstance(account_id, str):
                return "Invalid account_id, must be a string"
            if not isinstance(pin, int):
                return "Invalid pin, must be an integer"
            if not isinstance(description, str):
                return "Invalid description, must be a string"

            banks = self.read()
            account = banks.get(account_id)
            if account is None:
                return "Account not found."
            if account["transaction_pin"] != pin:
                return "Invalid pin."
            if account["state"] != AccountState.ACTIVE:
                return "Account is not active."
            if account["balance"] < amount:
                return "Insufficient balance."
            if account["state"] == AccountState.FROZEN:
                return "Account is frozen."

            account["balance"] = math.floor(account["balance"] - amount)
            transaction_id = str(uuid.uuid4())
            transaction = {
                "type": "withdrawal",
                "amount": amount,
                "date": str(datetime.date.today()),
                "time": str(datetime.datetime.now().time()),
                "TransactionDetails": f"Withdrawn {amount} from {account['name']}",
                "TransactionType": "debit",
                "TransactionDescription": description,
            }
            account["transaction_history"].append(transaction)
            self.save(banks)
            return f"Transaction successful. Transaction ID: {transaction_id}"

        def freeze(self, account_id: str, pin: int):
            """Freeze an account"""
            if not isinstance(account_id, str):
                return "Invalid account_id, must be a string"
            if not isinstance(pin, int):
                return "Invalid pin, must be an integer"

            banks = self.read()
            account = banks.get(account_id)
            if account is None:
                return "Account not found."
            if account["transaction_pin"] != pin:
                return "Invalid pin."
            if account["state"] != AccountState.ACTIVE:
                return "Account is not active."

            account["state"] = AccountState.FROZEN
            account["state_change_date"] = str(datetime.date.today())
            account["state_change_time"] = str(datetime.datetime.now().time())
            self.save(banks)
            return f"Account {account_id} has been frozen."

        def unfreeze(self, account_id: str, pin: int):
            """Unfreeze an account"""
            if not isinstance(account_id, str):
                return "Invalid account_id, must be a string"
            if not isinstance(pin, int):
                return "Invalid pin, must be an integer"

            banks = self.read()
            account = banks.get(account_id)
            if account is None:
                return "Account not found."
            if account["transaction_pin"] != pin:
                return "Invalid pin."
            if account["state"] != AccountState.FROZEN:
                return "Account is not frozen."

            account["state"] = AccountState.ACTIVE
            account["state_change_date"] = str(datetime.date.today())
            account["state_change_time"] = str(datetime.datetime.now().time())
            self.save(banks)
            return f"Account {account_id} has been unfrozen."
        
        def close(self, account_id: str, pin: int):
            """Close an account"""
            if not isinstance(account_id, str):
                return "Invalid account_id, must be a string"
            if not isinstance(pin, int):
                return "Invalid pin, must be an integer"

            banks = self.read()
            account = banks.get(account_id)
            if account is None:
                return "Account not found."
            if account["transaction_pin"] != pin:
                return "Invalid pin."
            if account["state"] == AccountState.CLOSED:
                return "Account is already closed."

            account["state"] = AccountState.CLOSED
            account["state_change_date"] = str(datetime.date.today())
            account["state_change_time"] = str(datetime.datetime.now().time())
            self.save(banks)
            return f"Account {account_id} has been closed."
        
        def archive(self, account_id: str, pin: int):
            """Archive an account"""
            if not isinstance(account_id, str):
                return "Invalid account_id, must be a string"
            if not isinstance(pin, int):
                return "Invalid pin, must be an integer"

            banks = self.read()
            account = banks.get(account_id)
            if account is None:
                return "Account not found."
            if account["transaction_pin"] != pin:
                return "Invalid pin."
            if account["state"] == AccountState.ARCHIVED:
                return "Account is already archived."

            account["state"] = AccountState.ARCHIVED
            account["state_change_date"] = str(datetime.date.today())
            account["state_change_time"] = str(datetime.datetime.now().time())
            self.save(banks)
            return f"Account {account_id} has been archived."
        
        def unarchive(self, account_id: str, pin: int):
            """Unarchive an account"""
            if not isinstance(account_id, str):
                return "Invalid account_id, must be a string"
            if not isinstance(pin, int):
                return "Invalid pin, must be an integer"

            banks = self.read()
            account = banks.get(account_id)
            if account is None:
                return "Account not found."
            if account["transaction_pin"] != pin:
                return "Invalid pin."
            if account["state"] == AccountState.ACTIVE:
                return "Account is already active."

            account["state"] = AccountState.ACTIVE
            account["state_change_date"] = str(datetime.date.today())
            account["state_change_time"] = str(datetime.datetime.now().time())
            self.save(banks)
            return f"Account {account_id} has been unarchived."
        
        def list_accounts(self, pin: int):
            """List accounts"""
            if not isinstance(pin, int):
                return "Invalid pin, must be an integer"

            banks = self.read()
            accounts = []
            for account in banks.values():
                if account["transaction_pin"] == pin:
                    accounts.append(account)
            return accounts

        def list_transactions(self, account_id: str, pin: int):
            """List transactions"""
            if not isinstance(account_id, str):
                return "Invalid account_id, must be a string"
            if not isinstance(pin, int):
                return "Invalid pin, must be an integer"

            banks = self.read()
            account = banks.get(account_id)
            if account is None:
                return "Account not found."
            if account["transaction_pin"] != pin:
                return "Invalid pin."
            return account["transaction_history"]

        def list_transactions_between(self, account_id: str, start_date: str, end_date: str, pin: int):
            """List transactions between two dates"""
            if not isinstance(account_id, str):
                return "Invalid account_id, must be a string"
            if not isinstance(start_date, str):
                return "Invalid start_date, must be a string"
            if not isinstance(end_date, str):
                return "Invalid end_date, must be a string"
            if not isinstance(pin, int):
                return "Invalid pin, must be an integer"

            banks = self.read()
            account = banks.get(account_id)
            if account is None:
                return "Account not found."
            if account["transaction_pin"] != pin:
                return "Invalid pin."
            return account["transaction_history"]
