# Smart ATM Banking System — Modular Demo

An educational console project using classes, inheritance, method overriding,
SQLite persistence, PIN hashing, and transaction records. Python 3.10 or newer;
no external packages required.

## Run

Keep all six Python files in the same folder, open a terminal there, and run:

```sh
python main.py
```

On macOS/Linux you may need `python3 main.py`.
Create an account, select savings or current, choose a four-digit PIN, and save
the generated account ID. Log in, deposit demo money, and try the menu.
For a transfer, create a second account and use its account ID as the recipient.
All amounts use one unspecified demo currency, with at most two decimal places.

## Files

| File | Responsibility |
| --- | --- |
| main.py | Console menus and program entry point |
| accounts.py | Account classes and Decimal money validation |
| bank.py | Account creation and banking operations |
| security.py | Salted PIN hashes and session login limits |
| storage.py | SQLite account and journal storage |
| transactions.py | History display and CSV statement export |

## GitHub upload

Extract the ZIP and upload the six `.py` files together. This is a separate
modular version: the existing `SCNU-ATM-Banking-System.py` is not required to run
it and has not been modified. If keeping both versions, consider uploading this
version into a `modular_atm` folder. Merge this guide into your existing README
instead of overwriting your own project description blindly.

## Limits

This is a single-process learning simulation, not software for real money.
Deposits are simulated. Savings/current accounts demonstrate inheritance and
have no overdraft; no automatic interest or fees are applied. Failed-login
limits reset on restart. SQLite is not encrypted. Use fictional information.
The menu requires login; service methods assume a trusted local caller.
CSV export includes up to the latest 10,000 records.
Do not commit generated databases, account IDs/PINs, or personal statements.
