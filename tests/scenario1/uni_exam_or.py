"""
# The University Final Exams

## Context
You are scheduling exams for 5 different subjects (Math, Physics, Chem, Bio, English) into 3 available time slots (Morning, Afternoon, Evening).

## The Rules

### Completeness
Every subject must be assigned to exactly one time slot.

### Room Capacity
A maximum of 2 exams can happen in the same time slot (because we only have 2 exam halls).

### The Conflict
"Math" and "Physics" cannot be scheduled in the same time slot because half the students take both.

### The Instructor Preference
The "English" exam cannot be scheduled in the Evening slot.
"""

from ortools.linear_solver import pywraplp
import typing


solver: pywraplp.Solver = pywraplp.Solver.CreateSolver("SCIP")

if not solver:
    print("Solver Not FOund")
    exit()

# Input Sets
subjects = ["Math", "Eng", "Chem", "Bio", "Phys"]
slots = ["M", "A", "E"]

x: typing.Dict[typing.Tuple[str,str], pywraplp.Variable] = {}

for sub in subjects:
    for slot in slots:
        x[(sub, slot)] = solver.IntVar(0,1, f'x_{sub}_{slot}')


# Constraints
### Completeness
# Every subject must be assigned to exactly one time slot.
for sub in subjects:
    solver.Add(solver.Sum([x[(sub, slot)] for slot in slots]) == 1)


# ### Room Capacity
# A maximum of 2 exams can happen in the same time slot (because we only have 2 exam halls).

for slot in slots:
    solver.Add(solver.Sum([x[(sub, slot)] for sub in subjects]) <= 2)

# ### The Conflict
# "Math" and "Physics" cannot be scheduled in the same time slot because half the students take both.

for slot in slots:
    solver.Add(x[("Math", slot)] + x[("Phys", slot)] <= 1 )

solver.Add(x[("Eng", "E")] == 0)

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print(f"Status Optimal/Feasible: {status} (Note: Optimal is {pywraplp.Solver.OPTIMAL} meanwhile \
          Feasible is {pywraplp.Solver.FEASIBLE} and \
            non Feasible is {pywraplp.Solver.ABNORMAL}"
    print(f"propoesd Schdule")
    print('-'*20)

    for slot in slots:
        print(f"{slot} :")
        exam_scheds = []
        for sub in subjects:
            if x[(sub, slot)].solution_value() > 0.5:
                exam_scheds.append(sub)
        print(f" {', '.join(exam_scheds)}\n")
else:
    print("No Schdule Found")


# ### The Instructor Preference
# The "English" exam cannot be scheduled in the Evening slot.



