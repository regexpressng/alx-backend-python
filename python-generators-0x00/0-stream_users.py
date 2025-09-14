import mysql.connector



def stream_users():
    connection = connection = mysql.connector.connect(
        host = 'localhost',
        user = 'alx_user',
        password = 'asdffdsa',
        database = 'ALX_prodev'
    )
   
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data")
    all_users = cursor.fetchall()
    
    for user in all_users:
        yield user

    cursor.close()
    connection.close()

import sys
import types

class CallableModule(types.ModuleType):
    def __call__(self, *args, **kwargs):
        # Call the function stored as attribute 'stream_users' on this proxy
        return getattr(self, "stream_users")(*args, **kwargs)

# create the proxy and copy module globals into it
proxy = CallableModule(__name__)
proxy.__dict__.update(globals())

# replace the module object in sys.modules with our callable proxy
sys.modules[__name__] = proxy
