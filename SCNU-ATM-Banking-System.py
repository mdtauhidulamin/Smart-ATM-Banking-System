from datetime import date
import numpy as np
import matplotlib.pyplot as plt


class BankAccount:
    def __init__(self, account_number, pin, owner_name, balance):
        self.account_number = account_number
        self.pin = pin
        self.owner_name = owner_name
        self.balance = balance
        self.transactions = []

    def save_transaction_to_file(self, transaction_type, amount):
        today = date.today()

        file = open("transactions.txt", "a")

        file.write(
            self.account_number + ","
            + self.owner_name + ","
            + transaction_type + ","
            + str(amount) + ","
            + str(today) + "\n"
        )

        file.close()

    def check_balance(self):
        print("Current Balance:", self.balance)

    def deposit(self, amount):
        if amount > 0:
            self.balance = self.balance + amount

            self.transactions.append(("Deposit", amount))

            self.save_transaction_to_file("Deposit", amount)

            print("Deposit Successful!")
            print("New Balance:", self.balance)
        else:
            print("Invalid Amount!")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance = self.balance - amount

            self.transactions.append(("Withdraw", amount))

            self.save_transaction_to_file("Withdraw", amount)

            print("Withdraw Successful!")
            print("Remaining Balance:", self.balance)
        else:
            print("Insufficient Balance!")

    def show_transactions(self):
        print("\n===== Transaction History =====")

        if len(self.transactions) == 0:
            print("No transactions yet.")
        else:
            for transaction in self.transactions:
                print(transaction[0], ":", transaction[1])


class SavingsAccount(BankAccount):
    def add_interest(self):
        interest = self.balance * 0.05

        self.balance = self.balance + interest

        self.transactions.append(("Interest Added", interest))

        self.save_transaction_to_file("Interest Added", interest)

        print("Interest Added:", interest)
        print("New Balance:", self.balance)


class CurrentAccount(BankAccount):
    def withdraw(self, amount):
        overdraft_limit = 1000

        if amount <= self.balance + overdraft_limit:
            self.balance = self.balance - amount

            self.transactions.append(("Withdraw", amount))

            self.save_transaction_to_file("Withdraw", amount)

            print("Withdraw Successful!")
            print("Remaining Balance:", self.balance)
        else:
            print("Overdraft Limit Exceeded!")


class BankReport:
    def __init__(self, account):
        self.account = account

    def total_deposit(self):
        total = 0

        for transaction in self.account.transactions:
            if transaction[0] == "Deposit":
                total = total + transaction[1]

        return total

    def total_withdraw(self):
        total = 0

        for transaction in self.account.transactions:
            if transaction[0] == "Withdraw":
                total = total + transaction[1]

        return total

    def average_transaction(self):
        amounts = []

        for transaction in self.account.transactions:
            amounts.append(transaction[1])

        if len(amounts) == 0:
            return 0

        average = np.mean(amounts)

        return average

    def sorted_transactions(self):
        amounts = []

        for transaction in self.account.transactions:
            amounts.append(transaction[1])

        if len(amounts) == 0:
            return []

        amounts.sort(reverse=True)

        return amounts

    def show_report(self):
        print("\n===== Analytics Dashboard =====")
        print("Account Holder:", self.account.owner_name)
        print("Account Number:", self.account.account_number)
        print("Total Deposit:", self.total_deposit())
        print("Total Withdraw:", self.total_withdraw())
        print("Average Transaction:", self.average_transaction())
        print("Current Balance:", self.account.balance)

        sorted_amounts = self.sorted_transactions()

        if len(sorted_amounts) > 0:
            print("Highest Transaction:", sorted_amounts[0])
            print("Lowest Transaction:", sorted_amounts[-1])

    def show_bar_graph(self):
        deposit = self.total_deposit()
        withdraw = self.total_withdraw()

        labels = ["Deposit", "Withdraw"]
        values = [deposit, withdraw]

        plt.figure(figsize=(8, 5))

        bars = plt.bar(labels, values)

        plt.title("ATM Transaction Summary")
        plt.xlabel("Transaction Type")
        plt.ylabel("Amount")

        for bar in bars:
            height = bar.get_height()

            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                str(height),
                ha="center"
            )

        plt.show()

    def show_dashboard(self):
        self.show_report()
        self.show_bar_graph()


class ATM:
    def __init__(self):
        self.accounts = {}

    def add_account(self, account):
        self.accounts[account.account_number] = account

    def authenticate(self, account_number, pin):
        if account_number in self.accounts:
            account = self.accounts[account_number]

            if account.pin == pin:
                return account

        return None

    def display_menu(self, current_account):
        while True:
            print("\n===== ATM MENU =====")
            print("1. Check Balance")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Transaction History")
            print("5. Analytics Dashboard")

            if isinstance(current_account, SavingsAccount):
                print("6. Add Interest")
                print("7. Exit")
            else:
                print("6. Exit")

            choice = input("Choose option: ")

            if choice == "1":
                current_account.check_balance()

            elif choice == "2":
                try:
                    amount = float(input("Enter Deposit Amount: "))
                    current_account.deposit(amount)
                except:
                    print("Invalid Amount!")

            elif choice == "3":
                try:
                    amount = float(input("Enter Withdraw Amount: "))
                    current_account.withdraw(amount)
                except:
                    print("Invalid Amount!")

            elif choice == "4":
                current_account.show_transactions()

            elif choice == "5":
                report = BankReport(current_account)
                report.show_dashboard()

            elif choice == "6":
                if isinstance(current_account, SavingsAccount):
                    current_account.add_interest()
                else:
                    print("Thank you for using ATM!")
                    break

            elif choice == "7":
                if isinstance(current_account, SavingsAccount):
                    print("Thank you for using ATM!")
                    break
                else:
                    print("Invalid Choice!")

            else:
                print("Invalid Choice!")


# Creating ATM machine
atm = ATM()

# Creating bank accounts
account1 = BankAccount("1001", "1234", "Amin", 5000)
account2 = SavingsAccount("1002", "5678", "Kim", 8000)
account3 = CurrentAccount("1003", "9999", "John", 12000)

# Adding accounts to ATM
atm.add_account(account1)
atm.add_account(account2)
atm.add_account(account3)

# Login system
print("===== Welcome to SCNU ATM =====")

account_number = input("Enter Account Number: ")
pin = input("Enter PIN: ")

current_account = atm.authenticate(account_number, pin)

if current_account is not None:
    print("Login Successful!")
    print("Welcome,", current_account.owner_name)
    atm.display_menu(current_account)
else:
    print("Invalid Account Number or PIN!")