#%%
from pathlib import Path
import pandas as pd
import sqlite3
import datetime

kindle_path = Path("/Volumes/Kindle/")
vocab_db = kindle_path / "system/vocabulary/vocab.db"

def kindle_db_is_available():
    """check that kindle is connected and db exists where we expect"""

    if kindle_path.is_dir():
        print("Kindle is connected ✨")
    else:
        raise FileNotFoundError(f"Mounted kindle not found at {kindle_path}")

    if vocab_db.is_file():
        print("Vocab database was found 🥰")
    else:
        raise FileNotFoundError(f"Vocab db not found at {vocab_db}")

    return True

def get_last_run_time_str():
    try:
        with open("output/last_run", mode="r") as f:
            return f.read()
    except:
        return None

def save_last_run_time_str():
    with open("output/last_run", mode="w") as f:
        timestamp = str(datetime.datetime.now())
        f.write(timestamp)

def create_query(num_days_history_or_last=None):
    """
    Options for time_filter:
    1. all since last run (since forever if no last_run timestamp)
    2. fixed number of days history
    3. nothing specified, since forever
    """
    if str(num_days_history_or_last).lower() == "last":
        last_run_str = get_last_run_time_str()
        if last_run_str is None:
            time_filter = ""
        else:
            time_filter = f"and lookup_timestamp > '{last_run_str}' "
    elif num_days_history_or_last in [int, float]:
        time_filter = (
            f"and lookup_timestamp > date('now', '-{num_days_history_or_last} days')"
        )
    elif num_days_history_or_last is None:
        time_filter = ""
    else:
        raise ValueError("num_days_history_or_last should be number of days, or 'last'")

    query_path = Path("queries/lookups_query.sql")
    query = open(query_path).read().format(time_filter=time_filter)

    return query

def query_to_df(query):
    try:
        conn = sqlite3.connect(vocab_db)
    except Exception as e:
        print(e)

    df = pd.read_sql_query(query, conn)

    return df