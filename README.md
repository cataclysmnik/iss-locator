# ISS Locator

A simple project I made to learn the usage of APIs. Provides the position of the ISS and plots the past and future locations on the world map whenever the program is run.

## Description

First, ISS Locator gets the live coordinates of the ISS from [wheretheiss](https://wheretheiss.at/).
Then, the latitude and longitude values are input into [geonames](https://geonames.org) to get the closest place on earth using reverse geocoding.
Finally, the latitude and longitude values are plotted on the world map using [plotly](https://plotly.org).

## Getting Started

### Dependencies

- Make sure you have python and pip installed.
- Create a [GeoNames](https://geonames.org) account and allow access for geocoding.

### Installing

- Download `main.py` and `requirements.txt` to an appropriate folder. Alternatively, clone this repo.
- Create a virtual environment.
- Run:
```
pip install -r requirements.txt	
```

### Executing program

- Store your username in line 8 of `main.py`. For example, if your username is "myusername", line 8 should look like this: `YOUR_GEONAME_USERNAME = "myusername"`
- Run the following in your IDE:
```
python3 main.py
```
- Open the `location.html` to see the map.

### Known bugs

- Tracing lines get broken at certain location
- You tell me?

## Acknowledgments
* [Where The ISS At?](https://wheretheiss.at/)
* [GeoNames](https://geonames.org)
* [Plotly](https://plotly.org)