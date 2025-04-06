# The Weather Wire

The Weather Wire is a background application that fetches live weather data from the Open-Meteo API and broadcasts it over OSC (Open Sound Control) on port 7000. It cycles through the 20 biggest cities in the world, updating every 10 seconds.

## Features

- Runs completely in the background with no visible window
- Broadcasts weather data over OSC on port 7000
- Cycles through 20 major cities every 10 seconds
- No configuration required - just install and run
- Fully self-contained macOS application
- Real-time weather data from Open-Meteo API
- Automatic timezone detection for each city

## OSC Messages

The application broadcasts the following OSC messages (all in capital letters):

- `/CITY` - City name
- `/LATITUDE` - City latitude
- `/LONGITUDE` - City longitude
- `/TIME` - Current time in ISO8601 format
- `/TEMPERATURE` - Current temperature in Celsius
- `/WIND_SPEED` - Current wind speed in m/s
- `/HUMIDITY` - Current humidity percentage
- `/TIMEZONE` - Timezone name (e.g., "America/New_York")
- `/TIMEZONE_ABBREVIATION` - Timezone abbreviation (e.g., "EST")
- `/ELEVATION` - Elevation in meters
- `/WEATHER_DESCRIPTION` - Weather description (e.g., "CLEAR SKY", "RAIN")

## Installation

1. Download the latest release of The Weather Wire from the releases page
2. Move the application to your Applications folder
3. Double-click to run

## Usage

1. Launch The Weather Wire from your Applications folder
2. The application will start running in the background
3. Connect your OSC client to localhost:7000 to receive weather data
4. To quit the application, use Activity Monitor to find and quit "The Weather Wire"

## Development

To build the application from source:

1. Clone the repository:
   ```bash
   git clone https://github.com/chasefostermusic/The-Weather-Wire.git
   cd The-Weather-Wire
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Build the application:
   ```bash
   ./build.sh
   ```

The built application will be available in the `dist` directory.

## Requirements

- macOS 10.12 or later
- Python 3.9 or later (for development)
- No additional software required for end users - all dependencies are bundled

## Troubleshooting

If you're not receiving OSC messages:

1. Ensure Wire is running and listening on port 7000
2. Check that no firewall is blocking localhost connections
3. Verify that both applications are running on the same machine
4. Check the application logs at `~/Library/Logs/The Weather Wire/weather_wire.log`

## License

MIT License

## Author

Chase Foster 