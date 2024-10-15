# Weather Application

## Overview

The Weather Application is a web-based platform that allows users to fetch current weather conditions and 16-day weather forecasts for various cities. Built using Flask for the backend and CSS, HTLM for the frontend, the application provides a user-friendly interface and utilizes the Weatherbit API to retrieve real-time weather data.

## Features

- **Current Weather**: Users can input a city name to get the current weather conditions, including temperature, humidity, wind speed, and a brief description.
- **16-Day Forecast**: Users can request a 16-day weather forecast for their chosen city, providing insights into upcoming weather patterns.
- **Search History**: The application saves the last five searched cities, allowing for quick access to previous weather inquiries.
- **Responsive Design**: The application is designed to be responsive and works well on various devices.

## Technologies Used

- **Backend**: Flask
- **Frontend**:  HTML, CSS
- **Database**: SQLAlchemy SQLite (for storing search history)
- **API**: Weatherbit API (for fetching weather data)

## Installation

1. Clone the repository:
   ```bash
      git clone https://github.com/hd-David/weather.git
         cd weather
	 ```

2. set up enviromnet variables
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows use
   `venv\Scripts\activate`

   ```

3. install requirements
```
	pip install -r requirements.txt

```

4. Set environment varibles
```
	API_KEY=your_api_key_here

```

5. Run the application
```
	flask run
```

### Usage

Navigate to http://127.0.0.1:5000/ in your web browser.

Enter the name of the city you wish to check the weather for in the input field.

Click the Current Weather button to retrieve current weather conditions.

Click the Forecast button to view a 16-day weather forecast for the selected city.

The last five searched cities will be displayed for quick access.
