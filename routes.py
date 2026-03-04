from flask import Blueprint, request

weather = Blueprint('weather', __name__)

@weather.route('/')
def home():  
    "default route"
    return '<h1>Hello, World! From my first Flask app!</h1>'


@weather.route('/about')
def about():
    return 'This is the About page.'

# GET -
@weather.route('/retrieve')
def retrieve():
    city_name = request.form.get('city')
    return "This is weather GET for a specific city"

# POST - 
@weather.route('/create')
def create():
    return "This is weather POST for a specific city"

# PUT -
@weather.route('/update')
def update():
    return "This is weather PUT for a specific city"

# DELETE -
@weather.route('/delete')
def delete():
    return "This is weather DELETE for a specific city"