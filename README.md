---

# Weather Dashboard Application

## Overview

This project is a **Weather Dashboard Application** designed to display real-time and historical weather data from a weather station connected to a Misol tablet. The data is fetched and stored in MongoDB and visualized through interactive charts. The dashboard includes features like current weather conditions, historical data trends, and predictions based on machine learning models.

## Features

- **Current Weather Data**: Display of real-time weather parameters such as temperature, humidity, wind speed, etc.
- **Historical Data**: Visualization of weather trends over days, weeks, and months.
- **Predictions**: Forecast for the next 7 days using machine learning models.
- **Responsive Design**: The dashboard adapts to various screen sizes for an optimal viewing experience.
- **Data Storage**: Uses MongoDB for storing and managing weather data.
- **Interactive Charts**: Interactive visualizations using Plotly for an enhanced user experience.

## Technologies Used

- **Frontend**: 
  - HTML, CSS
  - JavaScript
  - Tailwind CSS, Daisy UI

- **Backend**:
  - Django Framework
  - Python

- **Database**:
  - MongoDB (for storing weather data)
  
- **Data Visualization**:
  - Plotly (for interactive charts)

- **Machine Learning**:
  - Scikit-Learn (for weather predictions)

## Project Structure

```
weatherApp/
│
├── weatherApplication/           # Main Django application
│   ├── migrations/               # Database migrations
│   ├── static/                   # Static files (CSS, JavaScript)
│   │   ├── WeatherApp/
│   │       ├── CSS/
│   │       └── JS/
│   ├── templates/                # HTML templates
│   ├── views.py                  # Django views
│   ├── models.py                 # Django models
│   └── ...
│
├── requirements.txt              # Python dependencies
├── README.md                     # Project README
└── manage.py                     # Django management script
```

## Setup & Installation

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/weather-dashboard.git
    cd weather-dashboard
    ```

2. **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up MongoDB:**
    - Ensure MongoDB is installed and running.
    - Update the `settings.py` file with your MongoDB connection details.

5. **Run Migrations:**
    ```bash
    python manage.py migrate
    ```

6. **Start the Server:**
    ```bash
    python manage.py runserver
    ```

7. **Access the Dashboard:**
    - Open your web browser and go to: `http://127.0.0.1:8000/`

## Usage

- Navigate to the dashboard to view real-time weather data.
- Explore historical trends through interactive charts.
- Check predictions for future weather conditions.

## Future Improvements

- Add more weather parameters and improve the prediction model.
- Implement user authentication for personalized dashboards.
- Integrate additional weather APIs for broader data sources.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
