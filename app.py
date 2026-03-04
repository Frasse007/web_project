# Import the Flask class
from flask import Flask
from routes import weather

# Create an instance of the Flask class. 
# __name__ helps Flask find template and static files.
app = Flask(__name__)

app.register_blueprint(weather)


# This ensures the server only runs if the script is executed directly.
if __name__ == '__main__':
    app.run(debug=True)