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
from sqlalchemy import create_engine, inspect

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
from flask_sqlalchemy import SQLAlchemy
# The database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///chi_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


engine = create_engine("sqlite:///chi_db")
inspector = inspect(engine)

db = SQLAlchemy(app)

@app.route("/<comm>")
def commdata(comm):
    result = engine.execute(f"SELECT comm_names.community, crime.battery,\
                        crime.deceptive_pracice, crime.homicide, \
                        crime.narcotics, crime.non_criminal, crime.sexual, \
                        crime.theft, race.asian, race.white, race.other, \
                        race.black, race.hispanic, housing.percent_own \
                        FROM comm_names JOIN crime ON comm_names.id = crime.id \
                        JOIN race ON crime.id = race.id JOIN housing ON \
                        race.id = housing.id WHERE comm_names.id = {comm};").fetchall()
    result = result[0]
    result_dict = {
        "name":result[0],
        "crime":{
            "battery":result[1],
            "deceptive_practice":result[2],
            "homicide":result[3],
            "narcotics":result[4],
            "non_criminal":result[5],
            "sexual":result[6],
            "theft":result[7]
        },
        "pop_race":{
            "asian":result[8],
            "white":result[9],
            "other":result[10],
            "black":result[11],
            "hispanic":result[12]
        },
        "percent_owners":result[13]
    }

    return jsonify(result_dict)
    
if __name__ == "__main__":
    app.run(debug=True)