# Rasmus's Weather Tracker

## Description
A Python application that fetches real-time weather data and stores it in a database. Built for [CSIS 1230 - Programming for Everyone II].

### Features
- Fetches weather data from Open-Meteo API
- Stores data in PostgreSQL database  
- Displays weather data for requested cities on HTML page

## Installation

### Prerequisites
- PostgreSQL

### Steps
1. **Clone this repository:**
   ```bash
   git clone https://github.com/frasse007/web-project.git
   cd web-project
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up database**
   ```bash
   createdb weather-tracker
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

## Usage

### Web Interface
1. ```bash
   python app.py
2. 
3. 

## Project Structure
```
web-project/
├── templates/                # HTML Pages
├── tests/                    # Test files
├── docs/                     # Documentation
├── open_meteo_client.py      # API Client
├── routes.py                 # API Routes
├── app.py                    # Source code
└── README.md
```               

## Technologies Used
- Python 3
- PostgreSQL
- SQLAlchemy
- Open-Meteo API