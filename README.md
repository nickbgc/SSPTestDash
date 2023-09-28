# Heatmap Dash App

This repository contains a Dash app that fetches data from an external API, geocodes addresses to latitude and longitude coordinates, and displays the data as a heatmap on a map.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [License](#license)

## Installation

### 1. Clone the Repository:
   ```sh
   git clone https://github.com/your-username/heatmap-dash-app.git
   cd heatmap-dash-app
   ```

### 2. Create a Virtual Environment:
   ```sh
   python -m venv venv
   ```

### 3. Activate the Virtual Environment:
   - On Windows:
     ```sh
     .\venv\Scripts\activate
     ```
   - On Unix or MacOS:
     ```sh
     source venv/bin/activate
     ```

### 4. Install the Required Packages:
   ```sh
   pip install dash requests plotly pandas geopy
   ```

## Usage

### 1. Start the Dash App:
   ```sh
   python app.py
   ```

### 2. Open a Web Browser:
   - Navigate to [http://127.0.0.1:8050/](http://127.0.0.1:8050/) to view and interact with the app.

### 3. Load Data and View Heatmap:
   - Click the "Load Data" button to fetch data from the API, geocode addresses, and display the heatmap on the map.

## How It Works

- **Dash App Layout:**
  The app layout consists of a button ('Load Data') and a Graph component. When the button is clicked, a callback function is triggered to update the graph.

- **Fetching Data:**
  The callback function makes an HTTP GET request to the specified API URL to retrieve data. The API is expected to return a JSON object containing a list of addresses.

- **Geocoding Addresses:**
  The app iterates over the list of addresses and uses the `geolocator.geocode` method from the `geopy` library to convert each address into latitude and longitude coordinates.

- **Creating Heatmap:**
  The `px.density_mapbox` method from the `plotly.express` library is used to create a heatmap figure using the latitude and longitude coordinates. The heatmap is centered on the US, with a specified zoom level and map style.

- **Displaying Heatmap:**
  The heatmap figure is returned from the callback function and displayed in the Graph component of the Dash app.

- **Error Handling and Debugging:**
  The code includes error handling and print statements for debugging, addressing potential issues with API requests, data structure, geocoding, and figure construction.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
