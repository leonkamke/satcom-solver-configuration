from datetime import datetime
from gurobipy import Model, GRB, quicksum
from ..utils import *

# Read problem instance
problemInstance = readProblemInstance()
serviceTargets = problemInstance[0]
satellitePasses = problemInstance[1]


# Set parameters for optimization problem
V = list(range(0, len(satellitePasses)))
S = list(range(0, len(serviceTargets)))

di = {}
ti = {}
bi = {}
oi = {}
ni = {}
fi = {}

reference_time = datetime.fromisoformat(satellitePasses[0]["startTime"])
for satellitePass in satellitePasses:
    id = satellitePass["id"]
    start_time = datetime.fromisoformat(satellitePass["startTime"])
    end_time = datetime.fromisoformat(satellitePass["endTime"])

    # Calculate relative start time (seconds from reference_time)
    start_seconds = (start_time - reference_time).total_seconds()
    ti[id] = start_seconds

    # Calculate duration (seconds)
    duration_seconds = (end_time - start_time).total_seconds()
    di[id] = duration_seconds

    bi[id] = satellitePass["achievableKeyVolume"]

    oi[id] = 0 if satellitePass["possibleOperation"] == "QKD" else 1

    ni[id] = satellitePass["nodeId"]

    fi[id] = satellitePass["orbitId"]

pj = {}
sj = {}
mj = {}

for serviceTarget in serviceTargets:
    id = serviceTarget["id"]
    pj[id] = serviceTarget["priority"]
    sj[id] = serviceTarget["nodeId"]
    mj[id] = 0 if serviceTarget["requestedOperation"] == "QKD" else 1


T_min = 6  # Minimum time between consecutive contacts
# F_max = 7   # Maximum number of contacts per orbit
C_max = 99999999

# Create model
model = Model("Satellite Optimization")

# Decision variables
x = model.addVars(V, S, vtype=GRB.BINARY, name="x")

# Objective function
model.setObjective(
    quicksum(x[i, j] * (1 + bi[i] * pj[j] * mj[j]) for i in V for j in S), # + quicksum(x[i, j] * pj[j] for i in V for j in S),
    GRB.MAXIMIZE
)

# Constraints
print("Start defining constraints")

# Non-overlapping satellite passes
for i in V:
    for j in V:
        if ti[i] < ti[j]:
            model.addConstr(
                ti[i] + di[i] + T_min <= ti[j] + (2 - quicksum(x[i, k] for k in S) - quicksum(x[j, k] for k in S)) * 99999999
            )

# Maximum number of contacts per orbit
"""for f in fi.values():
    model.addConstr(quicksum(x[i, j] for i in V for j in S if fi[i] == f) <= F_max)"""

# Maximum number of contacts in total
model.addConstr(quicksum(x[i, j] for j in S for i in V) <= C_max)

# Each satellite pass has at most one service target
for i in V:
    model.addConstr(quicksum(x[i, j] for j in S) <= 1)

# The node in the service target and satellite pass must match
for i in V:
    for j in S:
        model.addConstr(x[i, j] * (ni[i] - sj[j]) == 0)

# The operation mode must match
"""for i in V:
    for j in S:
        model.addConstr(x[i, j] * oi[i] * (oi[i] - mj[j]) == 0)"""


# Each service target can be served at most once
for j in S:
    model.addConstr(
        quicksum(x[i, j] for i in V) <= 1
    )

# Optimize the model
print("Start optimization")
model.optimize()

# Display the results
if model.status == GRB.OPTIMAL:
    print("Optimal solution found!")
else:
    print("No optimal solution found.")


contacts = []
for i in V:
    for j in S:
        if x[i, j].x > 0.5:
            contact = {}
            contact["satellitePass"] = satellitePasses[i]
            contact["serviceTarget"] = serviceTargets[j]
            contacts.append(contact)


print("Performance of the solution is: " + str(round(calculateObjectiveFunction(contacts), 2)))
plotOptimizationResult(serviceTargets, satellitePasses, contacts, "gurobi")
