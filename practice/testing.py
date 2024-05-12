import uuid
import datetime
import json
import logging

class BankDataStorage:
    @staticmethod
    def save_to_file(data, filename='bank.json'):
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
        except OSError as e:
            logging.error(f"Error saving bank data: {e}")
            return False
        return True

    @staticmethod
    def read_from_file(filename='bank.json'):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error("Bank data file not found.")
            return {}
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing bank data: {e}")
            return {}

class BankOperation:
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

    def create_bank(self):
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
        return bank

    def update_bank(self, bank_data, **kwargs):
        bank_data.update(kwargs)
        bank_data["last_modified"] = str(datetime.date.today())
        return bank_data

    def delete_bank(self, bank_data):
        return None  # Placeholder for deletion logic

    def list_banks(self, bank_data):
        return "\n".join(
            f"{bank['id']:<10} {bank['name']}"
            for bank in bank_data.values()
        )

    def read_bank(self, bank_data, bank_id):
        return bank_data.get(bank_id)

# Example usage:
bank_storage = BankDataStorage()
bank_data = bank_storage.read_from_file()

bank_op = BankOperation("Example Bank", "Location", "Branch", "IFSC", "LLC", "Contact", "Email", "AccountType")
new_bank = bank_op.create_bank()
bank_data[new_bank['id']] = new_bank

if bank_storage.save_to_file(bank_data):
    print("Bank data saved successfully.")
else:
    print("Error saving bank data.")


