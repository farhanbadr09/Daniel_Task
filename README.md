# Simple data mapping

## Dependencies: pydantic, bs4, requests
* python -m pip install pydantic bs4 requests

## How to run:
* Open the console, and run the main python file named main.py, make sure models.py is also in the same directory, and that dependencies are installed. Run this command:
	python main.py

## What the script does:
* The script will fetch articles from the API every 5 minutes, map them to the format specified in models.py, then print them out.

## Modules:
* requests: used to send a GET requests to the API
* bs4: used to strip HTML tags from sections that contain text
* datetime: convert string object to datetime object, get current time for log
* time: stop the excution of the script for 5 minutes
* json: print JSON in a good format
* log file: create a log.txt file in base directory with outputs and time of generating log file will be in header of log file

## Time it took to finish: 3 hours
