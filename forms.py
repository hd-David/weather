from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CityForm(FlaskForm):
        city = StringField('City', validators=[
                DataRequired(message="City name is required.")])
        current_weather = SubmitField('Get Current Weather')
        forecast = SubmitField('Get 16-Day Forecast')
