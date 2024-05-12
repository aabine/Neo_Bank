import os
import datetime
import json
import uuid

class BankOperation:
    def __init__(self):
        self.banks = self.read()

    def create_bank(self, name, location, branch, ifsc, contact, email, account_type):
        bank = {
            "id": str(uuid.uuid4())[:15],
            "creation_date": str(datetime.date.today()),
            "creation_time": str(datetime.datetime.now().time()),
            "last_modified": str(datetime.date.today()),
            "name": name,
            "location": location,
            "branch": branch,
            "ifsc": ifsc,
            "contact": contact,
            "email": email,
            "account_type": account_type,
            "users": {},
        }
        self.banks[bank["id"]] = bank
        self.save_data(self.banks)
        return bank

    def update_bank(self, bank_id, name, location, branch, ifsc, contact, email, account_type):
        bank = self.banks.get(bank_id)
        if bank:
            bank["name"] = name
            bank["location"] = location
            bank["branch"] = branch
            bank["ifsc"] = ifsc
            bank["contact"] = contact
            bank["email"] = email
            bank["account_type"] = account_type
            bank["last_modified"] = str(datetime.date.today())
            self.save_data(self.banks)
            return bank
        return None

    def delete_bank(self, bank_id):
        return self.banks.pop(bank_id, None)

    def list_banks(self):
        return "\n".join(
            f"{bank['id']:<10} {bank['name']}"
            for bank in self.banks.values()
        )

    def read_bank(self, bank_id):
        return self.banks.get(bank_id)

    def save_data(self, data):
        try:
            with open('bank.json', 'w') as f:
                json.dump(data, f, indent=4)
        except OSError as e:
            print(f"Error saving bank data: {e}")

    def read(self):
        if not os.path.exists('bank.json'):
            return {}
        try:
            with open('bank.json', 'r') as f:
                return json.load(f)
        except (OSError, IOError) as e:
            print(f"Error reading bank data: {e}")
        except json.JSONDecodeError as e:
            print(f"Error parsing bank data: {e}")
        return {}

    def close(self):
        self.save_data(self.banks)


#Example usage

register = BankOperation()
register.create_bank("Bank of India", "Mumbai", "Mumbai Central", "BOI0000000", "1234567890", "j7t0w@example.com", "Savings")
created_bank = register.read_bank("id")
print(created_bank)
