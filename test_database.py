import pymysql
import pymysql.cursors

LOCALHOST = "127.0.0.1"
USER = "root"
DATABASE = "schoolinfo"

def connect():
    # Connect to the database
    connection = None
    try:
        connection = pymysql.connect(host=LOCALHOST, user=USER, password="", database=DATABASE, cursorclass=pymysql.cursors.DictCursor)
    except Exception as e:
        print(f"Error when connecting to database: {e}")
    
    return connection

def disconnect(connection):
    # Disconnect from the database
    try:
        connection.close()
    except Exception as e:
        print(f"Error when disconnecting from database: {e}")

def test_select_users():
    # Select all users from the database
    try:
        connection = connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `tblusers`"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                print(f"id: {row['id']}, first_name: {row['first_name']}, last_name: {row['last_name']}, email_address: {row['email_address']}, telephone_number: {row['telephone_number']}, date_created: {row['date_created']}")
    finally:
        disconnect(connection)

def test_add_log():
    # Add a log to the database
    try:
        connection = connect()
        with connection.cursor() as cursor:
            sql = "INSERT INTO `tbllogs` (`user_id`, `content`) VALUES (%s, %s)"
            cursor.execute(sql, (1, "What a wonderful day!"))
            connection.commit()
    finally:
        disconnect(connection)

def test_delete_log():
    # Delete a log from the database
    try:
        connection = connect()
        with connection.cursor() as cursor:
            sql = "DELETE FROM `tbllogs` WHERE `id` = %s"
            cursor.execute(sql, (4))
            connection.commit()
    finally:
        disconnect(connection)

def test_update_log():
    # Update a log in the database
    try:
        connection = connect()
        with connection.cursor() as cursor:
            sql = "UPDATE `tbllogs` SET `content` = %s WHERE `id` = %s"
            cursor.execute(sql, ("What a beautiful day!", 3))
            connection.commit()
    finally:
        disconnect(connection)

if __name__ == "__main__":
    # Testing all CRUD operations (Create, Read, Update, Delete)
    test_select_users()
    #test_add_log()
    #test_delete_log()
    #test_update_log()
