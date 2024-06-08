class LCMRandom:
    def __init__(self, seed=1):
        self.a = 1664525
        self.c = 1013904223
        self.m = 2**32
        self.seed = seed

    def random(self):
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed / self.m

    def randint(self, low, high):
        return low + int(self.random() * (high - low + 1))
    
    def shuffle(self, lst):
        for i in range(len(lst)-1, 0, -1):
            j = self.randint(0, i)
            lst[i], lst[j] = lst[j], lst[i]

class Team:
    def __init__(self, name, win_prob):
        self.name = name
        self.win_prob = win_prob
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_scored = 0
        self.goals_against = 0

    def update_stats(self, scored, against):
        self.goals_scored += scored
        self.goals_against += against
        if scored > against:
            self.wins += 1
        elif scored < against:
            self.losses += 1
        else:
            self.draws += 1

    def points(self):
        return self.wins * 3 + self.draws

    def goal_difference(self):
        return self.goals_scored - self.goals_against

class League:
    NON_EPL_TEAMS = ["Norwich", "Watford", "Huddersfield", "Derby", "Bristol", "Cardiff", "Middlesbrough", "Swansea", "Reading", "QPR", "Barnsley", "Blackburn", "Millwall", "Stoke", "Preston", "Birmingham", "Hull", "Coventry", "Rotherham", "Sheffield Wed"]

    def __init__(self, teams, seed=1):
        self.teams = [Team(name, prob) for name, prob in teams.items()]
        self.fixtures = []
        self.results = []
        self.history = []
        self.current_week = 0
        self.random = LCMRandom(seed)

    def generate_fixtures(self):
        teams = self.teams[:]
        num_teams = len(teams)
        home_away_fixtures = []

        # Create home and away fixtures for each pair of teams
        for i in range(num_teams):
            for j in range(i + 1, num_teams):
                home_away_fixtures.append((teams[i], teams[j]))  # Home fixture
                home_away_fixtures.append((teams[j], teams[i]))  # Away fixture

        # Shuffle the fixtures to randomize the order
        self.random.shuffle(home_away_fixtures)

        # Distribute fixtures across 38 weeks, ensuring each team plays one match per week
        weeks = [[] for _ in range(38)]
        matchups = {team: [0] * 38 for team in teams}

        week_idx = 0
        while home_away_fixtures:
            fixture = home_away_fixtures.pop(0)
            home, away = fixture

            if matchups[home][week_idx] < 1 and matchups[away][week_idx] < 1:
                weeks[week_idx].append(fixture)
                matchups[home][week_idx] += 1
                matchups[away][week_idx] += 1

                if len(weeks[week_idx]) == 10:
                    week_idx += 1

        self.fixtures = weeks

    def get_fixtures(self, week):
        if week < len(self.fixtures):
            return self.fixtures[week]
        return []

    def simulate_week(self, week):
        week_fixtures = self.get_fixtures(week)
        week_results = []
        for home, away in week_fixtures:
            home_prob = home.win_prob + 0.2
            away_prob = away.win_prob
            result = self.simulate_match(home_prob, away_prob)
            home_score, away_score = result
            home.update_stats(home_score, away_score)
            away.update_stats(away_score, home_score)
            week_results.append((home.name, away.name, home_score, away_score))
        self.results.append(week_results)
        self.current_week += 1

    def simulate_match(self, home_prob, away_prob):
        if home_prob > away_prob:
            home_score, away_score = self.generate_score(home_prob, away_prob, True)
        else:
            home_score, away_score = self.generate_score(home_prob, away_prob, False)
        return home_score, away_score

    def generate_score(self, home_prob, away_prob, home_wins):
        score_diff = abs(home_prob - away_prob)
    
        # Determine the maximum possible score
        if score_diff < 0.15:
            max_score = max(2, self.random.randint(2, 3))
            max_goal_diff = 2
        elif score_diff < 0.3:
            max_score = max(1, self.random.randint(0, 4))
            max_goal_diff = 2
        else:
            max_score = max(1, self.random.randint(0, 6))
            max_goal_diff = 3

        # Generate scores based on the outcome
        if home_wins:
            home_score = self.random.randint(1, max_score)
            if max_goal_diff > home_score:
                away_score = self.random.randint(0, home_score)
            else:
                away_score = self.random.randint(max(0, home_score - max_goal_diff), min(max_score - 1, home_score + max_goal_diff - 1))
        else:
            away_score = self.random.randint(1, max_score)
            if max_goal_diff > away_score:
                home_score = self.random.randint(0, away_score)
            else:
                home_score = self.random.randint(max(0, away_score - max_goal_diff), min(max_score - 1, away_score + max_goal_diff - 1))

        return home_score, away_score

    def get_results(self, week):
        return self.results[week]

    def get_standings(self):
        # Sort by points, goal difference, goals scored
        standings = sorted(self.teams, key=lambda x: (x.points(), x.goal_difference(), x.goals_scored), reverse=True)
        # If no matches have been played, sort alphabetically
        if all(team.wins == 0 and team.draws == 0 and team.losses == 0 for team in self.teams):
            standings = sorted(self.teams, key=lambda x: x.name)
        return standings

    def get_promoted_teams(self):
        relegated_teams = sorted(self.teams, key=lambda x: x.points())[:3]
        promoted_teams = [self.NON_EPL_TEAMS[self.random.randint(0, len(self.NON_EPL_TEAMS)-1)] for _ in range(3)]
        for team in relegated_teams:
            self.teams.remove(team)
        self.teams.extend([Team(name, self.random.random()) for name in promoted_teams])
        return promoted_teams

    def next_season(self):
        self.history.append({
            'standings': self.get_standings(),
            'results': self.results
        })
        self.adjust_win_probabilities()
        self.fixtures = []
        self.results = []
        self.current_week = 0
        for team in self.teams:
            team.wins = 0
            team.draws = 0
            team.losses = 0
            team.goals_scored = 0
            team.goals_against = 0
        self.generate_fixtures()

    def adjust_win_probabilities(self):
        # Reduce win probability for top teams
        top_teams = self.get_standings()[:4]
        for _ in range(12):
            for team in self.random.sample(top_teams, k=4):
                team.win_prob = max(0, team.win_prob - 0.189)
        
        # Improve win probability for promoted teams
        promoted_teams = self.get_standings()[-3:]
        for team in promoted_teams:
            team.win_prob = min(1, team.win_prob + 0.189)
