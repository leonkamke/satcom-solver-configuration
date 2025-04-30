from datetime import datetime
from pyscipopt import Model, quicksum
from ..utils import *
import time

start = time.time()

# Read problem instance
print("Read problem instance")
problemInstance = read_problem_instance("./src/input/data/train_world_dec_10_12h.json")
satellitePasses = problemInstance["satellite_passes"]
serviceTargets = problemInstance["service_targets"]

print("Start setting up problem and model")
V = list(range(len(satellitePasses)))
S = list(range(len(serviceTargets)))

di, ti, bi, ni, fi, oi = {}, {}, {}, {}, {}, {}
reference_time = datetime.fromisoformat(problemInstance["coverage_start"])

for idx, sp in enumerate(satellitePasses):
    start_time = datetime.fromisoformat(sp["startTime"])
    end_time = datetime.fromisoformat(sp["endTime"])
    ti[idx] = (start_time - reference_time).total_seconds()
    di[idx] = (end_time - start_time).total_seconds()
    bi[idx] = sp["achievableKeyVolume"]
    oi[idx] = 1 if sp["achievableKeyVolume"] == 0.0 else 0
    ni[idx] = sp["nodeId"]
    fi[idx] = sp["orbitId"]

pj, sj, mj, aj = {}, {}, {}, {}
for idx, st in enumerate(serviceTargets):
    pj[idx] = st["priority"]
    sj[idx] = st["nodeId"]
    mj[idx] = 1 if st["requestedOperation"] == "QKD" else 0
    aj[idx] = st["applicationId"]

T_min = 60  # Minimum time between consecutive contacts in seconds

model = Model("Satellite Optimization")

# Decision variables: only create if node and mode match
x = {}
for i in V:
    for j in S:
        if ni[i] == sj[j] and not (oi[i] == 1 and mj[j] == 1):
            x[i, j] = model.addVar(vtype="B", name=f"x_{i}_{j}")

# Objective
model.setObjective(
    quicksum(x[i, j] * pj[j] * (1 + bi[i] * mj[j]) for (i, j) in x),
    "maximize"
)

# Constraints: each pass at most once
for i in V:
    model.addCons(quicksum(x[i, j] for j in S if (i, j) in x) <= 1)

# Constraints: each target at most once
for j in S:
    model.addCons(quicksum(x[i, j] for i in V if (i, j) in x) <= 1)

# Non-overlapping satellite passes (optimized)
sorted_V = sorted(V, key=lambda i: ti[i])
for idx1, i1 in enumerate(sorted_V):
    for idx2 in range(idx1 + 1, len(sorted_V)):
        i2 = sorted_V[idx2]
        if ti[i2] - (ti[i1] + di[i1]) >= T_min:
            break
        expr1 = quicksum(x[i1, k] for k in S if (i1, k) in x)
        expr2 = quicksum(x[i2, k] for k in S if (i2, k) in x)
        model.addCons(
            (ti[i1] + di[i1] + T_min) <= (ti[i2] + (2 - expr1 - expr2) * 99999)
        )

# Application sequencing constraints: QKD before Post-Processing
for app_id in set(aj.values()):
    qkd_targets = [j for j in S if aj[j] == app_id and mj[j] == 1]
    pp_targets = [j for j in S if aj[j] == app_id and mj[j] == 0]
    for j1 in qkd_targets:
        for j2 in pp_targets:
            model.addCons(
                quicksum(ti[i] * x[i, j1] for i in V if (i, j1) in x) <=
                quicksum(ti[i] * x[i, j2] for i in V if (i, j2) in x)
            )

# Optimize
try:
    model.optimize()

    contacts = []
    for i in V:
        for j in S:
            if (i, j) in x and model.getVal(x[i, j]) > 0.5:
                contacts.append({
                    "satellitePass": satellitePasses[i],
                    "serviceTarget": serviceTargets[j]
                })

    print("###### Result ######")
    print("Performance of the solution is:", round(calculateObjectiveFunction(contacts), 2))
    print("Runtime was:", model.getSolvingTime())
    print("Overall time was:", time.time() - start)
    print("####################")

    plotOptimizationResult(serviceTargets, satellitePasses, contacts, "SCIP")
except Exception as ex:
    print(f"Exception: {ex}")

# Save SCIP parameters
params = model.getParams()
with open("scip_parameters.txt", "w") as f:
    for name in params:
        f.write(f"{name.replace('/', '_')}: {params[name]}\n")
