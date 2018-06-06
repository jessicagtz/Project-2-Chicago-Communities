import datetime as dt
import numpy as np
import pandas as pd

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///chi_db.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Communities = Base.classes.comm_names
Neighborhoods = Base.classes.neighborhoods
Twitter = Base.classes.twitter

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Routes
#################################################

@app.route("/dash/<ID>")
def dash(ID):
    names = session.query(Communities).filter(Communities.id == ID)
    all_names = []
    for name in names:
        comm_dict = {}
        comm_dict["name"] = name.community
        all_names.append(comm_dict)
    name = jsonify(all_names)
    twitters = session.query(Twitter).filter(Twitter.id == ID)
    handles = []
    for handle in twitters:
        handle_dict = {}
        handle_dict["handle"] = handle.twitter_handle
        handles.append(handle_dict)
    twitter_handle = jsonify(handles)
    return render_template("index.html", comm_dict=comm_dict, handle_dict=handle_dict)


@app.route("/twitter/<ID>")
def twitter(ID):
    twitters = session.query(Twitter).filter(Twitter.id == ID)
    handles = []
    for handle in twitters:
        handle_dict = {}
        handle_dict["handle"] = handle.twitter_handle
        handles.append(handle_dict)
    twitter_handle = jsonify(handles)
    return twitter_handle
    

@app.route("/names/<ID>")
def names(ID):
    results = session.query(Communities).filter(Communities.id == ID)

    all_communities = []
    for comm in results:
        comm_dict = {}
        comm_dict["ID"] = comm.id
        comm_dict["Name"] = comm.community
        all_communities.append(comm_dict)

    return jsonify(all_communities)

@app.route("/hoods/<ID>")
def hoods(ID):
    results = session.query(Neighborhoods).filter(Neighborhoods.ID ==ID)

    all_neighborhoods = []
    for hood in results:
        hood_dict = {}
        hood_dict["ID"] = hood.ID
        hood_dict["Neighborhoods"] = hood.neighborhoods
        all_neighborhoods.append(hood_dict)

    return jsonify(all_neighborhoods)


if __name__ == '__main__':
    app.run(debug=True)
