'''

### Scenario 4: The Sports League (Home & Away)

**Context:** You are scheduling a round-robin tournament for 4 teams (A, B, C, D) over 3 weeks.

**The Rules:**

1. **One Game Per Week:** Every team must play exactly one game per week.
2. **Opponent Matching:** Every team must play every other team exactly once over the course of the season.
3. **Venue Logic:** If Team A plays Team B at Team A's stadium ("Home"), Team B is considered "Away."
4. **Travel Constraint:** No team can play "Away" games for two consecutive weeks.

'''
import pulp

teams = ["A", "B", "C", "D"]
weeks = [1, 2, 3]

# Generate all unique pairs for the Round Robin constraint
pairs = [(t1, t2) for i, t1 in enumerate(teams) for t2 in teams[i+1:]]

model = pulp.LpProblem("Sports_Scheduling", pulp.LpMinimize)

# Variables: x[week][home_team][away_team]
x = pulp.LpVariable.dicts("Match", (weeks, teams, teams), 0, 1, pulp.LpBinary)

# 1. One Game Per Week
for w in weeks:
    for t in teams:
        # Sum of games where t is Home + games where t is Away = 1
        home_games = pulp.lpSum(x[w][t][opponent] for opponent in teams if opponent != t)
        away_games = pulp.lpSum(x[w][opponent][t] for opponent in teams if opponent != t)
        model += home_games + away_games == 1

# 2. Round Robin (Play exactly once)
for t1, t2 in pairs:
    # Sum of (t1 vs t2) + (t2 vs t1) across all weeks = 1
    total_matches = pulp.lpSum(x[w][t1][t2] + x[w][t2][t1] for w in weeks)
    model += total_matches == 1

# 3. Travel Constraint (No Consecutive Aways)
for t in teams:
    for w in [1, 2]: # Check week 1-2 and 2-3
        # Is t Away in week w?
        away_w = pulp.lpSum(x[w][opponent][t] for opponent in teams if opponent != t)
        # Is t Away in week w+1?
        away_next = pulp.lpSum(x[w+1][opponent][t] for opponent in teams if opponent != t)
        
        # Cannot be Away in both
        model += away_w + away_next <= 1

model.solve()

print("Season Schedule:")
print("-" * 30)
for w in weeks:
    print(f"Week {w}:")
    for t1 in teams:
        for t2 in teams:
            if t1 != t2 and pulp.value(x[w][t1][t2]) == 1:
                print(f"  {t1} (Home) vs {t2} (Away)")