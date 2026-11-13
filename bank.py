"""Bank service coordinating accounts, authentication, and transfers."""
from decimal import Decimal
from uuid import uuid4
from accounts import SavingsAccount, CurrentAccount, account_from_dict, money
from security import LoginGuard, hash_pin, verify_pin
from transactions import make_entry


class Bank:
    def __init__(self, storage):
        self.storage = storage
        self.guard = LoginGuard()

    def get_account(self, account_id):
        for record in self.storage.load_accounts():
            if record['account_id'] == account_id:
                return account_from_dict(record)
        raise ValueError('Account not found.')

    def create_account(self, owner, pin, kind='savings'):
        owner = owner.strip()
        if not 2 <= len(owner) <= 80:
            raise ValueError('Name must contain 2 to 80 characters.')
        classes = {'savings': SavingsAccount, 'current': CurrentAccount}
        if kind not in classes:
            raise ValueError('Choose savings or current.')
        account = classes[kind](uuid4().hex[:12].upper(), owner,
                                Decimal('0.00'), hash_pin(pin))
        self.storage.commit([account])
        return account

    def login(self, account_id, pin):
        account = self.get_account(account_id)
        self.guard.authenticate(account_id, pin, account.pin_hash)
        return account

    def deposit(self, account_id, amount):
        account = self.get_account(account_id)
        amount = money(amount)
        account.deposit(amount)
        self.storage.commit([account], [make_entry(account, 'DEPOSIT', amount)])
        return account.balance

    def withdraw(self, account_id, amount):
        account = self.get_account(account_id)
        amount = money(amount)
        account.withdraw(amount)
        self.storage.commit([account], [make_entry(account, 'WITHDRAW', amount)])
        return account.balance

    def transfer(self, sender_id, receiver_id, amount):
        if sender_id == receiver_id:
            raise ValueError('Cannot transfer to the same account.')
        sender = self.get_account(sender_id)
        receiver = self.get_account(receiver_id)
        amount = money(amount)
        sender.withdraw(amount)
        receiver.deposit(amount)
        entries = [make_entry(sender, 'TRANSFER_OUT', amount, f'To {receiver_id}'),
                   make_entry(receiver, 'TRANSFER_IN', amount, f'From {sender_id}')]
        self.storage.commit([sender, receiver], entries)
        return sender.balance

    def change_pin(self, account_id, old_pin, new_pin):
        account = self.get_account(account_id)
        if not verify_pin(old_pin, account.pin_hash):
            raise ValueError('Current PIN is incorrect.')
        account.pin_hash = hash_pin(new_pin)
        self.storage.commit([account])
