#!/usr/bin/python3
import seed
stream_users = __import__('0-stream_users')

def stream_users_in_batches(batch_size):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True, buffered=True)
    cursor.execute("SELECT * FROM user_data;")


    
    try:
        while True:
            # Fetch the next batch of rows
            user_batch = cursor.fetchmany(batch_size)
            
            # cursor.fetchmany() returns an empty list [] when no more rows remain
            if not user_batch:
                break
                
            yield user_batch

    finally:
        # Clean up resources
        cursor.close()
        connection.close()
    
    

def batch_processing(batch_size):
    user_batch_stream = stream_users_in_batches(batch_size)

    try:
        current_batch = next(user_batch_stream)
        for user in current_batch:
            if user.get("age") > 25:
                print(user)
    except StopIteration:
        return
        
    
    
