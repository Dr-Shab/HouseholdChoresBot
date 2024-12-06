from flask import Flask, request, render_template, redirect
import datetime
import requests
import os

app = Flask(__name__, template_folder='templates')

DB_API_URL = os.getenv("DB_API")

@app.route('/', methods=['GET'])
def standardview():
    return render_template('index.html')

@app.route('/checkinforwork', methods=['GET'])
def checkin():
    token = request.args.get('zodiac')
    if not token:
        return '<h1>Invalid check-in link.</h1>', 400

    timestamp = datetime.datetime.now()

    response = requests.post(DB_API_URL, json={'token': str(token), 'timestamp': str(timestamp)})
    if response.status_code == 200:
        return '<h1>Check-in successful!</h1>', 200
    return redirect("https://media.tenor.com/ihqN6a3iiYEAAAAd/pikachu-shocked-face-stunned.gif", 302)


if __name__ == '__main__':
    """
        Example for db request https://happycastle.ch/checkinforwork?zodiac=78d43094f8c056d196d7167e43ed5758
    """
    app.run(host='0.0.0.0', debug=False, port=8080)
