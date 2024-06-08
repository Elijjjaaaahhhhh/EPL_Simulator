from models import League
import json

with open('data/teams.json', 'r') as f:
    teams = json.load(f)

league = League(teams)
league.generate_fixtures()

for week in range(1, 39):
    league.simulate_week(week - 1)

standings = league.get_standings()
for team in standings:
    print(f'{team.name}: {team.points()} points')
