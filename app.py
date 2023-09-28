import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import requests
import pandas as pd
import plotly.express as px
from geopy.geocoders import Nominatim
from flask_login import LoginManager, UserMixin, login_user, current_user
from flask import Flask, render_template, redirect, url_for, request

# Initialize Flask app
server = Flask(__name__)
server.secret_key = 'your-secret-key'  # Change this to a random secret key

# Initialize Dash app with the Flask server
app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = 'login'

# User class
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# User database (replace with your actual user database)
users = {'user1': {'password': 'password1'}, 'user2': {'password': 'password2'}}

# Load user
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Landing page route
@server.route('/')
def home():
    return render_template('index.html')

# Login route
@server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect('/dashboard')
    return render_template('login.html')

# Logout route
@server.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# Define the layout of the dashboard
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Button('Load Data', id='load-button'),
    dcc.Graph(id='example-graph')
])

# Initialize geolocator
geolocator = Nominatim(user_agent="geoapi")

# Define a callback function to update the graph and redirect unauthenticated users
@app.callback(
    Output('example-graph', 'figure'),
    Input('load-button', 'n_clicks'),
    State('url', 'pathname')
)
def update_graph(n_clicks, pathname):
    if not current_user.is_authenticated:
        return dcc.Location(pathname='/login', id='url')
    if n_clicks is None:
        # Prevent the callback from being triggered on app load
        return dash.no_update

    try:
        # Make HTTP request to the external API
        response = requests.get('https://api.example.com/data')
        data = response.json()

        # Extract addresses from the data and geocode them to get latitude and longitude
        latitudes = []
        longitudes = []
        for address in data['addresses']:
            location = geolocator.geocode(f"{address['street']}, {address['city']}, {address['state']}, {address['zip']}")
            if location:
                latitudes.append(location.latitude)
                longitudes.append(location.longitude)

        # Create the heatmap figure
        figure = px.density_mapbox(
            lat=latitudes, lon=longitudes,
            radius=10,
            center=dict(lat=37.0902, lon=-95.7129),  # Center on the US
            zoom=3,
            mapbox_style="stamen-terrain"
        )

        return figure
    except Exception as e:
        print(f"Error: {e}")
        return dash.no_update

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
