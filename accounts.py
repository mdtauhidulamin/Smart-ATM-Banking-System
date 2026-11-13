"""Account models, inheritance, and exact money validation."""
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation


def money(value):
    try:
        amount = Decimal(str(value))
        if not amount.is_finite() or amount <= 0:
            raise ValueError('Amount must be positive and finite.')
        if amount > Decimal('1000000000'):
            raise ValueError('Amount is above the demo limit.')
        if amount != amount.quantize(Decimal('0.01')):
            raise ValueError('Use at most two decimal places.')
        return amount.quantize(Decimal('0.01'))
    except InvalidOperation as exc:
        raise ValueError('Enter a valid monetary amount.') from exc


@dataclass
class BankAccount:
    account_id: str
    owner: str
    balance: Decimal
    pin_hash: str
    account_type: str = 'standard'

    def deposit(self, amount):
        self.balance += money(amount)

    def withdraw(self, amount):
        amount = money(amount)
        if amount > self.balance:
            raise ValueError('Insufficient balance.')
        self.balance -= amount

    def description(self):
        return 'Standard account'

    def to_dict(self):
        return dict(account_id=self.account_id, owner=self.owner,
                    balance=str(self.balance), pin_hash=self.pin_hash,
                    account_type=self.account_type)


@dataclass
class SavingsAccount(BankAccount):
    account_type: str = 'savings'

    def description(self):
        return 'Savings account: no overdraft'


@dataclass
class CurrentAccount(BankAccount):
    account_type: str = 'current'

    def description(self):
        return 'Current account: no overdraft in this demo'


def account_from_dict(record):
    classes = {'standard': BankAccount, 'savings': SavingsAccount,
               'current': CurrentAccount}
    fields = dict(record)
    fields['balance'] = Decimal(fields['balance'])
    return classes[fields['account_type']](**fields)
