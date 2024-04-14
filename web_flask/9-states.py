#!/usr/bin/python3
"""this script starts a Flask web application
    this web application must be listening on 0.0.0.0 at port 5000
    Route:
        /states: ***
        /states/id: ***
"""
from models import storage
from models.state import State
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def states_id(id=None):
    """Displays an HTML page with a list of all states/cites
        at '/states' path
        or '/states/id' path
    """
    states = storage.all(State)
    if id:
        for state in states.values():
            if id == state.id:
                return render_template("9-states.html", state=state)
        return render_template("9-states.html")
    else:
        return render_template("9-states.html", state=states)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
