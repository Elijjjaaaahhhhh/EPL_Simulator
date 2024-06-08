# EPL Simulator

This project is a simulator for the English Premier League (EPL) that allows you to simulate a full season, view fixtures, results, standings, and promoted teams. The project is built using Flask, a lightweight WSGI web application framework in Python.

## Features

- Simulate a full EPL season with 38 game weeks
- View fixtures, results, and standings
- See promoted teams at the end of the season
- Random number generation using the Linear Congruential Method (LCM)

## Directory Structure

```
project-directory/
├── app.py
├── models.py
├── requirements.txt
├── Procfile
├── data/
│   ├── teams.json
│   ├── fixtures.json
│   └── standings.json
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
├── templates/
│   ├── welcome.html
│   ├── team.html
│   ├── fixture.html
│   ├── results.html
│   ├── standings.html
│   └── promoted.html
```

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)
- Git (for cloning the repository)

### Steps

1. **Clone the repository**:

   ```sh
   git clone https://github.com/your-username/your-repository-name.git
   cd your-repository-name
   ```

2. **Create a virtual environment**:

   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

4. **Run the application**:

   ```sh
   flask run
   ```

5. Open your web browser and go to `http://127.0.0.1:5000/` to see the application in action.

## Deployment

To deploy this application to Heroku:

1. **Create a `Procfile`**:

   ```plaintext
   web: python app.py
   ```

2. **Create a `requirements.txt`**:

   ```sh
   pip freeze > requirements.txt
   ```

3. **Initialize a Git repository** (if not already done):

   ```sh
   git init
   git add .
   git commit -m "Initial commit"
   ```

4. **Create a Heroku app**:

   ```sh
   heroku create your-app-name
   ```

5. **Push to Heroku**:

   ```sh
   git push heroku main
   ```

6. **Open your app**:

   ```sh
   heroku open
   ```

## Usage

### Navigating the App

- **Home Page**: Start the simulation and navigate to other sections.
- **Teams Page**: View the list of teams participating in the league.
- **Fixtures Page**: View the fixtures for each game week.
- **Results Page**: View the results of each game week.
- **Standings Page**: View the current standings of the teams.
- **Promoted Teams Page**: View the teams promoted at the end of the season.

### Simulating a Season

1. Start the simulation from the home page.
2. Navigate through each game week to simulate matches.
3. View results and standings as the season progresses.
4. At the end of the season, view the promoted teams and start a new season.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgements

- Flask framework
- Python programming language
