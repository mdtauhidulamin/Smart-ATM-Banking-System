"""Run with python main.py. Python standard library only.

Educational single-user ATM simulator; not a production banking service.
Use invented account information. Do not upload atm_data.sqlite3 to GitHub.
"""
from getpass import getpass
from pathlib import Path
import sqlite3
from bank import Bank
from security import prompt_new_pin
from storage import Storage
from transactions import print_statement, export_statement


def account_menu(bank, account_id):
    while True:
        account = bank.get_account(account_id)
        print(f'\nWelcome, {account.owner} | {account.description()}')
        print('1. Balance  2. Deposit  3. Withdraw  4. Transfer')
        print('5. History  6. Export CSV  7. Change PIN  0. Log out')
        choice = input('Choose: ').strip()
        try:
            if choice == '0':
                return
            if choice == '1':
                print(f'Balance: {account.balance:,.2f}')
            elif choice == '2':
                balance = bank.deposit(account_id, input('Deposit amount: '))
                print(f'Deposit successful. Balance: {balance:,.2f}')
            elif choice == '3':
                balance = bank.withdraw(account_id, input('Withdraw amount: '))
                print(f'Withdrawal successful. Balance: {balance:,.2f}')
            elif choice == '4':
                receiver = input('Receiver account ID: ').strip().upper()
                amount = input('Transfer amount: ')
                balance = bank.transfer(account_id, receiver, amount)
                print(f'Transfer successful. Balance: {balance:,.2f}')
            elif choice == '5':
                print_statement(bank.storage.history(account_id, 20))
            elif choice == '6':
                entries = bank.storage.history(account_id, 10000)
                path = Path(__file__).with_name(f'statement_{account_id}.csv')
                print('Exported:', export_statement(entries, path))
            elif choice == '7':
                old_pin = getpass('Current PIN: ')
                bank.change_pin(account_id, old_pin, prompt_new_pin())
                print('PIN updated.')
            else:
                print('Choose a listed option.')
        except (ValueError, OSError, sqlite3.Error) as error:
            print('Operation failed:', error)


def main():
    print('SMART ATM BANKING SYSTEM — Educational Demo')
    with Storage() as storage:
        bank = Bank(storage)
        while True:
            print('\n1. Create account  2. Log in  0. Exit')
            choice = input('Choose: ').strip()
            try:
                if choice == '0':
                    print('Thank you. Goodbye!')
                    return
                if choice == '1':
                    owner = input('Account holder name: ')
                    kind = input('Type (savings/current): ').strip().lower()
                    account = bank.create_account(owner, prompt_new_pin(), kind)
                    print('Account created. Save your account ID:', account.account_id)
                elif choice == '2':
                    account_id = input('Account ID: ').strip().upper()
                    bank.login(account_id, getpass('PIN: '))
                    account_menu(bank, account_id)
                else:
                    print('Choose a listed option.')
            except (ValueError, OSError, sqlite3.Error) as error:
                print('Operation failed:', error)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print('\nSession ended.')
