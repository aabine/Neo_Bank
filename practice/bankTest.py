
import datetime
import json
import logging
from pathlib import Path
import uuid


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
            "account_types": account_types,
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
        if bank_id in banks:
            del banks[bank_id]
            self.save(banks)
            return True
        return False

    def list_banks(self):
        banks = self.read()
        return "\n".join(
            f"{bank['id']:<10} {bank['name']}"
            for bank in banks.values()
        )

    def read_bank(self, bank_id):
        banks = self.read()
        return banks.get(bank_id)
    


class BankOperation:
    Bank_data = {}

    def __init__(self, BankName, BankLocation, BankBranch, BankIFSC, LLCNumber, BankContact, BankEmail, BankAccountType):
        self.bankId = str(uuid.uuid4())[:15]
        self.BankName = BankName
        self.BankLocation = BankLocation
        self.BankBranch = BankBranch
        self.BankIFSC = BankIFSC
        self.LLCNumber = LLCNumber
        self.BankContact = BankContact
        self.BankEmail = BankEmail
        self.BankAccountType = BankAccountType

    def createBank(self):
        bank = {
            "id": self.bankId,
            "creation_date": str(datetime.date.today()),
            "creation_time": str(datetime.datetime.now().time()),
            "last_modified": str(datetime.date.today()),
            "name": self.BankName,
            "location": self.BankLocation,
            "branch": self.BankBranch,
            "ifsc": self.BankIFSC,
            "contact": self.BankContact,
            "email": self.BankEmail,
            "account_type": self.BankAccountType,
            "users": {},
        }
        BankOperation.Bank_data[self.bankId] = bank
        return bank

    def updateBank(self, bankId, name, location, branch, ifsc, contact, email, account_type):
        bank = BankOperation.Bank_data.get(bankId)
        if bank:
            bank["name"] = name
            bank["location"] = location
            bank["branch"] = branch
            bank["ifsc"] = ifsc
            bank["contact"] = contact
            bank["email"] = email
            bank["account_type"] = account_type
            bank["last_modified"] = str(datetime.date.today())
            return bank
        return None
    
    def deleteBank(self, bankId):
        return BankOperation.Bank_data.pop(bankId, None)

    def listBanks(self):
        return "\n".join(
            f"{bank['id']:<10} {bank['name']}"
            for bank in BankOperation.Bank_data.values()
        )

    def readBank(self, bankId):
        return BankOperation.Bank_data.get(bankId)

    def saveBank(self):
        try:
            with open('bank.json', 'w') as f:
                json.dump(BankOperation.Bank_data, f, indent=4)
        except OSError as e:
            logging.error(f"Error saving {self.banks_file}: {e}")

    def read(self):
        try:
            with open('bank.json', 'r') as f:
                return json.load(f)
        except (OSError, IOError) as e:
            logging.error(f"Error reading {self.banks_file}: {e}")
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing {self.banks_file}: {e}")
        return {}

    def save(self, data):
        try:
            with open('bank.json', 'w') as f:
                json.dump(data, f, indent=4)
        except OSError as e:
            logging.error(f"Error saving {self.banks_file}: {e}")

    def close(self):
        self.save(BankOperation.Bank_data)

    def __del__(self):
        self.close()

