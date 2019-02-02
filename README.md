# Python CSV to SQLite
This application reads a CSV input file given from the command line and save those values into a SQLite database.


### Input file 
The first line of the file will be ignored because it is assumed that it contains titles.
It is expected that each row contains three fields of data about boardgames: Name, Designer and Rating.
If there is an error in some row of the input file, none of the games will be added.
The game name is used as key to store the data in the database.

#### Example:

```
name,artist,rating
Blood Rage,Eric M. Lang,9
Stone Age,Bernd Brunnhofer,7
King of Tokyo,Richard Garfield,7
Ticket to Ride,Alan R. Moon,8
Carcassonne,Klaus-Jürgen Wrede,7
Istanbul,Ruediger Dorn,6
Forbidden Island,Matt Leacock,8
Tikal,Michael Kiesling,7
Catan,Klaus Teuber,6
Tsuro,Tom McMurchie,8
```

### Output example
```
02-02-2019 10:42:04 INFO     [app.py:52] Reading file...
02-02-2019 10:42:04 INFO     [app.py:78] Adding games...
02-02-2019 10:42:05 INFO     [app.py:84] 10 games were inserted of 10
```

If there is an error inserting a game into the database, only that item will not be added, the app 
will continue trying to insert the rest of rows.

```
...
...
02-02-2019 12:53:10 ERROR    [app.py:95] UNIQUE constraint failed: games.name error inserting Game Tsuro by Tom McMurchie, Rating: 8
02-02-2019 12:53:10 INFO     [app.py:84] 2 games were inserted of 12
```


## Running application
Prerequisites: Python3.x (tested with Python 3.7), it does not work with Python2.x

Go to the root folder of the application and execute the following command: 

`./app-src/app.py <your-csv-file>`


It is provided a file with entry data to test, use it as follow:

`./app-src/app.py csv_data.txt`


#### Running test
Prerequisites: pytest

`pytest -v`


## Running application in a docker container
The image is based on Alpine with Python 3.7
There is a volume to share data between the application and the container, so
the database file will be in the host.

Go to the root folder of the application and use the following options:


#### Running app using example file 
`make build run f=csv_data.txt`


#### Running app using your data file
Copy your file into the application folder so it can be used by the container.

`make build run f=<your-csv-file>`


#### To remove container and image
`make clean`

