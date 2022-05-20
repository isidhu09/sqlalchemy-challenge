# sqlalchemy-challenge

Part 1: Climate Analysis and Exploration
* Used Python and SQLAlchemy to perform basic climate analysis and data exploration of climate database. Completed tasks by using SQLAlchemy ORM queries, Pandas, and Matplotlib
* Used the provided hawaii.sqlite files to complete climate analysis and data exploration
* Used SQLAlchemy’s create_engine to connect to SQLite database
* Used SQLAlchemy’s automap_base() to reflect tables into classes and saved a reference to those classes called Station and Measurement
* Linked Python to the database by creating a SQLAlchemy session

Precipitation Analysis - performed an analysis of precipitation in the area, by doing the following:
* Found the most recent date in the dataset
* Using this date, retrieved the previous 12 months of precipitation data by querying the 12 previous months of data
* Selected only the date and prcp values
* Loaded the query results into a Pandas DataFrame, and set the index to the date column
* Sorted the DataFrame values by date
* Ploted the results by using the DataFrame plot method
* Used Pandas to print the summary statistics for the precipitation data

Station Analysis - performed an analysis of stations in the area, by doing the following:
* Designed a query to calculate the total number of stations in the dataset
* Designed a query to find the most active stations (the stations with the most rows)
* Listed the stations and observation counts in descending order - identifying station with highest observation count
* Using the most active station id, calculated the lowest, highest, and average temperatures
* Designed a query to retrieve the previous 12 months of temperature observation data (TOBS)
* Filtered by the station with the highest number of observations
* Queried the previous 12 months of temperature observation data for this station
* Ploted the results as a histogram with bins=12

Part 2: Designed Climate App - Flask API based on the queries developed in part 1
* Used Flask to create routes, as follows:

* /
* Homepage
* Listed all available routes

* /api/v1.0/precipitation
* Converted the query results to a dictionary using date as the key and prcp as the value
* Returned the JSON representation of dictionary

* /api/v1.0/stations
* Returned a JSON list of stations from the dataset

* /api/v1.0/tobs
* Queried the dates and temperature observations of the most active station for the previous year of data
* Returned a JSON list of temperature observations (TOBS) for the previous year

* /api/v1.0/<start> and /api/v1.0/<start>/<end>
* Returned a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range
* When given the start only, calculated TMIN, TAVG, and TMAX for all dates greater than or equal to the start date
* When given the start and the end date, calculated the TMIN, TAVG, and TMAX for dates from the start date through the end date (inclusive)
