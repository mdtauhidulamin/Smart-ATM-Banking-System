"""Transaction records, statements, and CSV export."""
import csv
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

FIELDS = ['transaction_id', 'account_id', 'kind', 'amount',
          'balance_after', 'timestamp', 'note']


def make_entry(account, kind, amount, note=''):
    return {
        'transaction_id': uuid4().hex,
        'account_id': account.account_id,
        'kind': kind,
        'amount': str(amount),
        'balance_after': str(account.balance),
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'note': note,
    }


def print_statement(entries):
    if not entries:
        print('No transactions yet.')
        return
    print('\n' + '-' * 76)
    print(f'{"Date (UTC)":20} {"Type":14} {"Amount":>12} {"Balance":>12}')
    print('-' * 76)
    for entry in entries:
        date = entry['timestamp'][:19].replace('T', ' ')
        print(f'{date:20} {entry["kind"]:14} '
              f'{entry["amount"]:>12} {entry["balance_after"]:>12}')
        if entry['note']:
            print('  ' + entry['note'])
    print('-' * 76)


def csv_safe(value):
    """Prevent text cells from becoming spreadsheet formulas."""
    text = str(value)
    if text.lstrip().startswith(('=', '+', '-', '@')):
        return "'" + text
    return text


def export_statement(entries, destination):
    destination = Path(destination)
    with destination.open('w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        for entry in entries:
            writer.writerow({key: csv_safe(entry[key]) for key in FIELDS})
    return destination.resolve()
