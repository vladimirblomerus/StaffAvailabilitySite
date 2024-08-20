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
    updates = {
        "message": "Jag vill informera er om att jag tyvärr måste hålla stängt imorgon på grund av sjukdom. Jag beklagar verkligen det besvär detta kan orsaka och hoppas på er förståelse under dessa omständigheter. Min förhoppning är att kunna återgå till ordinarie öppettider så snart som möjligt, och jag tackar för ert tålamod och er förståelse.",
        "published_datetime": "2024-08-20 12:00",
    }

    return render_template("/view-signs/administration.html", page_title="Administration", person=person, updates=updates)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
