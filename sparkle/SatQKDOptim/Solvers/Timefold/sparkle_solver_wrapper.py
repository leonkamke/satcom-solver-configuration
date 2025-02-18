#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import sys
from pathlib import Path
from sparkle.types import SolverStatus
from sparkle.tools.solver_wrapper_parsing import parse_solver_wrapper_args
from .utils import *
import subprocess

# Convert the arguments to a dictionary
args = parse_solver_wrapper_args(sys.argv[1:])

# Extract and delete data that needs specific formatting
solver_dir = Path(args["solver_dir"])
instance_path = Path(args["instance"])
seed = args["seed"]

del args["solver_dir"]
del args["instance"]
del args["cutoff_time"]
del args["seed"]

# Prepare the command to execute the solver
solver_name = "Timefold"
if solver_dir != Path("."):
    solver_exec = f"{solver_dir / solver_name}"
else:
    f"./{solver_name}"
solver_cmd = [solver_exec,
              "-inst", str(instance_path),
              "-seed", str(seed)]

run_solver_command = [
    "java",
    "-Xmx4g",
    "-jar",
    "./timefold_solver/target/timefold_solver-1.0-SNAPSHOT-jar-with-dependencies.jar",  # Path to be checked
    instance_path
]

# Read Timefold parameter from call
params = []
for key in args:
    if args[key] is not None:
        params.extend(["-" + str(key), str(args[key])])


# Set the parameters in timefold configuration file (xml)
# TODO: Use some xml python package to write into xml file


# Run Timefold solver
schedule_quality = None
runtime = max_runtime # Timefold always runs as long as specified in xml
try:
    subprocess.run(run_solver_command)
                
    # Compute quality of solution
    # Calculate performance and plot solution
    problemInstance = read_problem_instance(instance_path)
    satellitePasses = problemInstance["satellite_passes"]
    serviceTargets = problemInstance["service_targets"]
    contacts_file_path = "./tmp/timefold_solution_tmp.json"
    contacts = read_contacts_from_timefold(contacts_file_path)
    os.remove("./tmp/timefold_solution_tmp.json")
    schedule_quality = round(calculateObjectiveFunction(contacts), 2)
    # TODO: Get timefold runtime. Solve in timefold_solution_tmp?

except Exception as ex:
    print(f"Solver call failed with exception:\n{ex}")

# Optional: Print original output so the solution can be verified by SATVerifier
print("Performance of the solution is: " + str(schedule_quality))

status = SolverStatus.CRASHED
if schedule_quality and runtime:
    status = SolverStatus.SUCCESS
    

outdir = {"status": status.value,               
          "schedule_quality": schedule_quality,
          "runtime": runtime,                   
          "solver_call": solver_cmd + params}

print(outdir)