"""PIN hashing and validation for an educational ATM application."""
import hashlib
import hmac
import secrets
from getpass import getpass

ITERATIONS = 200_000


def validate_pin(pin):
    if not (pin.isascii() and pin.isdigit() and len(pin) == 4):
        raise ValueError('PIN must contain exactly four digits.')
    return pin


def hash_pin(pin, salt=None):
    validate_pin(pin)
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        'sha256', pin.encode(), bytes.fromhex(salt), ITERATIONS
    ).hex()
    return f'{salt}:{digest}'


def verify_pin(pin, stored):
    try:
        salt, expected = stored.split(':')
        actual = hash_pin(pin, salt).split(':')[1]
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError, AttributeError):
        return False


class LoginGuard:
    """Limit failed logins during the current program session."""

    def __init__(self, maximum=3):
        self.maximum = maximum
        self.attempts = {}

    def authenticate(self, account_id, pin, stored_hash):
        if self.attempts.get(account_id, 0) >= self.maximum:
            raise ValueError('Account locked for this session. Restart to retry.')
        if not verify_pin(pin, stored_hash):
            self.attempts[account_id] = self.attempts.get(account_id, 0) + 1
            remaining = self.maximum - self.attempts[account_id]
            raise ValueError(f'Incorrect PIN. Remaining attempts: {remaining}')
        self.attempts.pop(account_id, None)
        return True


def prompt_new_pin():
    pin = getpass('Choose a four-digit PIN: ')
    validate_pin(pin)
    if pin != getpass('Confirm PIN: '):
        raise ValueError('PINs do not match.')
    return pin
