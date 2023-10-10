import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid
import re
from cs50 import SQL

from flask import redirect, render_template, session
from functools import wraps

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///climberslog.db")


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Prepare API request
    symbol = symbol.upper()
    end = datetime.datetime.now(pytz.timezone("US/Eastern"))
    start = end - datetime.timedelta(days=7)

    # Yahoo Finance API
    url = (
        f"https://query1.finance.yahoo.com/v7/finance/download/{urllib.parse.quote_plus(symbol)}"
        f"?period1={int(start.timestamp())}"
        f"&period2={int(end.timestamp())}"
        f"&interval=1d&events=history&includeAdjustedClose=true"
    )

    # Query API
    try:
        response = requests.get(url, cookies={"session": str(uuid.uuid4())}, headers={
            "User-Agent": "python-requests", "Accept": "*/*"})
        response.raise_for_status()

        # CSV header: Date,Open,High,Low,Close,Adj Close,Volume
        quotes = list(csv.DictReader(response.content.decode("utf-8").splitlines()))
        quotes.reverse()
        price = round(float(quotes[0]["Adj Close"]), 2)
        return {
            "name": symbol,
            "price": price,
            "symbol": symbol
        }
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def is_strong_password(password):
    # Define password strength rules using regular expressions
    min_length = 8
    min_uppercase = 1
    min_lowercase = 1
    min_digits = 1
    min_special_chars = 1

    # Regular expressions for character classes
    uppercase_regex = r'[A-Z]'
    lowercase_regex = r'[a-z]'
    digits_regex = r'[0-9]'
    special_chars_regex = r'[!@#$%^&*()_+{}[\]:;<>,.?~]'

    # Check password against rules
    if len(password) < min_length:
        return False
    if len(re.findall(uppercase_regex, password)) < min_uppercase:
        return False
    if len(re.findall(lowercase_regex, password)) < min_lowercase:
        return False
    if len(re.findall(digits_regex, password)) < min_digits:
        return False
    if len(re.findall(special_chars_regex, password)) < min_special_chars:
        return False

    return True


def get_username(session):
    """Get the username for the current user based on the session."""
    user_id = session.get("user_id")

    if user_id is not None:
        user = db.execute("SELECT username FROM users WHERE id = :user_id", user_id=user_id)
        return user[0]["username"] if user else None

    return None



def calculate_weighted_kpi(level1, level2, level3, level4, level5, level6, level7, level8, gym_levels):
    if gym_levels < 1:
        raise ValueError("Gym levels must be at least 1.")



    kpi = 0
    for i in range(1, gym_levels + 1):
        tops = locals().get(f"level{i}", 0)
        kpi += ((i / gym_levels) ** 5) * tops

    # Round the KPI value to two decimal places
    kpi = round(kpi, 2)

    return kpi

# Helper function to convert to integer or set a default value
def convert_to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0  # Default to 0 for empty or invalid input
