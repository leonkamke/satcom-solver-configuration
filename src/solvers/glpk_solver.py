from datetime import datetime
from pulp import LpProblem, LpVariable, LpBinary, LpMaximize, lpSum, value
from ..utils import *

# Read problem instance
problemInstance = read_problem_instance("./src/input/data/problem_instance_europe_6h.json")
satellitePasses = problemInstance["satellite_passes"]
serviceTargets = problemInstance["service_targets"]

# Set parameters for the optimization problem
V = list(range(len(satellitePasses)))
S = list(range(len(serviceTargets)))

di = {}
ti = {}
bi = {}
ni = {}
fi = {}
oi = {}

reference_time = datetime.fromisoformat(problemInstance["coverage_start"])
for idx, satellitePass in enumerate(satellitePasses):
    start_time = datetime.fromisoformat(satellitePass["startTime"])
    end_time = datetime.fromisoformat(satellitePass["endTime"])

    start_seconds = (start_time - reference_time).total_seconds()
    end_seconds = (end_time - reference_time).total_seconds()

    ti[idx] = start_seconds
    di[idx] = end_seconds - start_seconds
    bi[idx] = satellitePass["achievableKeyVolume"]
    oi[idx] = 1 if satellitePass["achievableKeyVolume"] == 0.0 else 0
    ni[idx] = satellitePass["nodeId"]
    fi[idx] = satellitePass["orbitId"]

pj = {}
sj = {}
mj = {}
aj = {}
for idx, serviceTarget in enumerate(serviceTargets):
    pj[idx] = serviceTarget["priority"]
    sj[idx] = serviceTarget["nodeId"]
    mj[idx] = 1 if serviceTarget["requestedOperation"] == "QKD" else 0
    aj[idx] = serviceTarget["applicationId"]

T_min = 60  # Minimum time between consecutive contacts in seconds

# Create GLPK model
model = LpProblem("GLPK_Satellite_Optimization", LpMaximize)

# Decision variables
x = LpVariable.dicts("x", [(i, j) for i in V for j in S], cat=LpBinary)

# Objective function
model += lpSum(x[i, j] * pj[j] * (1 + bi[i] * mj[j]) for i in V for j in S)

# Constraints
print("Start defining constraints")

# Each satellite pass has at most one service target
for i in V:
    model += lpSum(x[i, j] for j in S) <= 1

# Each service target can be served at most once
for j in S:
    model += lpSum(x[i, j] for i in V) <= 1

# Non-overlapping satellite passes
for i1 in V:
    for i2 in V:
        if i1 != i2 and ti[i1] <= ti[i2]:
            model += (
                ti[i1] + di[i1] + T_min
                <= ti[i2] + (2 - lpSum(x[i1, k] for k in S) - lpSum(x[i2, k] for k in S)) * 99999
            )

# The node in the service target and satellite pass must match
for i in V:
    for j in S:
        model += x[i, j] * (ni[i] - sj[j]) == 0

# The operation mode must match
for i in V:
    for j in S:
        model += x[i, j] * oi[i] * (oi[i] - mj[j] - 1) == 0

# For a given application id, first do QKD and afterwards QKD post-processing
for j1 in S:
    for j2 in S:
        if aj[j1] == aj[j2] and mj[j1] == 1 and mj[j2] == 0:
            model += lpSum(ti[i] * x[i, j1] for i in V) <= lpSum(ti[i] * x[i, j2] for i in V)

# QKD post-processing and QKD must happen in the same schedule
for j1 in S:
    for j2 in S:
        if aj[j1] == aj[j2] and mj[j1] == 1 and mj[j2] == 0:
            model += lpSum(x[i, j1] for i in V) == lpSum(x[i, j2] for i in V)

# Solve the model using GLPK
model.solve()

# Display the results
if model.status == 1:
    print("Optimal solution found!")
else:
    print("No optimal solution found.")

contacts = []
for i in V:
    for j in S:
        if value(x[i, j]) > 0.5:
            contact = {}
            contact["satellitePass"] = satellitePasses[i]
            contact["serviceTarget"] = serviceTargets[j]
            contacts.append(contact)

print("Performance of the solution is: " + str(round(calculateObjectiveFunction(contacts), 2)))
plotOptimizationResult(serviceTargets, satellitePasses, contacts, "glpk")