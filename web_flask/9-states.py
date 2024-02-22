#!/usr/bin/python3
"""
Script that starts a Flask web application
"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def display_states():
    """
    Route that displays a HTML page with a list of states
    """
    states = storage.all("State").values()
    return render_template('9-states.html', states=states)


@app.route('/states/<state_id>', strict_slashes=False)
def display_state_cities(state_id):
    """
    Route that displays a HTML page with cities of a given state
    """
    state = storage.get("State", state_id)
    if state is None:
        return render_template('9-not_found.html'), 404
    else:
        return render_template('9-states.html', state=state)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Teardown method to close storage
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
