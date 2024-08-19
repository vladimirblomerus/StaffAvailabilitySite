from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", page_title="Home")

@app.route("/administration")
def administration():
    person = {
        "name": "Lina Aker",
        "phone": "019-44 64 60",
        "email": "lina.aker@ntig.se",
        "open_hours": [
            "Måndag: 8:00 - 12:00",
            "Tisdag: 12:00 - 16:00",
            "Onsdag - Fredag: 8:00 - 12:00",
        ],
    }
    availability = {
        "message": "Stängt för dagen",
        "datetime": "imorgon, 12:00",
    }

    return render_template("/view-signs/administration.html", page_title="Administration", person=person, availability=availability, status_messages=[ "Lorem ipsum dolor sit amet.", "Ut enim ad minim veniam." ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
