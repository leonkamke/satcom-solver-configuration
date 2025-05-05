import os
import time
from datetime import datetime
from pyscipopt import Model, quicksum
from ..utils import *

start = time.time()

# MPS file path
mps_file_path = "/home/vx475510/satcom-solver-configuration/src/input/data/Dataset_year_europe_12h_80app/test_europe_12h_80app_apr_15.mps"

# Json file path
json_file_path = "/home/vx475510/satcom-solver-configuration/src/input/data/Dataset_year_europe_12h_80app/test_europe_12h_80app_apr_15.json"

# Time limit
max_runtime = 30

# Read problem instance
print("Read problem instance")
problemInstance = read_problem_instance(json_file_path)
satellitePasses = problemInstance["satellite_passes"]
serviceTargets = problemInstance["service_targets"]

V = list(range(len(satellitePasses)))
S = list(range(len(serviceTargets)))

T_min = 60  # Minimum time between consecutive contacts in seconds

# Try to load MPS model
model = Model("Satellite Optimization")
if os.path.exists(mps_file_path):
    print(f"Reading model from {mps_file_path}")
    model.readProblem(mps_file_path)
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
                x[i, j] = model.addVar(vtype="B", name=f"x_{i}_{j}")

    # Objective
    model.setObjective(
        quicksum(x[i, j] * pj[j] * (1 + bi[i] * mj[j]) for (i, j) in x), "maximize"
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
                    quicksum(ti[i] * x[i, j1] for i in V if (i, j1) in x)
                    <= quicksum(ti[i] * x[i, j2] for i in V if (i, j2) in x)
                )

    # Save MPS model for next time
    model.writeProblem(mps_file_path)
    print(f"Model saved to {mps_file_path}")

# Solve model
try:
    model.setParam("limits/time", max_runtime)
    model.setParam("misc/usesymmetry", 0)

    tmpparams = {
        "branching_checksol": True,
        "branching_forceallchildren": False,
        "branching_gomory_priority": 72071924,
        "branching_preferbinary": False,
        "branching_relpscost_confidencelevel": 2,
        "branching_scorefac": 0.14121197684769626,
        "branching_scorefunc": "q",
        "conflict_enable": False,
        "constraints_linear_aggregatevariables": False,
        "constraints_linear_proptiming": 2,
        "constraints_linear_sepafreq": 461961634,
        "cutselection_dynamic_efficacyweight": 879304.5976928559,
        "cutselection_hybrid_priority": 564442401,
        "heuristics_actconsdiving_freq": 978392638,
        "heuristics_alns_freq": 956691656,
        "heuristics_dins_freq": 450210403,
        "heuristics_feaspump_freq": 876504788,
        "heuristics_gins_freq": 294877508,
        "heuristics_localbranching_freq": 954988040,
        "heuristics_mutation_freq": 987620083,
        "heuristics_rens_freq": 368823167,
        "heuristics_rens_priority": 478883798,
        "heuristics_rins_freq": 576029859,
        "heuristics_rounding_freq": 649926310,
        "heuristics_scheduler_freq": 184568753,
        "heuristics_trustregion_freq": 149969819,
        "heuristics_undercover_freq": 131180632,
        "heuristics_undercover_priority": 363364839,
        "lp_fastmip": 1,
        "lp_initalgorithm": "b",
        "lp_presolving": True,
        "lp_pricing": "f",
        "lp_resolvealgorithm": "b",
        "lp_scaling": 2,
        "lp_solvefreq": 501306455,
        "lp_threads": 21,
        "misc_allowstrongdualreds": True,
        "misc_allowweakdualreds": False,
        "nodeselection_bfs_stdpriority": 1066130691,
        "nodeselection_dfs_stdpriority": 1037298603,
        "nodeselection_estimate_stdpriority": 107562887,
        "nodeselection_hybridestim_stdpriority": 765042499,
        "parallel_mode": 0,
        "presolving_maxrestarts": 1618597296,
        "presolving_maxrounds": 1789029270,
        "presolving_milp_enabledualinfer": False,
        "presolving_milp_enablemultiaggr": True,
        "presolving_milp_enablesparsify": True,
        "presolving_milp_internalmaxrounds": 1711922534,
        "presolving_milp_maxrounds": 1801288061,
        "presolving_restartfac": 0.3632183745532702,
        "presolving_restartminred": 0.7937056062006929,
        "separating_clique_freq": 576453343,
        "separating_cmir_freq": 414683884,
        "separating_cmir_priority": 215498175,
        "separating_flowcover_freq": 770778782,
        "separating_flowcover_priority": 70689790,
        "separating_gomory_freq": 301365980,
        "separating_maxcuts": 1828009121,
        "separating_maxcutsroot": 65785104,
        "separating_maxrounds": 1282328041,
        "separating_maxroundsroot": 1218547494,
        "separating_strongcg_freq": 965934401,
    }
    
    for key, value in tmpparams.items():
        model.setParam(key.replace("_", "/"), value)

    model.optimize()

    # Rebuild variable dictionary from model if x is not defined
    if "x" not in locals():
        x = {}
        for var in model.getVars():
            if var.name.startswith("x_"):
                _, i_str, j_str = var.name.split("_")
                i, j = int(i_str), int(j_str)
                x[i, j] = var

    contacts = []
    for i in V:
        for j in S:
            if (i, j) in x:
                val = model.getVal(x[i, j])
                if val > 0.5:
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
    print("Runtime was:", model.getSolvingTime())
    print("Overall time was:", time.time() - start)
    print("####################")

    # plotOptimizationResult(serviceTargets, satellitePasses, contacts, "SCIP")

except Exception as ex:
    print(f"Exception: {ex}")
