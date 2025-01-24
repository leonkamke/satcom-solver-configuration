from datetime import datetime
from docplex.mp.model import Model
from ..utils import readProblemInstance, plotOptimizationResult

problemInstance = readProblemInstance()
serviceTargets = problemInstance[0]
satellitePasses = problemInstance[1]

# Set parameters for optimization problem
V = list(range(len(satellitePasses)))
S = list(range(len(serviceTargets)))

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
F_max = 7   # Maximum number of contacts per orbit
C_max = 100

# Create model
model = Model(name="Satellite Optimization")

# Decision variables
x = model.binary_var_matrix(V, S, name="x")

# Objective function
model.maximize(
    model.sum(x[i, j] * bi[i] for i in V for j in S) +
    model.sum(x[i, j] * pj[j] for i in V for j in S)
)

# Constraints
print("Start defining constraints")

# Non-overlapping satellite passes
for i in V:
    for j in V:
        if ti[i] < ti[j]:
            model.add_constraint(
                ti[i] + di[i] + T_min <= ti[j] + 
                (2 - model.sum(x[i, k] for k in S) - model.sum(x[j, k] for k in S)) * 99999999
            )

# Maximum number of contacts per orbit
model.add_constraint(model.sum(x[i, j] for j in S for i in V) <= C_max)

# Each satellite pass has at most one service target
for i in V:
    model.add_constraint(model.sum(x[i, j] for j in S) <= 1)

# The node in the service target and satellite pass must match
for i in V:
    for j in S:
        model.add_constraint(x[i, j] * (ni[i] - sj[j]) == 0)

# The operation mode must match
for i in V:
    for j in S:
        model.add_constraint(x[i, j] * oi[i] * (oi[i] - mj[j]) == 0)

# Each service target can be served at most once
for j in S:
    model.add_constraint(
        model.sum(x[i, j] for i in V) <= 1
    )

# Optimize the model
print("Start optimization")
solution = model.solve()

if solution:
    print("Optimal solution found!")
else:
    print("No optimal solution found.")

# Display the results
contacts = []
for i in V:
    for j in S:
        if x[i, j].solution_value > 0.5:
            contact = {}
            contact["satellitePass"] = satellitePasses[i]
            contact["serviceTarget"] = serviceTargets[j]
            contacts.append(contact)

plotOptimizationResult(serviceTargets, satellitePasses, contacts)