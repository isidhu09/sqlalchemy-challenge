# Import Dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from scipy import stats
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>"
    )


@app.route("/api/v1.0/precipitation")
def percipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return precipitation for past year"""
    # Query all precipitation for year
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(recent_date[0], '%Y-%m-%d')
    one_year = last_date - dt.timedelta(days=365)
    query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > one_year).all()
    session.close()

    # Convert list to dictionary
    percip = []
    for date, prcp in query:
        percipDict = {}
        percipDict[date] = prcp
        percip.append(percipDict)
    # Return JSON dict
    return jsonify(percip)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all stations
    stationsLi = session.query(Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all stations
    allStations = []
    for station, name, latitude, longitiude, elevation in stationsLi:
        stationDic = {}
        stationDic["station"] = station
        stationDic["name"] = station
        stationDic["latitude"] = station
        stationDic["longitude"] = station
        stationDic["elevation"] = station
        allStations.append(stationDic)

    return jsonify(allStations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observations for most active station in the previous year"""
    # Query the 12 months of temperature observation data
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    one_year = last_date - dt.timedelta(days=365)
    year_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > one_year).\
    filter(Measurement.station == 'USC00519281').all()
    session.close()

    # Create a dictionary from the station tobs data and append to list
    allTobs = []
    for date, tobs in year_data:
        tobsDic = {}
        tobsDic["date"] = date
        tobsDic["tobs"] = tobs
        allTobs.append(tobsDic)

    # Return JSON representation of list
    return jsonify(allTobs)

@app.route('/api/v1.0/<start>')
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    start_date = dt.datetime.strptime(start, '%Y-%m-%d')

    """Return a list of min, avg, and max temp records after start date"""
    # Query temperature post observation data 
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    session.close()

    # Create a dictionary from the station tobs data and append to list
    tobsAll = []
    for min,avg,max in results:
        tobsDic = {}
        tobsDic["Min"] = min
        tobsDic["Average"] = avg
        tobsDic["Max"] = max
        tobsAll.append(tobsDic)

    # Return JSON representation of list
    return jsonify(tobsAll)

@app.route('/api/v1.0/<start>/<stop>')
def range(start,stop):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    stop_date = dt.datetime.strptime(stop, '%Y-%m-%d')

    """Return a list of min, avg, and max temp between start/stop dates"""
    # Query temperature observation data between dates
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= stop_date).all()
    session.close()

    # Create a dictionary from the station tobs data and append to list
    tobsAll = []
    for min,avg,max in results:
        tobsDic = {}
        tobsDic["Min"] = min
        tobsDic["Average"] = avg
        tobsDic["Max"] = max
        tobsAll.append(tobsDic)

    # Return JSON representation of list
    return jsonify(tobsAll)

if __name__ == '__main__':
    app.run(debug=True)

