'''

### Scenario 4: The Sports League (Home & Away)

**Context:** You are scheduling a round-robin tournament for 4 teams (A, B, C, D) over 3 weeks.

**The Rules:**

1. **One Game Per Week:** Every team must play exactly one game per week.
2. **Opponent Matching:** Every team must play every other team exactly once over the course of the season.
3. **Venue Logic:** If Team A plays Team B at Team A's stadium ("Home"), Team B is considered "Away."
4. **Travel Constraint:** No team can play "Away" games for two consecutive weeks.

'''

from ortools.linear_solver import pywraplp
import typing
from typing import Dict, Tuple

teams = ["A", "B", "C", "D"]
weeks = range(1,4)

pairs = [(t1,t2) for i, t1 in enumerate(teams) for t2 in teams[i+1:]]



x: Dict[Tuple[str,str], pywraplp.Variable] = {}