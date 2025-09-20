#!/usr/bin/python3
import time
import sqlite3 
import functools


#### paste your with_db_decorator here
def with_db_connection(func):
    """ your code goes here"""
    @functools.wraps(func)
    def wrapper():
        try:
            conn = sqlite3.connect('user.db')
            result = func(conn)
            return result

        except Exception as e:
             print(f"An unexpected error occurred: {e}")
    return wrapper

""" your code goes here"""
def retry_on_failure(retries, delay):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error=None
            for retry in range(retries):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    last_error = e
                    print(f"Attempt {retry + 1} failed: {e}")
                    time.sleep(delay)
            raise last_error
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)