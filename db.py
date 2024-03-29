#%%
from pathlib import Path
import pandas as pd
import sqlite3
import datetime

kindle_path = Path("/Volumes/Kindle/")
vocab_db = kindle_path / "system/vocabulary/vocab.db"


def check_kindle_db_available():
    """check kindle is connected and db file is where we expect"""

    if kindle_path.is_dir() is False:
        raise FileNotFoundError(f"Mounted kindle not found at {kindle_path}")

    if vocab_db.is_file() is False:
        raise FileNotFoundError(f"Vocab db not found at {vocab_db}")

    return True


def get_last_run_time_str():
    """read the timestamp of the last run time"""
    try:
        with open(Path(__file__).resolve().parent/"output/last_run", mode="r") as f:
            return f.read()
    except:
        return None


def save_last_run_time_str():
    """write the timestamp of the last run time"""
    with open(Path(__file__).resolve().parent/"output/last_run", mode="w") as f:
        timestamp = str(datetime.datetime.now())
        f.write(timestamp)


def create_query(num_days_history=None):
    """
    Return the query, with relevant time period filter. 
    Options for time_filter:
    1. all since last run (since forever if no last_run timestamp)
    2. fixed number of days history
    """
    if num_days_history is None:
        last_run_str = get_last_run_time_str()
        if last_run_str is None:
            print("No previous run found 🕵️, importing everything 📶")
            time_filter = ""
        else:
            print(f"Previous run on {last_run_str} found, importing since then ⌚️")
            time_filter = f"and lookup_timestamp > '{last_run_str}' "
    elif type(num_days_history) in [int, float]:
        time_filter = (
            f"and lookup_timestamp > date('now', '-{num_days_history} days')"
        )
    else:
        raise ValueError("num_days_history should be a number")

    query_path = Path(__file__).resolve().parent / "queries/lookups_query.sql" # first part is just current folder
    query = open(query_path).read().format(time_filter=time_filter)

    return query


def query_to_df(query):
    """Return the result of the query as a df"""
    try:
        conn = sqlite3.connect(vocab_db)
    except Exception as e:
        print(e)

    df = pd.read_sql_query(query, conn)

    return df


def import_vocab(num_days_history=None):
    """Run the full import process"""
    print("Starting import...")
    check_kindle_db_available()
    print("Kindle is connected ✨, vocab database was found 🥰")
    query = create_query(num_days_history=num_days_history)
    df = query_to_df(query)
    print(f"{len(df)} vocab words imported")
    return df

