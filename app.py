from flask import Flask, render_template, redirect, url_for
from models import League
import json

app = Flask(__name__)

# Initialize league
with open('data/teams.json', 'r') as f:
    teams = json.load(f)
league = League(teams)
league.generate_fixtures()

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/teams')
def teams():
    return render_template('team.html', teams=league.teams)

@app.route('/fixture/<int:week>')
def fixture(week):
    fixtures = league.get_fixtures(week - 1)
    return render_template('fixture.html', fixtures=fixtures, week=week)

@app.route('/simulate/<int:week>')
def simulate(week):
    league.simulate_week(week - 1)
    return redirect(url_for('results', week=week))

@app.route('/results/<int:week>')
def results(week):
    results = league.get_results(week - 1)
    end_of_season = week == 38
    return render_template('results.html', results=results, week=week, end_of_season=end_of_season)

@app.route('/standings')
def standings():
    standings = league.get_standings()
    end_of_season = league.current_week == 38
    return render_template('standings.html', standings=standings, current_week=league.current_week, end_of_season=end_of_season)

@app.route('/promoted')
def promoted():
    promoted_teams = league.get_promoted_teams()
    return render_template('promoted.html', promoted=promoted_teams)

@app.route('/next_season')
def next_season():
    league.next_season()
    return redirect(url_for('standings'))

if __name__ == '__main__':
    app.run(debug=True)
