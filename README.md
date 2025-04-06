# The Weather Wire

The Weather Wire is a background application that fetches live weather data from the Open-Meteo API and broadcasts it over OSC (Open Sound Control) on port 7001. It cycles through the 20 biggest cities in the world, updating every 10 seconds.

## Features

- Runs completely in the background with no visible window
- Broadcasts weather data over OSC on port 7001
- Cycles through 20 major cities every 10 seconds
- No configuration required - just install and run
- Fully self-contained macOS application

## OSC Messages

The application broadcasts the following OSC messages (all in capital letters):

- `/CITY` - City name
- `/LATITUDE` - City latitude
- `/LONGITUDE` - City longitude
- `/TIME` - Current time in ISO8601 format
- `/TEMPERATURE` - Current temperature in Celsius
- `/WIND_SPEED` - Current wind speed in km/h
- `/HUMIDITY` - Current humidity percentage
- `/TIMEZONE` - Timezone name
- `/TIMEZONE_ABBREVIATION` - Timezone abbreviation
- `/ELEVATION` - Elevation in meters
- `/WEATHER_DESCRIPTION` - Weather description (e.g., "CLEAR SKY", "RAIN")

## Installation

1. Download the latest release of The Weather Wire from the releases page
2. Move the application to your Applications folder
3. Double-click to run

## Usage

1. Launch The Weather Wire from your Applications folder
2. The application will start running in the background
3. Connect your OSC client to localhost:7001 to receive weather data
4. To quit the application, use Activity Monitor to find and quit "The Weather Wire"

## Development

To build the application from source:

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Build the application: `python setup.py py2app`

## Requirements

- macOS 10.12 or later
- No additional software required - all dependencies are bundled

## License

MIT License 