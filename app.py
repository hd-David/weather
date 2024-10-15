from flask import Flask, render_template, request, redirect, url_for, flash
from helper import lookup_weather, lookup_forecast
from forms import CityForm
from models import SearchHistory, dbconnect
from datetime import datetime, timedelta
import os, json, pytz




app = Flask(__name__)



session = dbconnect()

# Cache duration (in minutes)
CACHE_DURATION = 15


SECRET_KEY = os.urandom(64)
app.config['SECRET_KEY'] = SECRET_KEY



# Custom filter to parse JSON
@app.template_filter('fromjson')
def fromjson(json_string):
    try:
        return json.loads(json_string)
    except Exception as e:
        return str(e)

# Convert a naive datetime object to GMT
def convert_to_gmt(naive_datetime):
    local_tz = pytz.timezone('GMT')  # Use 'UTC' as an alternative if you prefer
    gmt_datetime = local_tz.localize(naive_datetime)
    return gmt_datetime


@app.route("/", methods=["GET","POST"])
def index():
    form = CityForm()
    weather = None
    forecast_data = None
    if form.validate_on_submit():
        city = form.city.data
        if form.current_weather.data:

            # Check if there is cached data for this city
            recent_search = session.query(SearchHistory).filter_by(city=city).order_by(SearchHistory.timestamp.desc()).first()

            # Check if cached data is still valid (e.g., 15 minutes old)
            if recent_search and recent_search.timestamp > datetime.utcnow() - timedelta(minutes=CACHE_DURATION):
                weather = recent_search.weather_data 
            else:
                # Fetch new weather data using `lookup_weather`
                weather_data = lookup_weather(f"{city}")
                if weather_data:
                    # Update or add new search record
                    new_search = SearchHistory(city=city, weather_data=json.dumps(weather_data))
                    session.add(new_search)
                    session.commit()

                    # Prepare data to pass to the template
                    weather = {
                    'city': weather_data['city'],
                    'temperature': weather_data['temperature'],  # Assuming the key is 'temp'
                    'feels_like': weather_data['feels_like'],
                    'description': weather_data['description'],  # Access nested data safely
                    'wind_speed': weather_data['wind_speed'],
                    'humidity': weather_data['humidity']
                    }
                else:
                    flash("Could not retrieve valid weather data. Please try again.")
                
        elif form.forecast.data:
            # Logic for fetching 16-day forecast
            forecast_data = lookup_forecast(city)
            if forecast_data:
                return redirect(url_for("forecast", city=city))
            else:
                flash("Could not retrieve forecast data. Please try again.")
   
                                                    
                                                        
    # Fetch the last five searched cities
    last_searched_cities = session.query(SearchHistory).order_by(SearchHistory.timestamp.desc()).limit(5).all()
        

    return render_template("index.html", form=form, weather=weather, last_searched_cities=last_searched_cities)



@app.route("/forecast", methods=["GET"])
def forecast():
    city = request.args.get('city')  # Get city from the query string
    if city:
        forecast_data = lookup_forecast(city)  # Your function to get forecast data
        if forecast_data:
            return render_template("forecast.html", forecast=forecast_data, city=city)
        else:
            return render_template("forecast.html", error="Could not retrieve forecast data.")
    else:
        return render_template("forecast.html", error="City not provided.")

@app.route("/history")
def history():
    searches = session.query(SearchHistory).order_by(SearchHistory.timestamp.desc()).limit(5).all()
    for search in searches:
        # Convert the timestamp to GMT
        search.timestamp = convert_to_gmt(search.timestamp)
    return render_template("history.html", searches=searches)



if __name__ == "__main__":
    app.run(debug=True)
