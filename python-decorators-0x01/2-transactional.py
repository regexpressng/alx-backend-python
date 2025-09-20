#!/usr/bin/python3
import functools
from seed import connect_to_prodev   # reuse your DB connection utility

def with_db_connection(func):
    """Decorator to handle opening and closing database connections automatically"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        connection = connect_to_prodev()
        try:
            # Pass the connection into the wrapped function
            result = func(connection, *args, **kwargs)
            return result
        finally:
            # Ensure the connection is always closed
            connection.close()
    return wrapper


def transactional(func):
    """Decorator to manage transactions (commit on success, rollback on error)"""
    @functools.wraps(func)
    def wrapper(connection, *args, **kwargs):
        try:
            result = func(connection, *args, **kwargs)
            connection.commit()   
            return result
        except Exception as e:
            connection.rollback()  
            print(f"Transaction failed, rolled back. Error: {e}")
            raise
    return wrapper


# Example usage
@with_db_connection
@transactional
def insert_user(connection, name, email, age):
    """Insert a user into the user_data table"""
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO user_data (user_id, name, email, age) VALUES (UUID(), %s, %s, %s)",
        (name, email, age)
    )
    cursor.close()
    return "User inserted successfully"


if __name__ == "__main__":
    try:
        print(insert_user("Test User", "testuser@example.com", 30))
    except Exception as e:
        print("Error during insert:", e)