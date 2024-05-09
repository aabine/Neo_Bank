import unittest
from unittest.mock import patch
from bank import BankOperation  # Replace with the actual module where BankOperation is defined
import json



def test_create_bank():
    op = BankOperation()
    bank_details = {
        "name": "Test Bank",
        "location": "Mumbai",
        "branch": "Andheri",
        "ifsc": "TTSB00001",
        "contact": "8888888888",
        "email": "test@bank.com",
        "account_types": ["savings", "current"]
    }
    bank = op.create_bank(**bank_details)

    assert bank["name"] == "Test Bank"
    assert len(op.read()) == 1
