import mysql.connector




def stream_users_in_batches(batch_size):
    connection = connection = mysql.connector.connect(
        host = 'localhost',
        user = 'alx_user',
        password = 'asdffdsa',
        database = 'ALX_prodev'
    )
   
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data")

    while True:
        users = cursor.fetchmany(batch_size)
        for user in users:
            yield user

        cursor.close()
        connection.close()

    
        

        
            



def batch_processing(batch_size):
    users = stream_users_in_batches(batch_size)
    while True:
        try:
            user = next(users)
            if user["age"] > 25:
                print(user)

        except StopIteration:
            break

    