import sys
from pathlib import Path
from datetime import datetime
from gurobipy import Model, GRB, quicksum, read
import json
import uuid
import traceback


def parse_args_to_dict(argv):
    args_dict = {}
    i = 1  # skip python gurobi_solver.py
    while i < len(argv):
        if argv[i].startswith("-"):
            key = argv[i].lstrip("-")
            # Make sure there's a value after the key
            if i + 1 < len(argv) and not argv[i + 1].startswith("-"):
                args_dict[key] = argv[i + 1]
                i += 2
            else:  # Else skip
                i += 1
        else:  # Else skip
            i += 1
    return args_dict


# Helper function
def read_problem_instance(instance_path):
    with open(instance_path, "r") as file:
        data = json.load(file)
        return data[0]


# Helper function
def calculateObjectiveFunction(contacts):
    result = 0
    for contact in contacts:
        satellitePass = contact["satellitePass"]
        serviceTarget = contact["serviceTarget"]

        priority = serviceTarget["priority"]
        achievableKeyVolume = satellitePass["achievableKeyVolume"]
        operationMode = 1 if serviceTarget["requestedOperation"] == "QKD" else 0
        result += priority * (1 + achievableKeyVolume * operationMode)
    return result


try:
    # Set max_solve_time
    max_solve_time = None
    with open("./Solvers/Gurobi/max_solve_time.txt", "r") as file:
        max_solve_time = int(file.read().strip())

    # Read the arguments
    args = parse_args_to_dict(sys.argv)

    instance_path_json = args["inst"]
    full_path_json = Path(instance_path_json)
    name_parts = full_path_json.name.split("_")
    instance_path_mps = (
        "../../../src/input/data2/Dataset_year_"
        + str(name_parts[1])
        + "_"
        + str(name_parts[2])
        + "_"
        + str(name_parts[3])
        + "/"
        + full_path_json.with_suffix(".mps").name
    )

    seed = int(args["seed"]) % 1999999999
    del args["inst"]
    del args["seed"]

    config = args

    # Read problem instance
    print("Read problem instance")
    problemInstance = read_problem_instance(instance_path_json)
    satellitePasses = problemInstance["satellite_passes"]
    serviceTargets = problemInstance["service_targets"]

    V = list(range(len(satellitePasses)))
    S = list(range(len(serviceTargets)))

    model = read(instance_path_mps)

    # Suppress all solver output
    model.setParam("OutputFlag", 0)

    # Set Gurobi seed
    # model.setParam("Seed", seed)

    # Set parameters for model
    for k, v in config.items():
        config[k] = float(v)
        model.setParam(k, config[k])

    # Run the Gurobi solver
    model.setParam("TimeLimit", max_solve_time)
    quality = 0
    solve_time = max_solve_time
    par10 = 10 * max_solve_time

    # Optimize the model
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

    # Compute objectives
    if len(contacts) > 0:
        quality = int(calculateObjectiveFunction(contacts))
    if model.Runtime != None:
        solve_time = round(model.Runtime, 4)
    if solve_time < max_solve_time:
        par10 = solve_time

    # Print result
    result = {
        "status": "SUCCESS",
        "par10": par10,
        "quality": 1 if quality <= 0 else quality,
        "solve_time": solve_time,
        "solver_call": None,
    }
    print("Gurobi solver output is:")
    print(result)

except Exception as ex:
    max_solve_time = None
    with open("./Solvers/Gurobi/max_solve_time.txt", "r") as file:
        max_solve_time = int(file.read().strip())

    result = {
        "status": "SUCCESS",
        "par10": max_solve_time * 10,
        "quality": 1,
        "solve_time": max_solve_time,
        "solver_call": None,
    }
    print("Gurobi solver output is:")
    print(result)
    exception_file_name = "./Tmp/" + str(uuid.uuid4()) + ".txt"
    with open(exception_file_name, "w") as file:
        file.write("Optimization method failed with exception:\n")
        file.write(str(ex) + "\n")
        file.write(traceback.format_exc() + "\n")
        file.write("This was the configuration:\n")
        file.write(str(config))
