from datetime import datetime
from pyscipopt import Model, quicksum
from ..utils import *

# Read problem instance
problemInstance = readProblemInstance()
satellite_passes = problemInstance["satellite_passes"]
service_targets = problemInstance["service_targets"]

# Set parameters for optimization problem
V = list(range(len(satellite_passes)))
S = list(range(len(service_targets)))

d = {}
t = {}
b = {}
n = {}
f = {}

reference_time = datetime.fromisoformat(satellite_passes[0]["startTime"])
for satellitePass in satellite_passes:
    id = satellitePass["id"]
    start_time = datetime.fromisoformat(satellitePass["startTime"])
    end_time = datetime.fromisoformat(satellitePass["endTime"])

    # Calculate relative start time (seconds from reference_time)
    start_seconds = (start_time - reference_time).total_seconds()
    t[id] = start_seconds

    # Calculate duration (seconds)
    duration_seconds = (end_time - start_time).total_seconds()
    d[id] = duration_seconds

    b[id] = satellitePass["achievableKeyVolume"]

    n[id] = satellitePass["nodeId"]

    f[id] = satellitePass["orbitId"]

p = {}
s = {}
m = {}
for serviceTarget in service_targets:
    id = serviceTarget["id"]
    p[id] = serviceTarget["priority"]
    s[id] = serviceTarget["nodeId"]
    m[id] = 0 if serviceTarget["requestedOperation"] == "QKD" else 1

T_min = 6  # Minimum time between consecutive contacts
# F_max = 20  # Maximum number of contacts per orbit
C_max = 99999999

# Create SCIP model
model = Model("Satellite Optimization")

# Decision variables
x = {}
for i in V:
    for j in S:
        x[i, j] = model.addVar(vtype="B", name=f"x_{i}_{j}")

# Objective function
model.setObjective(
    quicksum(x[i, j] * (1 + b[i] * p[j]) for i in V for j in S), # + quicksum(x[i, j] * pj[j] for i in V for j in S),
)

print("Start defining constraints")
# Constraints
# Non-overlapping satellite passes
for i in V:
    for j in V:
        if t[i] < t[j]:
            model.addCons(
                t[i] + d[i] + T_min <= t[j] + (2 - quicksum(x[i, k] for k in S) - quicksum(x[j, k] for k in S)) * 99999999
            )

# Maximum number of contacts per orbit
"""for f in set(fi.values()):
    model.addCons(
        quicksum(x[i, j] for i in V for j in S if fi[i] == f) <= F_max
    )"""

# Maximum number of contacts in total
model.addCons(quicksum(x[i, j] for j in S for i in V) <= C_max)

# Each satellite pass has at most one service target
for i in V:
    model.addCons(quicksum(x[i, j] for j in S) <= 1)

# The node in the service target and satellite pass must match
for i in V:
    for j in S:
        model.addCons(x[i, j] * (n[i] - s[j]) == 0)

# The operation mode must match
"""for i in V:
    for j in S:
        model.addCons(x[i, j] * oi[i] * (oi[i] - mj[j]) == 0)"""

# Each service target can be served at most once
for j in S:
    model.addCons(
        quicksum(x[i, j] for i in V) <= 1
    )

# Optimize the model
model.optimize()

# Display the results
if model.getStatus() == "optimal":
    print("Optimal solution found!")
else:
    print("No optimal solution found.")

contacts = []
for i in V:
    for j in S:
        if model.getVal(x[i, j]) > 0.5:
            contact = {}
            contact["satellitePass"] = satellite_passes[i]
            contact["serviceTarget"] = service_targets[j]
            contacts.append(contact)

print("Performance of the solution is: " + str(round(calculateObjectiveFunction(contacts), 2)))
# plotOptimizationResult(service_targets, satellite_passes, contacts, "scip")
