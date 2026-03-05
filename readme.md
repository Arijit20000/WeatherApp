# Weather App (Python Tkinter)
A simple desktop weather application built using Python and Tkinter. The application fetches real-time weather data for any city and also displays a short forecast using the OpenWeatherMap API.

## Features

* Search weather by city name
* Display current temperature and feels-like temperature
* Show humidity and wind speed
* Show weather condition and description
* Display a 5-day forecast
* Light and dark theme toggle
* Weather icons based on conditions

## Technologies Used

* Python
* Tkinter for GUI
* Requests library
* OpenWeatherMap API
* python-dotenv for hiding API key

## API Key Setup

This project uses the OpenWeatherMap API.

Create a `.env` file in the project folder and add your API key:

API_KEY=your_api_key_here

Install the required libraries:

pip install requests python-dotenv

## Running the Application

Run the following command in the project directory:

python weatherApp.py

    ## Project Structure

    WeatherApp
    │
    ├── weatherApp.py
    ├── README.md
    ├── .gitignore
    ├── Sun.png
    ├── Cloud.png
    ├── Rain.png
    ├── Mist.png
    ├── Moon.png

## Important Note

The `.env` file is not uploaded to GitHub to keep the API key secure.

## Author

Arijit
