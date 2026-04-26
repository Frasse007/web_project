from flask import Blueprint, request, render_template, redirect, url_for, flash
from sqlalchemy.orm import Session
from open_meteo_client import get_weather, WeatherReport

from db import (
    insert_observation,
    update_observation,
    delete_observation,
    Observation,
    engine
)

weather = Blueprint('weather', __name__)

# Homepage/Default landing site
@weather.route('/')
def home():  
    return render_template('index.html')

# GET /weather/<id> - Returns the saved observation
@weather.route('/weather/<int:observation_id>')
def retrieve(observation_id):
    with Session(engine) as session:
        obs = session.get(Observation, observation_id)
 
    if obs is None:
        flash("Observation not found.", "error")
        return redirect(url_for("weather.home"))
 
    return render_template("weather.html", obs=obs.to_dict())

# POST /create - Creates record for city submitted by HTML form
@weather.route('/create', methods=["POST"])
def create():
    city_name = request.form.get("city", "").strip()
    if not city_name:
        flash("Please enter a city name.", "error")
        return redirect(url_for("weather.home"))
 
    data = get_weather({"name": city_name, "count": 1, "language": "en", "format": "json"})
    if not data:
        flash(f"Could not fetch weather for '{city_name}'. Try another city.", "error")
        return redirect(url_for("weather.home"))
 
    report = WeatherReport(data)
    obs = insert_observation(report)
 
    return redirect(url_for("weather.retrieve", observation_id=obs.id))

# PUT /update/<id> - Updates the allowed fields and returns the new data
@weather.route('/update/<int:observation_id>', methods=["POST"])
def update(observation_id):
    updates = {}
    temperature = request.form.get("temperature", "").strip()
    windspeed = request.form.get("windspeed", "").strip()
    elevation = request.form.get("elevation", "").strip()
 
    try:
        if temperature:
            updates["temperature"] = float(temperature)
        if windspeed:
            updates["windspeed"] = float(windspeed)
        if elevation:
            updates["elevation"] = float(elevation)
    except ValueError:
        flash("Temperature, windspeed and elevation must be numbers.", "error")
        return redirect(url_for("weather.retrieve", observation_id=observation_id))
 
    if not updates:
        flash("Nothing to update, fill in at least one field.", "error")
        return redirect(url_for("weather.retrieve", observation_id=observation_id))
 
    updated = update_observation(observation_id, updates)
    if updated is None:
        flash("Observation not found.", "error")
        return redirect(url_for("weather.home"))
 
    flash("Observation updated successfully.", "success")
    return redirect(url_for("weather.retrieve", observation_id=updated.id))

# DELETE -
@weather.route('/delete/<int:observation_id>', methods=["POST"])
def delete(observation_id):
    deleted = delete_observation(observation_id)
    flash("Observation deleted." if deleted else "Observation not found", "success" if deleted else "error")
    return redirect(url_for('weather.home'))