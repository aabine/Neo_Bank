from decimal import Decimal
import datetime
import uuid
from practice.fileStorage import FileOperation
from practice.user import AccountState, AccountStateEncoder

class TransactionOperation(FileOperation):
    def __init__(self):
        super().__init__("banks.json")



    def transfer(self, sender_bank_id: str, receiver_bank_id: str, amount: Decimal, sender: int, receiver: int, pin: int, description: str):
        if sender == receiver:
            return "Cannot transfer to the same account."
        
        # Read the complete set of accounts from the JSON file
        banks = self.read()
        
        # Get the individual accounts
        sender_account = banks[sender_bank_id].get(str(sender))
        receiver_account = banks[receiver_bank_id].get(str(receiver))

        print(
            f"Sender account: {sender_account}, Receiver account: {receiver_account}"
        )

        # Validate the accounts
        if sender_account is None:
            return "Sender's account not found."
        if receiver_account is None:
            return "Receiver's account not found."
        if sender_account["state"] not in [AccountState.ACTIVE]:
            return "Sender's account is not valid for transactions."
        if receiver_account["state"] not in [AccountState.ACTIVE]:
            return "Receiver's account is not valid for transactions."
        if sender_account["transaction_pin"] != pin:
            return "Invalid pin."
        if sender_account["balance"] < amount:
            return "Insufficient balance."

        # Perform the transfer
        sender_account["balance"] -= amount
        receiver_account["balance"] += amount

        sender_transaction_id = str(uuid.uuid4())
        receiver_transaction_id = str(uuid.uuid4())
        now = datetime.datetime.now()

        # Create the sender's transaction
        sender_transaction = {
            "transaction_id": sender_transaction_id,
            "type": "withdrawal",
            "amount": amount,
            "timestamp": now.isoformat(),
            "TransactionDetails": f"Withdrawn {amount} to {receiver}",
            "TransactionType": "debit",
            "TransactionDescription": description,
        }
        sender_account["transaction_history"].append(sender_transaction)

        # Create the receiver's transaction
        receiver_transaction = {
            "transaction_id": receiver_transaction_id,
            "type": "deposit",
            "amount": amount,
            "timestamp": now.isoformat(),
            "TransactionDetails": f"Deposited {amount} from {sender}",
            "TransactionType": "credit",
            "TransactionDescription": description,
        }
        receiver_account["transaction_history"].append(receiver_transaction)

        # Update the accounts in the 'banks' dictionary
        banks[str(sender)] = sender_account
        banks[str(receiver)] = receiver_account

        # Save the updated dictionary back to the JSON file
        self.save(banks, encoder=AccountStateEncoder)

        return f"Transaction successful. Sender Transaction ID: {sender_transaction_id}, Receiver Transaction ID: {receiver_transaction_id}"
    def withdraw(self, amount: Decimal, account_id: int, pin: int, description: str):
        account, banks = self._get_account(account_id)
        if account["state"] not in [AccountState.ACTIVE]:
            return "Account is not valid for transactions."
        if account["transaction_pin"] != pin:
            return "Invalid pin."
        if account["balance"] < amount:
            return "Insufficient balance."

        account["balance"] -= amount

        transaction_id = str(uuid.uuid4())
        now = datetime.datetime.now()

        transaction = {
            "transaction_id": transaction_id,
            "type": "withdrawal",
            "amount": amount,
            "timestamp": now.isoformat(),
            "TransactionDetails": f"Withdrawn {amount} from {account['name']}",
            "TransactionType": "debit",
            "TransactionDescription": description,
        }
        account["transaction_history"].append(transaction)

        banks[str(account_id)] = account
        self.save(banks, encoder=AccountStateEncoder)

        return f"Transaction successful. Transaction ID: {transaction_id}"

