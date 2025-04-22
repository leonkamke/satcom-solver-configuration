from datetime import datetime
from pyscipopt import Model, quicksum
from ..utils import *
import time

start = time.time()

# Read problem instance
print("Read problem instance")
problemInstance = read_problem_instance("./src/input/data/problem_instance_europe_dec_3h.json")
satellitePasses = problemInstance["satellite_passes"]
serviceTargets = problemInstance["service_targets"]

print("Start setting up problem and model")
# Set parameters for optimization problem
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
    # id = satellitePass["id"]
    start_time = datetime.fromisoformat(satellitePass["startTime"])
    end_time = datetime.fromisoformat(satellitePass["endTime"])

    # Calculate relative start time and end time (seconds from reference_time)
    start_seconds = (start_time - reference_time).total_seconds()
    end_seconds =   (end_time - reference_time).total_seconds()

    ti[idx] = start_seconds

    # Calculate duration (seconds)
    duration_seconds = end_seconds - start_seconds
    di[idx] = duration_seconds
    bi[idx] = satellitePass["achievableKeyVolume"]
    oi[idx] = 1 if satellitePass["achievableKeyVolume"] == 0.0 else 0
    ni[idx] = satellitePass["nodeId"]
    fi[idx] = satellitePass["orbitId"]

pj = {}
sj = {}
mj = {}
aj = {}
for idx, serviceTarget in enumerate(serviceTargets):
    # id = serviceTarget["id"]
    pj[idx] = serviceTarget["priority"]
    sj[idx] = serviceTarget["nodeId"]
    mj[idx] = 1 if serviceTarget["requestedOperation"] == "QKD" else 0
    aj[idx] = serviceTarget["applicationId"]

T_min = 60  # Minimum time between consecutive contacts in seconds
# F_max = 20  # Maximum number of contacts per orbit
# C_max = 99999999

# Create SCIP model
model = Model("Satellite Optimization")
# model.setParam('display/verblevel', 0)   # Suppress display output

# Computation time limit in seconds
# model.setParam("limits/time", 20)

# Decision variables
x = {}
for i in V:
    for j in S:
        x[i, j] = model.addVar(vtype="B", name=f"x_{i}_{j}")

# Objective function
model.setObjective(
    quicksum(x[i, j] * pj[j] * (1 + bi[i] * mj[j]) for i in V for j in S), # + quicksum(x[i, j] * pj[j] for i in V for j in S),
    # quicksum(x[i, j] for i in V for j in S),
    "maximize"
)

# Constraints
# Each satellite pass has at most one service target
for i in V:
    model.addCons(quicksum(x[i, j] for j in S) <= 1)

# Each service target can be served at most once
for j in S:
    model.addCons(quicksum(x[i, j] for i in V) <= 1)

# Non-overlapping satellite passes
for i1 in V:
    for i2 in V:
        if i1 != i2 and ti[i1] <= ti[i2]:
            model.addCons(
                (ti[i1] + di[i1] + T_min) <= (ti[i2] + (2 - quicksum(x[i1, k] for k in S) - quicksum(x[i2, k] for k in S)) * 99999)
            )

# The node in the service target and satellite pass must match
for i in V:
    for j in S:
        model.addCons(x[i, j] * (ni[i] - sj[j]) == 0)

# The operation mode must match
for i in V:
    for j in S:
        model.addCons(x[i, j] * oi[i] * (oi[i] - mj[j] - 1) == 0)

# For a given application id first do qkd and afterwards qkd post processing
for j1 in S:
    for j2 in S:
        if aj[j1] == aj[j2] and mj[j1] == 1 and mj[j2] == 0:
            model.addCons(quicksum(ti[i] * x[i, j1] for i in V) <= quicksum(ti[i] * x[i, j2] for i in V))

"""
# QKD post-processing and QKD must happen in the same schedule
for j1 in S:
    for j2 in S:
        if aj[j1] == aj[j2] and mj[j1] == 1 and mj[j2] == 0:  # Same application ID, QKD, and QKD post-processing
            model.addCons(
                quicksum(x[i, j1] for i in V) == quicksum(x[i, j2] for i in V)
            )
"""


# Maximum number of contacts per orbit
"""for f in set(fi.values()):
    model.addCons(
        quicksum(x[i, j] for i in V for j in S if fi[i] == f) <= 2
    )"""

# Maximum number of contacts in total
"""
model.addCons(quicksum(x[i, j] for j in S for i in V) <= C_max)
"""

# Optimize the model
try:
    model.optimize()

    contacts = []
    selected_passes = []
    for i in V:
        for j in S:
            if model.getVal(x[i, j]) > 0.5:
                contact = {}
                selected_passes.append(satellitePasses[i])
                contact["satellitePass"] = satellitePasses[i]
                contact["serviceTarget"] = serviceTargets[j]
                contacts.append(contact)

    print("###### Result ######")
    print("Performance of the solution is: " + str(round(calculateObjectiveFunction(contacts), 2)))
    print("Runtime was: " + str(model.getSolvingTime()))
    end = time.time()
    print("Overall time was: " + str(end-start))
    print("####################")

    plotOptimizationResult(serviceTargets, satellitePasses, contacts, "SCIP")
except Exception as ex:
    print(f"Exception: {ex}")

    