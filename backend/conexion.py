import mysql.connector

mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'moto',
    'auth_plugin': 'mysql_native_password'
}

connection = mysql.connector.connect(**mysql_config)
def get_connection():
    return connection
