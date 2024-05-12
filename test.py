from practice.fileStorage import FileOperation
from practice.bank import BankOperation
from practice.transaction import TransactionOperation
from practice.user import UserOperation

storage = FileOperation("banks.json")
register = BankOperation()
# createBank = register.create_bank(
#     "SBI", "Hyderabad", "Hyderabad", "SBI000001", "9876543210", "9f0Xt@example.com", ["Savings", "Current"]
# )
# register.update_bank("e0eba8ce-6b36-417a-9f73-c30482516047",name="SBI", ifsc="SBI007002")

# createUser = UserOperation()
# createUser.create_user(
#     "b2701d1b-6a26-4e95-8659-a17caad89a0d", "Savings", "Rajesh", "9f0Xt@example.com", "12345", 123
# )

# transact = TransactionOperation()
# print(transact.transfer("618d134c-8ef7-4523-a7fc-dbc034c2bf39","d28d014b-c9cb-442b-a6a9-85ac5b0d31e1", 200, 3860163361, 3102958558, 12345, "Rajesh"))
