#!/usr/bin/python3
""" Script that starts a Flask web application """

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def display_hbnb_filters():
    """ Route displays an HTML page with Airbnb filters """
    states = sorted(storage.all("State").values(), key=lambda x: x.name)
    cities = sorted(storage.all("City").values(), key=lambda x: x.name)
    return render_template('10-hbnb_filters.html',
                           states=states,
                           cities=cities,
                           amenities=amenities)


@app.teardown_appcontext
def teardown_db(exception):
    """ method to close storage """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
