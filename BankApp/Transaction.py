#!/usr/bin/env python3

import uuid
from BankApp.BankUser import UserOperations
from datetime import datetime, timezone


class TransactionOperations(UserOperations):

    def __init__(self, db_manager):
        self.db_manager = db_manager

    def transfer_money(self, sender_id, receiver_account_number, receiver_bank_name, amount, description):
        with self.db_manager.pool.item() as conn:
            with conn.cursor() as cursor:
                try:
                    # Begin a transaction
                    conn.begin()

                    # Retrieve sender details
                    sender = self._get_user_details(cursor, sender_id)

                    # Validate sender
                    self._validate_sender(sender, amount)

                    if sender_id == receiver_account_number:
                        raise ValueError("You can't transfer money to yourself")

                    # Retrieve receiver details using bank name and account number
                    receiver = self._get_receiver_details(
                        cursor, receiver_bank_name, receiver_account_number)

                    # Validate receiver
                    self._validate_receiver(receiver)

                    # Perform the transfer
                    new_sender_balance = sender['balance'] - amount
                    new_receiver_balance = receiver['balance'] + amount

                    # Update balances
                    self._update_sender_balance(cursor, sender, new_sender_balance)
                    self._update_receiver_balance(
                        cursor, receiver, new_receiver_balance)

                    # Insert transaction history
                    self._insert_transaction_history(
                        cursor, sender, receiver, amount, description)

                    # Commit the transaction
                    conn.commit()
                    return "Money transfer successful"
                except Exception as e:
                    # Rollback in case of any error
                    conn.rollback()
                    raise e

    def _get_user_details(self, cursor, user_identifier):
        """Retrieve user details."""
        cursor.execute(
            "SELECT * FROM users WHERE username = ? OR user_account_number = ?",
            (user_identifier, user_identifier)
        )
        return cursor.fetchone()

    def _validate_sender(self, sender, amount):
        """Validate sender details."""
        if not sender:
            raise ValueError("Invalid sender")
        if sender['balance'] < amount:
            raise ValueError("Insufficient balance")
        if sender['status'] != 'active':
            raise ValueError("Account under review")
        if sender['status'] == 'Suspended':
            raise ValueError("Account suspended")
        if sender['status'] == 'Frozen':
            raise ValueError("Account frozen")
        return sender

    def _get_receiver_details(self, cursor, bank_name, account_number):
        """Retrieve receiver details."""
        cursor.execute(
            "SELECT * FROM users WHERE bank_id = (SELECT bank_registration_number FROM banks WHERE bank_name = ?) AND user_account_number = ?",
            (bank_name, account_number)
        )
        return cursor.fetchone()

    def _validate_receiver(self, receiver):
        """Validate receiver details."""
        if not receiver:
            raise ValueError("Receiver not found")
        if receiver['status'] != 'active':
            raise ValueError("Receiver account under review")
        if receiver['status'] == 'Suspended':
            raise ValueError("Receiver account suspended")
        if receiver['status'] == 'Frozen':
            raise ValueError("Receiver account frozen")
        return receiver

    def _update_sender_balance(self, cursor, sender, new_balance):
        """Update sender's balance."""
        cursor.execute(
            "UPDATE users SET balance = ? WHERE username = ? OR user_account_number = ?",
            (new_balance, sender['username'], sender['user_account_number'])
        )

    def _update_receiver_balance(self, cursor, receiver, new_balance):
        """Update receiver's balance."""
        cursor.execute(
            "UPDATE users SET balance = ? WHERE username = ? OR user_account_number = ?",
            (new_balance, receiver['username'],
             receiver['user_account_number'])
        )

    def _insert_transaction_history(self, cursor, sender, receiver, amount, description):
        """Insert transaction history."""
        sender_transaction_id = str(uuid.uuid4())
        receiver_transaction_id = str(uuid.uuid4())
        current_datetime = datetime.now(timezone.utc).isoformat()
        sender_transaction_description = description + \
            ' to ' + receiver['username']
        receiver_transaction_description = 'Transfer from ' + \
            sender['username']

        cursor.execute(
            "INSERT INTO transactions (transaction_id, sender_user_id, receiver_user_id, amount, description, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (sender_transaction_id, sender['user_account_number'], receiver['user_account_number'], -
             amount, sender_transaction_description, current_datetime)
        )

        cursor.execute(
            "INSERT INTO transactions (transaction_id, sender_user_id, receiver_user_id, amount, description, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (receiver_transaction_id, sender['user_account_number'], receiver['user_account_number'],
             amount, receiver_transaction_description, current_datetime)
        )

    def deposit_money(self, user_id, amount):
        with self.db_manager.pool.item() as conn:
            with conn.cursor() as cursor:
                try:
                    # Begin a transaction
                    conn.begin()

                    # Retrieve user details
                    cursor.execute(
                        "SELECT * FROM users WHERE username = ? OR account_number = ?",
                        (user_id, user_id)
                    )
                    user = cursor.fetchone()

                    # Check if user is valid and has an active status
                    if not user:
                        raise ValueError("User not found")
                    if user['status'] != 'active':
                        raise ValueError("Account under review")

                    # Perform the deposit
                    new_balance = user['balance'] + amount
                    cursor.execute(
                        "UPDATE users SET balance = ? WHERE username = ? OR user_account_number = ?",
                        (new_balance, user['username'],
                         user['user_account_number'])
                    )

                    # Insert transaction history
                    transaction_id = str(uuid.uuid4())
                    current_datetime = datetime.now(timezone.utc).isoformat()
                    transaction_type = 'credit'
                    transaction_description = 'Deposit'
                    cursor.execute(
                        "INSERT INTO transactions (transaction_id, user_id, amount, type, description, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                        (transaction_id, user['user_account_number'], amount,
                         transaction_type, transaction_description, current_datetime)
                    )

                    # Commit the transaction
                    conn.commit()
                    return "Deposit successful"
                except Exception as e:
                    # Rollback in case of any error
                    conn.rollback()
                    raise e

    def withdraw_money(self, user_id, amount):
        with self.db_manager.pool.item() as conn:
            with conn.cursor() as cursor:
                try:
                    # Begin a transaction
                    conn.begin()

                    # Retrieve user details
                    cursor.execute(
                        "SELECT * FROM users WHERE username = ? OR account_number = ?",
                        (user_id, user_id)
                    )
                    user = cursor.fetchone()

                    # Check if user is valid and has an active status
                    if not user:
                        raise ValueError("User not found")
                    if user['status'] != 'active':
                        raise ValueError(
                            "Account under review, please contact support")

                    # Perform the withdrawal
                    new_balance = user['balance'] - amount
                    cursor.execute(
                        "UPDATE users SET balance = ? WHERE username = ? OR user_account_number = ?",
                        (new_balance, user['username'],
                         user['user_account_number'])
                    )

                    # Insert transaction history
                    transaction_id = str(uuid.uuid4())
                    current_datetime = datetime.now(timezone.utc).isoformat()
                    transaction_type = 'debit'
                    transaction_description = 'Withdrawal'
                    cursor.execute(
                        "INSERT INTO transactions (transaction_id, user_id, amount, type, description, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                        (transaction_id, user['user_account_number'], -amount,
                         transaction_type, transaction_description, current_datetime)
                    )

                    # Commit the transaction
                    conn.commit()
                    return "Withdrawal successful"
                except Exception as e:
                    # Rollback in case of any error
                    conn.rollback()
                    raise e
