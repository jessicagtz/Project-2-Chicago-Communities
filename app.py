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
Population = Base.classes.population
Race = Base.classes.race
Crime = Base.classes.crime

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Routes
#################################################

@app.route("/")
def index():


    #render the index template
    return render_template("index.html")

@app.route("/dash/<ID>")
def dash(ID):
    # query for the community name based off of ID selected
    names = session.query(Communities).filter(Communities.id == ID)
    all_names = []
    for name in names:
        comm_dict = {}
        comm_dict["name"] = name.community
        all_names.append(comm_dict)
    name = jsonify(all_names)
    # query for community twitter handle based off of ID
    twitters = session.query(Twitter).filter(Twitter.id == ID)
    handles = []
    for handle in twitters:
        handle_dict = {}
        handle_dict["handle"] = handle.twitter_handle
        handles.append(handle_dict)
    twitter_handle = jsonify(handles)
    # query the population data for chart based off of ID
    results = session.query(Population).filter(Population.id == ID)
    totals = session.query(Population).filter(Population.id == 78)

    pop = []
    for population in results:
        pop_dict = {}
        pop_dict["ID"] = population.id
        pop_dict["_1930"] = population._1930
        pop_dict["_1940"] = population._1940
        pop_dict["_1950"] = population._1950
        pop_dict["_1960"] = population._1960
        pop_dict["_1970"] = population._1970
        pop_dict["_1980"] = population._1980
        pop_dict["_1990"] = population._1990
        pop_dict["_2000"] = population._2000
        pop_dict["_2010"] = population._2010
        pop_dict["_2015"] = population._2015    
    
    for total in totals:
        pop_dict["all_1930"] = total._1930
        pop_dict["all_1940"] = total._1940
        pop_dict["all_1950"] = total._1950
        pop_dict["all_1960"] = total._1960
        pop_dict["all_1970"] = total._1970
        pop_dict["all_1980"] = total._1980
        pop_dict["all_1990"] = total._1990
        pop_dict["all_2000"] = total._2000
        pop_dict["all_2010"] = total._2010
        pop_dict["all_2015"] = total._2015
        pop.append(pop_dict)

    population_data = jsonify(pop)
    
    # query the race data for chart based off of ID
    demographics = session.query(Race).filter(Race.id == ID)

    race = []
    for demo in demographics:
        demo_dict = {}
        demo_dict["ID"] = demo.id
        demo_dict["asian2015"] = demo.asian2015
        demo_dict["black2015"] = demo.black2015
        demo_dict["hispanic2015"] = demo.hispanic2015
        demo_dict["other2015"] = demo.other2015
        demo_dict["white2015"] = demo.white2015
        race.append(demo_dict)
    race_data = jsonify(race)

    # query the neighborhood data for chart based off of ID
    neighborhoods = session.query(Neighborhoods).filter(Neighborhoods.ID ==ID)

    all_neighborhoods = []
    for hood in neighborhoods:
        hood_dict = {}
        hood_dict["ID"] = hood.ID
        hood_dict["Neighborhoods"] = hood.neighborhoods
        all_neighborhoods.append(hood_dict)
    neighborhood_data = jsonify(all_neighborhoods)

    #query the crime data for chart based off of ID
    crimes = session.query(Crime).filter(Crime.id == ID)

    crime_data = []
    for crime in crimes:
        crime_dict = {}
        crime_dict["ID"] = crime.id
        crime_dict["battery"] = crime.battery
        crime_dict["deceptive_practice"] = crime.deceptive_practice
        crime_dict["homicide"] = crime.homicide
        crime_dict["narcotics"] = crime.narcotics
        crime_dict["non_criminal"] = crime.non_criminal
        crime_dict["sexual"] = crime.sexual
        crime_dict["theft"] = crime.theft
        crime_data.append(crime_dict)
    crimes2017 = jsonify(crime_data)
    
    # render the template
    return render_template("dashboard.html", comm_dict=comm_dict, handle_dict=handle_dict, pop_dict=pop_dict, demo_dict=demo_dict, hood_dict=hood_dict, crime_dict=crime_dict)


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

@app.route("/pop/<ID>")
def pop(ID):
    results = session.query(Population).filter(Population.id == ID)
    totals = session.query(Population).filter(Population.id == 78)

    pop = []
    for population in results:
        pop_dict = {}
        pop_dict["ID"] = population.id
        pop_dict["1930"] = population._1930
        pop_dict["1940"] = population._1940
        pop_dict["1950"] = population._1950
        pop_dict["1960"] = population._1960
        pop_dict["1970"] = population._1970
        pop_dict["1980"] = population._1980
        pop_dict["1990"] = population._1990
        pop_dict["2000"] = population._2000
        pop_dict["2010"] = population._2010
        pop_dict["2015"] = population._2015
        
    
    for total in totals:
        pop_dict["all_1930"] = total._1930
        pop_dict["all_1940"] = total._1940
        pop_dict["all_1950"] = total._1950
        pop_dict["all_1960"] = total._1960
        pop_dict["all_1970"] = total._1970
        pop_dict["all_1980"] = total._1980
        pop_dict["all_1990"] = total._1990
        pop_dict["all_2000"] = total._2000
        pop_dict["all_2010"] = total._2010
        pop_dict["all_2015"] = total._2015
        pop.append(pop_dict)
    

    return jsonify(pop)

@app.route("/race/<ID>")
def race(ID):
    demographics = session.query(Race).filter(Race.id == ID)

    race = []
    for demo in demographics:
        demo_dict = {}
        demo_dict["ID"] = demo.id
        demo_dict["asian2015"] = demo.asian2015
        demo_dict["black2015"] = demo.black2015
        demo_dict["hispanic2015"] = demo.hispanic2015
        demo_dict["other2015"] = demo.other2015
        demo_dict["white2015"] = demo.white2015
        race.append(demo_dict)
    
    return jsonify(race)

@app.route("/crime/<ID>")
def crime(ID):
    crimes = session.query(Crime).filter(Crime.id == ID)

    crime_data = []
    for crime in crimes:
        crime_dict = {}
        crime_dict["ID"] = crime.id
        crime_dict["battery"] = crime.battery
        crime_dict["deceptive_practice"] = crime.deceptive_practice
        crime_dict["homicide"] = crime.homicide
        crime_dict["narcotics"] = crime.narcotics
        crime_dict["non_criminal"] = crime.non_criminal
        crime_dict["sexual"] = crime.sexual
        crime_dict["theft"] = crime.theft
        crime_data.append(crime_dict)
    
    return jsonify(crime_data)

@app.route("/about")
def about():
    return("Chicago Community Project: "
        "Nameyeh Alam, Emre Celik, Maddy Cieslak, Jess Gutierrez, Stefan Sampaleanu")   

if __name__ == '__main__':
    app.run(debug=True)
