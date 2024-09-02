# Musafir Backend

This is the backend for the Musafir web application, built using Python and Flask. It provides API endpoints for managing user authentication, generating and saving travel itineraries, fetching weather data, and interacting with places of interest.

## Features

- User registration and authentication using Firebase.
- Travel itinerary generation using the Google Gemini API.
- Weather data fetching using the OpenWeatherMap API.
- MongoDB integration for storing user data and itineraries.
- RESTful API structure.

## Requirements

- Python 3.7+
- MongoDB Atlas account (or any other MongoDB instance)
- Firebase project (for authentication)
- Google Gemini API access
- OpenWeatherMap API key

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/musafir-backend.git
   cd musafir-backend
   ```

2. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root and add the following:

   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   MONGODB_URI=your_mongodb_uri
   DATABASE_NAME=your_database_name
   WEATHER_API_KEY=your_openweathermap_api_key
   FIREBASE_API_KEY=your_firebase_api_key
   ```

5. **Run the application**

   ```bash
   flask run
   ```

   The backend should now be running on `http://127.0.0.1:5000`.

## API Endpoints

- **User Registration & Login**: `/register`, `/login`
- **Generate Itinerary**: `/generate-itinerary`, `/generate-itinerary-with-destination`
- **Fetch Weather**: `/get-weather`
- **Save Itinerary**: `/save-itinerary`
- **Fetch Itineraries**: `/fetch-itineraries`
- **User Info**: `/user-info`

## Deployment

The backend can be deployed to platforms like Heroku, Render, or any other service supporting Python and Flask. Ensure that the environment variables are correctly set on the platform you choose.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request.


