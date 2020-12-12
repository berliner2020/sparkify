# Data Modeling with Postgres
To address Sparkify's business goal of quickly analyzing song play data from their music streaming app, this database 
has been built with analytics in mind. 

The database uses Postgresql as the DBMS and uses a star schema with 
songplays and artists, songs, time, and users as it's dimension tables.

## Setup
### Requirements and Dependencies
Before running any of the scripts in this app, be sure to create a virtual environment or Docker container with the 
requirements.txt file which has been provided.

    pip install -r requirements.txt

### Database
The easiest way to get started with the database is by using Docker. You can download it here: https://docs.docker.
com/get-docker/.

Once Docker has been installed, you can create and run a container with the latest version of Postgresql by running 
the command below in the CLI.

    docker run -d -p 5432:5432 --name sparkify -e POSTGRES_PASSWORD=mysecretpassword postgres

With the container running, access it by running this command and then create a database for the application

    docker exec -it my-postgres bash
    psql -U postgres
    CREATE DATABASE sparkifydb;

### Application
With the database running, you are ready to run the application.

#### Create Tables
Create the tables for the application by running create_tables.py. This will drop any tables you currently in your 
database as well as create new ones for your data. The tables which will be created in your database are:
- fact
    - songplays
- dimensions
    - artists
    - time
    - users
    - songs

#### Data Migration
With the tables in place, it is time to load the data into the tables from the data sources by running etl.py. This 
file runs through the log and song data json files in the data folder included with this project and extracts 
them into dataframes using pandas. Pandas is used to do the transformations on the data (e.g., normalization, 
missing values). Finally, data is loaded into the different tables using the sql_queries.py imported into the etl.py 
while it runs.

