#!/usr/bin/python3
import sqlite3
import functools
from datetime import datetime

#### decorator to log SQL queries

""" YOUR CODE GOES HERE"""
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args:
            print(f"{datetime.utcnow()} LOG: {args[0]}")
        if 'query' in kwargs:
            print(f"{datetime.utcnow()} LOG: {kwargs.get('query')}")
        return func(*args, **kwargs)
            
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")