from flask import Flask, render_template
import json
import os

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Read the latest threats from the JSON file
    alerts = []
    if os.path.exists("alerts.json"):
        with open("alerts.json", "r") as f:
            try:
                alerts = json.load(f)
            except:
                alerts = []
    
    # Send the data to the HTML file
    return render_template("index.html", alerts=alerts)

if __name__ == "__main__":
    app.run(port=5000, debug=True)