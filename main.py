from flask import Flask, render_template, redirect, url_for, request
import pymysql
import pymysql.cursors
from datetime import datetime, timedelta, MINYEAR

LOCALHOST = "127.0.0.1"
USER = "root"
DATABASE = "schoolinfo"

USER_FETCH_INTERVAL = timedelta(minutes=10) # To lighten the load on the database, as the users don't change that often


users = {
    "user_list": [],
    "last_updated": datetime(MINYEAR, 1, 1) # Force an update on the first request
}

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
    # Fetch all users from the database if the global users variable is outdated
    if users["last_updated"] > datetime.now() - USER_FETCH_INTERVAL:
        return
    
    try:
        connection = connect()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `tblusers`"
            cursor.execute(sql)
            result = cursor.fetchall()

            # TODO: Replace this with a proper logging mechanism
            print(f"selected users: {result}")

            users["user_list"] = result
            users["last_updated"] = datetime.now()
    finally:
        disconnect(connection)

def get_user_by_profession(profession):
    # Select a user by profession from the global users variable
    get_users()
    user = next(user for user in users["user_list"] if user["profession"] == profession)

    # TODO: Replace this with a proper logging mechanism
    print(f"selected user with profession {profession}: {user}")
    return user

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

def post_log(user_id, content):
    # Add a log to the database
    try:
        connection = connect()
        with connection.cursor() as cursor:
            sql = "INSERT INTO `tbllogs` (`user_id`, `content`) VALUES (%s, %s)"
            cursor.execute(sql, (user_id, content))
            connection.commit()

            # TODO: Replace this with a proper logging mechanism
            print(f"added log with user ID {user_id} and content {content}")

            return {"type": "success", "message": "Uppdateringen har skickats."}
    except Exception as e:
        # TODO: Replace this with a proper logging mechanism
        print(f"Error when adding log: {e}")
        return {"type": "error", "message": "Något gick fel när uppdateringen skulle skickas."}
    finally:
        disconnect(connection)

def count_users_with_role_id(role_id):
    # Count users with a specific role ID using the global users variable
    return sum(1 for user in users["user_list"] if user["role_id"] == role_id)

@app.route("/")
def home():
    get_users()
    return render_template("index.html", page_title="Home", count_moderators=count_users_with_role_id(2))

@app.route("/error", defaults={"message": "404 - Sidan hittades inte."})
def error(message):
    return render_template("system/error.html", message=message)

def get_administration_data():
    # Get data for the administration page
    person = get_user_by_profession("Administrator")
    if person is None:
        return redirect(url_for("error", message="404 - Personen hittades inte."))
    
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

    if updates is None:
        return person_dto, None

    updates_dto = {
        "message": updates["content"],
        "published_datetime": updates["date_created"],
    }

    return person_dto, updates_dto

@app.route("/administration/")
def administration(toast=None):
    room_name = "Administration"
    person_dto, updates_dto = get_administration_data()
    if toast is not None:
        print(toast)
    return render_template("/view-signs/administration.html", page_title="Administration", room_name=room_name, person=person_dto, updates=updates_dto, toast=toast)


@app.route("/administration/update/", methods=["GET"])
def administration_update(toast=None, prefilled_message=""):
    # TODO: Check if the user is logged in and has the correct role
    room_name = "Administration"
    person_dto, updates_dto = get_administration_data()
    if toast is not None:
        print(toast)
    if prefilled_message != "":
        updates_dto["message"] = prefilled_message
        updates_dto["published_datetime"] = datetime(MINYEAR, 1, 1) # Because the message is not published yet, and we don't want to show the old date
    return render_template("/view-signs/administration-update.html", page_title="Administration - Uppdatera", room_name=room_name, person=person_dto, updates=updates_dto, toast=toast)

@app.route("/administration/update/submit/", methods=["POST"])
def administration_update_submit():
    # TODO: Check if the user is logged in and has the correct role
    message = request.form["message"]
    if len(message) > 4:
        post_toast = post_log(3, message) # TODO: Replace 3 with the user ID of the logged in user
        return administration_update(toast=post_toast)
    else:
        post_toast = {"type": "error", "message": "Meddelandet måste innehålla minst 5 tecken."}
        return administration_update(toast=post_toast, prefilled_message=message)

# Catch-all route for non-existing pages
@app.route("/<path:path>")
def catch_all(path):
    return redirect(url_for("error", message="404 - Sidan hittades inte."))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
