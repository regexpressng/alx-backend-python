import mysql.connector

connection = connection = mysql.connector.connect(
        host = 'localhost',
        user = 'alx_user',
        password = 'asdffdsa',
        database = 'ALX_prodev'
    )
   
cursor = connection.cursor(dictionary=True)

cursor.execute("SELECT * FROM user_data")


def stream_users_in_batches(batch_size):
    while True:
        users = cursor.fetchmany(batch_size)
        if not users:
            return
        yield users
    
        

        
            



def batch_processing(batch_size):
    for users in stream_users_in_batches(batch_size):
        for user in users:
            if user["age"] > 25:
                print(user)

    