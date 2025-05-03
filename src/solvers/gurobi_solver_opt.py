import os
import time
from datetime import datetime
from gurobipy import *
from ..utils import *

start = time.time()

# MPS file path
mps_file_path = "/home/vx475510/satcom-solver-configuration/src/input/data/Dataset_year_europe_12h_80app/train_europe_12h_80app_nov_5.mps"

# Json file path
json_file_path = "/home/vx475510/satcom-solver-configuration/src/input/data/Dataset_year_europe_12h_80app/train_europe_12h_80app_nov_5.json"

# Read problem instance
print("Read problem instance")
problemInstance = read_problem_instance(json_file_path)
satellitePasses = problemInstance["satellite_passes"]
serviceTargets = problemInstance["service_targets"]

V = list(range(len(satellitePasses)))
S = list(range(len(serviceTargets)))

T_min = 60  # Minimum time between consecutive contacts in seconds

# Try to load model from MPS if available
if os.path.exists(mps_file_path):
    print(f"Reading model from {mps_file_path}")
    model = read(mps_file_path)
else:
    print("Building model from scratch...")

    print("Start setting up problem and model")
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

    model = Model("Satellite Optimization")

    # Decision variables: only create if node and mode match
    x = {}
    for i in V:
        for j in S:
            if ni[i] == sj[j] and not (oi[i] == 1 and mj[j] == 1):
                x[i, j] = model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")

    model.update()

    # Objective
    model.setObjective(
        quicksum(x[i, j] * pj[j] * (1 + bi[i] * mj[j]) for (i, j) in x), GRB.MAXIMIZE
    )

    # Constraints: each pass at most once
    for i in V:
        model.addConstr(quicksum(x[i, j] for j in S if (i, j) in x) <= 1)

    # Constraints: each target at most once
    for j in S:
        model.addConstr(quicksum(x[i, j] for i in V if (i, j) in x) <= 1)

    # Non-overlapping satellite passes (optimized)
    sorted_V = sorted(V, key=lambda i: ti[i])
    for idx1, i1 in enumerate(sorted_V):
        for idx2 in range(idx1 + 1, len(sorted_V)):
            i2 = sorted_V[idx2]
            if ti[i2] - (ti[i1] + di[i1]) >= T_min:
                break
            expr1 = quicksum(x[i1, k] for k in S if (i1, k) in x)
            expr2 = quicksum(x[i2, k] for k in S if (i2, k) in x)
            # Use big-M constraint
            M = 99999
            model.addConstr(
                (ti[i1] + di[i1] + T_min) <= (ti[i2] + (2 - expr1 - expr2) * M)
            )

    # Application sequencing constraints: QKD before Post-Processing
    for app_id in set(aj.values()):
        qkd_targets = [j for j in S if aj[j] == app_id and mj[j] == 1]
        pp_targets = [j for j in S if aj[j] == app_id and mj[j] == 0]
        for j1 in qkd_targets:
            for j2 in pp_targets:
                lhs = quicksum(ti[i] * x[i, j1] for i in V if (i, j1) in x)
                rhs = quicksum(ti[i] * x[i, j2] for i in V if (i, j2) in x)
                model.addConstr(lhs <= rhs)

    # Save the model to MPS file
    model.write(mps_file_path)
    print(f"Model saved to {mps_file_path}")

# Optimize the model
try:
    model.setParam("TimeLimit", 60)
    model.optimize()

    contacts = []
    for i in V:
        for j in S:
            var = model.getVarByName(f"x_{i}_{j}")
            if var is not None and var.X > 0.5:
                contacts.append(
                    {
                        "satellitePass": satellitePasses[i],
                        "serviceTarget": serviceTargets[j],
                    }
                )

    solution_valid = verify_contacts_solution(contacts, T_min)
    if not solution_valid:
        raise Exception("Invalid Solution!")

    print("###### Result ######")
    print(
        "Performance of the solution is:",
        round(calculateObjectiveFunction(contacts), 2),
    )
    print("Runtime was:", model.Runtime)
    print("Overall time was:", time.time() - start)
    print("####################")

    plotOptimizationResult(serviceTargets, satellitePasses, contacts, "Gurobi")

except Exception as ex:
    print(f"Exception: {ex}")
