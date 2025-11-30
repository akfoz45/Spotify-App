# 🎵 Django Spotify Profile Analysis App

## 🌐 Live Demo

You can try the project live here: **[Spotify Profile Analyzer](https://akf.pythonanywhere.com)**
[![Spotify Profile Analyzer](https://img.shields.io/badge/Canlı_Demo-1DB954?style=for-the-badge&logo=spotify&logoColor=white)](https://akf.pythonanywhere.com)
[![Visit Site](https://img.shields.io/badge/Web_Sitesi-000000?style=for-the-badge&logo=google-chrome&logoColor=white)](https://akf.pythonanywhere.com)
[![Open in Browser](https://img.shields.io/badge/Open_in_Browser-4285F4?style=flat-square&logo=google-chrome&logoColor=white)](https://akf.pythonanywhere.com)
---

This project is a Django web application that allows users to log in with their Spotify accounts to analyze and visualize their listening habits. It presents the user's top tracks, artists, and music genres in a stylish interface.

## 🚀 Features

* **Spotify OAuth2 Authentication:** Secure login using Spotify accounts.
* **Data Analysis:**
    * **Top Artists:** Filterable by last month, last 6 months, and all time.
    * **Top Tracks:** Lists tracks with album art and artist details.
    * **Recently Played:** Displays the user's most recently played tracks.
    * **Music Taste Chart:** A dynamic "Doughnut" chart visualizing the genres of listened artists (using Chart.js).
* **Data Caching:** User data is saved to the SQLite database at specific intervals to avoid hitting API rate limits and to improve performance.
* **Modern Interface:** Responsive dark theme design built with Bootstrap 5.
* **Token Management:** Seamless session management with access token refreshing mechanisms.

## 🛠️ Tech Stack

* **Backend:** Python 3.x, Django 5.2
* **API Integration:** [Spotipy](https://spotipy.readthedocs.io/) (Spotify Web API Wrapper)
* **Frontend:** HTML5, CSS3, Bootstrap 5
* **Data Visualization:** Chart.js
* **Database:** SQLite3
* **Other Libraries:** `python-dotenv`, `requests`, `pillow`

## ⚙️ Installation

Follow the steps below to run the project on your local machine.

### 1. Clone the Project

```bash
git clone <repo-url>
cd spotifyproject
```
### 2. Create a Virtual Environment

It is recommended to create a virtual environment to isolate Python libraries.

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Requirements
```bash
pip install -r requirements.txt
```
### 4. Spotify Developer Settings
To run this application, you need to create an app on the Spotify Developer Dashboard.

 1.Go to the Spotify Developer Dashboard and log in.

 2.Click on the "Create App" button.

 3.Once created, go to the Settings section.

 4.Note down the Client ID and Client Secret.

 5.Add the following address to the Redirect URIs section and save: http://127.0.0.1:8000/spotifyapp/callback/

### 5. Set Environment Variables (.env)
Create a file named .env inside the spotifyproject/ folder (the same directory as settings.py) and enter your credentials as shown below:
```bash
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
DJANGO_SECRET_KEY=django-insecure-your-random-secret-key
DEBUG=True
```
### 6. Apply Database Migrations
```bash
python manage.py migrate
```
### 7. Run the Application
```bash
python manage.py runserver
```
Open your browser and navigate to http://127.0.0.1:8000/. You will be redirected to the login page.

## 📂 Project Structure
```text
spotifyproject/
├── manage.py
├── requirements.txt
├── spotifyproject/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── spotifyapp/              # Main application
    ├── admin.py
    ├── apps.py
    ├── migrations/          # Database migrations
    ├── models.py            # Database models (Profile, Artist, Track)
    ├── tests.py             # Unit tests
    ├── urls.py              # App-specific routing
    ├── views.py             # OAuth and API logic
    └── templates/
        └── spotifyapp/
            └── profile.html # Profile interface
```
## 📝 Notes

* ** The application uses user-top-read and user-read-recently-played scopes.

* ** When saving data to the database, the last_updated field is checked; if the data is older than 1 hour or if the user changes the time range filter, fresh data is fetched from the API.

## 📄 License
This project was developed for educational purposes.