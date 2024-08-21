from flask import Flask, render_template
import pymysql
import pymysql.cursors

LOCALHOST = "127.0.0.1"
USER = "root"
DATABASE = "schoolinfo"


users: list[object] = []

app = Flask(__name__)

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

def get_users():
    global users
    # Select all users from the database
    try:
        connection = connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `tblusers`"
            cursor.execute(sql)
            result = cursor.fetchall()

            # TODO: Replace this with a proper logging mechanism
            print(f"selected users: {result}")

            users = result
    finally:
        disconnect(connection)

def get_user_by_profession(profession):
    # Select a user by profession from the database
    try:
        connection = connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `tblusers` WHERE `profession` = %s"
            cursor.execute(sql, (profession))
            result = cursor.fetchone()

            # TODO: Replace this with a proper logging mechanism
            print(f"selected user with profession {profession}: {result}")

            return result
    finally:
        disconnect(connection)

def get_latest_log_by_user_id(user_id):
    # Select the last log by user ID from the database
    try:
        connection = connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `tbllogs` WHERE `user_id` = %s ORDER BY `date_created` DESC LIMIT 1"
            cursor.execute(sql, (user_id))
            result = cursor.fetchone()

            # TODO: Replace this with a proper logging mechanism
            print(f"selected latest log by user ID {user_id}: {result}")

            return result
    finally:
        disconnect(connection)

def count_users_with_role_id(role_id):
    # Count users with a specific role ID using the global users variable
    return sum(1 for user in users if user["role_id"] == role_id)

@app.route("/")
def home():
    get_users()
    return render_template("index.html", page_title="Home", count_moderators=count_users_with_role_id(2))

@app.route("/administration")
def administration():
    person = get_user_by_profession("Administrator")
    if person is None:
        return render_template("system/error.html", page_title="404", message="404 - Personen hittades inte.")
    
    person_dto = {
        "name": person["first_name"] + " " + person["last_name"],
        "phone": person["telephone_number"],
        "email": person["email_address"],
        "open_hours": [
            "Måndag: 8:00 - 12:00",
            "Tisdag: 12:00 - 16:00",
            "Onsdag - Fredag: 8:00 - 12:00",
        ] # TODO: Fetch this from the database
    }
    
    updates = get_latest_log_by_user_id(person["id"])

    updates_dto = {
        "message": updates["content"],
        "published_datetime": updates["date_created"],
    }

    return render_template("/view-signs/administration.html", page_title="Administration", person=person_dto, updates=updates_dto)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
