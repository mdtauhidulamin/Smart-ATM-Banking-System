"""SQLite persistence: accounts and journal are saved atomically."""
import sqlite3
from pathlib import Path

DEFAULT_DATABASE = Path(__file__).with_name('atm_data.sqlite3')


class Storage:
    def __init__(self, path=DEFAULT_DATABASE):
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute('PRAGMA foreign_keys = ON')
        with self.connection:
            self.connection.execute('''CREATE TABLE IF NOT EXISTS accounts (
                account_id TEXT PRIMARY KEY, owner TEXT NOT NULL,
                balance TEXT NOT NULL, pin_hash TEXT NOT NULL,
                account_type TEXT NOT NULL)''')
            self.connection.execute('''CREATE TABLE IF NOT EXISTS transactions (
                transaction_id TEXT PRIMARY KEY, account_id TEXT NOT NULL,
                kind TEXT NOT NULL, amount TEXT NOT NULL,
                balance_after TEXT NOT NULL, timestamp TEXT NOT NULL,
                note TEXT NOT NULL,
                FOREIGN KEY(account_id) REFERENCES accounts(account_id))''')

    def load_accounts(self):
        return [dict(row) for row in self.connection.execute(
            'SELECT * FROM accounts ORDER BY account_id')]

    def commit(self, accounts, transactions=()):
        """Write every part of a transfer in one database transaction."""
        with self.connection:
            for account in accounts:
                self.connection.execute('''INSERT INTO accounts VALUES (
                    :account_id, :owner, :balance, :pin_hash, :account_type)
                    ON CONFLICT(account_id) DO UPDATE SET
                    owner=excluded.owner, balance=excluded.balance,
                    pin_hash=excluded.pin_hash,
                    account_type=excluded.account_type''', account.to_dict())
            for entry in transactions:
                self.connection.execute('''INSERT INTO transactions VALUES (
                    :transaction_id, :account_id, :kind, :amount,
                    :balance_after, :timestamp, :note)''', entry)

    def history(self, account_id, limit=10):
        rows = self.connection.execute('''SELECT * FROM transactions
            WHERE account_id = ? ORDER BY timestamp DESC, rowid DESC LIMIT ?''',
            (account_id, limit))
        return [dict(row) for row in rows]

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
