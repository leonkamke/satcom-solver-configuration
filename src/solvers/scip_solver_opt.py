import os
import time
from datetime import datetime
from pyscipopt import Model, quicksum
from ..utils import *

start = time.time()

# MPS file path
mps_file_path = "/home/vx475510/satcom-solver-configuration/src/input/hardData/Dataset_year_europe_48h_100app/test_europe_48h_100app_dec_15.mps"

# Json file path
json_file_path = "/home/vx475510/satcom-solver-configuration/src/input/hardData/Dataset_year_europe_48h_100app/test_europe_48h_100app_dec_15.json"

# Time limit
max_runtime = 600

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
    """for app_id in set(aj.values()):
        qkd_targets = [j for j in S if aj[j] == app_id and mj[j] == 1]
        pp_targets = [j for j in S if aj[j] == app_id and mj[j] == 0]
        for j1 in qkd_targets:
            for j2 in pp_targets:
                model.addCons(
                    quicksum(ti[i] * x[i, j1] for i in V if (i, j1) in x)
                    <= quicksum(ti[i] * x[i, j2] for i in V if (i, j2) in x)
                )"""

    # Save MPS model for next time
    # model.writeProblem(mps_file_path)
    print(f"Model saved to {mps_file_path}")

# Solve model
try:
    testvar = int("21474836475669999")
    model.setParam("limits/time", max_runtime)
    # model.setParam("misc/usesymmetry", 0)
    # model.setParam("lp/threads", 64)
    # model.setParam("randomization/randomseedshift", int("2147483647"))


    tmpparams = {
        "branching_checksol": True,
        "branching_forceallchildren": False,
        "branching_gomory_priority": 499927866,
        "branching_preferbinary": False,
        "branching_relpscost_confidencelevel": 2,
        "branching_scorefunc": "s",
        "conflict_enable": False,
        "constraints_linear_aggregatevariables": False,
        "constraints_linear_proptiming": 15,
        "constraints_linear_sepafreq": 681394052,
        "cutselection_dynamic_efficacyweight": 122241.52570260246,
        "cutselection_hybrid_priority": 745329472,
        "heuristics_actconsdiving_freq": 63949455,
        "heuristics_alns_freq": 816160605,
        "heuristics_dins_freq": 197493421,
        "heuristics_dins_priority": 38894488,
        "heuristics_feaspump_freq": 20221553,
        "heuristics_gins_freq": 802811023,
        "heuristics_localbranching_freq": 916894188,
        "heuristics_mutation_freq": 886314512,
        "heuristics_rens_freq": 240378796,
        "heuristics_rens_priority": 234784832,
        "heuristics_rins_freq": 224726510,
        "heuristics_rins_priority": 288486519,
        "heuristics_rounding_freq": 902836979,
        "heuristics_scheduler_freq": 827689196,
        "heuristics_trustregion_freq": 988778766,
        "heuristics_undercover_freq": 72153277,
        "lp_fastmip": 0,
        "lp_initalgorithm": "d",
        "lp_presolving": False,
        "lp_pricing": "f",
        "lp_resolvealgorithm": "b",
        "lp_scaling": 0,
        "lp_solvefreq": 417470629,
        "lp_threads": 18,
        "misc_allowstrongdualreds": True,
        "misc_allowweakdualreds": False,
        "nodeselection_dfs_stdpriority": 437339483,
        "nodeselection_estimate_stdpriority": 637192790,
        "nodeselection_hybridestim_stdpriority": 739537760,
        "nodeselection_uct_stdpriority": 864508281,
        "parallel_mode": 0,
        "presolving_maxrestarts": 672921010,
        "presolving_maxrounds": 257649809,
        "presolving_milp_enabledualinfer": False,
        "presolving_milp_enablemultiaggr": True,
        "presolving_milp_enablesparsify": False,
        "presolving_milp_internalmaxrounds": 656301124,
        "presolving_milp_maxrounds": 30840976,
        "presolving_restartfac": 0.25862884472312997,
        "presolving_restartminred": 0.07097988771641295,
        "separating_clique_freq": 197426096,
        "separating_clique_priority": 422593773,
        "separating_cmir_freq": 954064182,
        "separating_flowcover_freq": 449104720,
        "separating_gomory_freq": 495738927,
        "separating_maxcuts": 1877929427,
        "separating_maxcutsroot": 1152346066,
        "separating_maxrounds": 1873452250,
        "separating_maxroundsroot": 194917172,
        "separating_strongcg_freq": 955433686,
    }

    #for key, value in tmpparams.items():
     #   model.setParam(key.replace("_", "/"), value)

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

    plotOptimizationResult(serviceTargets, satellitePasses, contacts, "SCIP")

except Exception as ex:
    print(f"Exception: {ex}")
