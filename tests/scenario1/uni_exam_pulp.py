import pulp

# Model Initialization
model = pulp.LpProblem("Exam_Scheduling", pulp.LpMinimize)

# Input Sets
subjects = ["Math", "Eng", "Chem", "Bio", "Phys"]
slots = ["M", "A", "E"]

# Decision Variables
x = pulp.LpVariable.dicts("Schdeule", (subjects, slots), cat=pulp.LpBinary)

# Constraints


# Every subject must be assigned to exactly one time slot.
for sub in subjects:
    model += pulp.lpSum([x[sub][slot] for slot in slots]) == 1


# A maximum of 2 exams can happen in the same time slot (because we only have 2 exam halls).
for slot in slots:
    model += pulp.lpSum([x[sub][slot] for sub in subjects]) <= 2

# "Math" and "Physics" cannot be scheduled in the same time slot because half the students take both.
for slot in slots:
    model += x["Math"][slot] + x["Phys"][slot] <= 1

# The "English" exam cannot be scheduled in the Evening slot.
model += x["Eng"]["E"] == 0

model.solve()


print(f"Status {pulp.LpStatus[model.status]}\n")


if pulp.LpStatus[model.status] == "Optimal":
    print("Proposed Schedule")
    print("-" * 20 )
    for slot in slots:
        print(f"{slot}: ")
        exam_in_slots = []
        for sub in subjects:
            if pulp.value(x[sub][slot]) == 1:
                exam_in_slots.append(sub)
        print(f" {', '.join(exam_in_slots) }")
else:
    print("No Schedule found.")
