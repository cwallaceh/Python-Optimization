# Linear and (mixed) integer programming

import pulp
import pandas as pd

"""
The discrete optimization problem is simple:

Sets
F = set of foods
N = set of nutrients

Parameters
aij = amount of nutrient j in food i, ∀i∈F, ∀j∈N
ci = cost per serving of food i, ∀i∈F
Fmini = minimum number of required servings of food i, ∀i∈F
Fmaxi = maximum allowable number of servings of food i, ∀i∈F
Nminj = minimum required level of nutrient j, ∀j∈N
Nmaxj = maximum allowable level of nutrient j, ∀j∈N

Variables
xi = number of servings of food i to purchase/consume, ∀i∈F

Objective Function: Minimize the total cost of the food

Minimize ∑i∈Fcixi

Constraint Set 1: For each nutrient j∈N, at least meet the minimum required level.
∑i∈Faijxi≥Nminj,∀j∈N

Constraint Set 2: For each nutrient j∈N, do not exceed the maximum allowable level.
∑i∈Faijxi≤Nmaxj,∀j∈N

Constraint Set 3: For each food i∈F, select at least the minimum required number of servings.
xi≥Fmini,∀i∈F

Constraint Set 4: For each food i∈F, do not exceed the maximum allowable number of servings.
xi≤Fmaxi,∀i∈F
"""

# pdb.set_trace()

# Define problem
prob = pulp.LpProblem("Simple Diet Problem", pulp.LpMinimize)

# Read the first few rows dataset in a Pandas DataFrame
df = pd.read_excel("diet.xls", nrows=17)

# Create a list of the food items
foods = df.pop('Foods').tolist()

# Create a dictionary of all variables
costs = dict(zip(foods, df['Price/Serving']))
calories = dict(zip(foods, df['Calories']))
fat = dict(zip(foods, df['Total_Fat (g)']))
carbs = dict(zip(foods, df['Carbohydrates (g)']))

# Continuous (Convex) / Integer (Non-Convex)
# food_vars = pulp.LpVariable.dicts("Food", foods, lowBound=0, cat='Continuous')
food_vars = pulp.LpVariable.dicts("Food", foods, lowBound=0, cat='Integer')

# Objective function
prob += pulp.lpSum([costs[i]*food_vars[i] for i in foods])

# Calories constraints
prob += pulp.lpSum([calories[f] * food_vars[f] for f in foods]) >= 800.0
prob += pulp.lpSum([calories[f] * food_vars[f] for f in foods]) <= 1300.0

# Nutrition constrains
# Fat
prob += pulp.lpSum([fat[f] * food_vars[f] for f in foods]) >= 20.0, "FatMinimum"
prob += pulp.lpSum([fat[f] * food_vars[f] for f in foods]) <= 50.0, "FatMaximum"

# Carbs
prob += pulp.lpSum([carbs[f] * food_vars[f] for f in foods]) >= 130.0, "CarbsMinimum"
prob += pulp.lpSum([carbs[f] * food_vars[f] for f in foods]) <= 200.0, "CarbsMaximum"

# Solve
prob.solve()

# The status of the solution is printed to the screen
print("Status:", pulp.LpStatus[prob.status])

# Print servings
for v in prob.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)

# Print objective function
obj = pulp.value(prob.objective)
print("The total cost of this balanced diet is: ${}".format(round(obj, 2)))
