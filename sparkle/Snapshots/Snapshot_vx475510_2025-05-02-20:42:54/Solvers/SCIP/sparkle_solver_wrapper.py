#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import subprocess
from pathlib import Path
import uuid
from sparkle.tools.solver_wrapper_parsing import parse_solver_wrapper_args


def trim_to_solver_output(text):
    marker = "SCIP solver output is:"
    parts = text.split(marker, 1)
    if len(parts) > 1:
        return parts[1].lstrip()
    return ""


try:
    # Convert the arguments to a dictionary
    args = parse_solver_wrapper_args(sys.argv[1:])

    # Extract and delete data that needs specific formatting
    solver_dir = Path(args["solver_dir"])
    instance = Path(args["instance"])
    seed = args["seed"]

    del args["solver_dir"]
    del args["instance"]
    del args["cutoff_time"]
    del args["seed"]
    del args["objectives"]

    solver_name = "scip_solver.py"
    if solver_dir != Path("."):
        solver_exec = f"{solver_dir / solver_name}"
    else:
        solver_exec = f"./{solver_name}"
    solver_cmd = ["python", solver_exec, "-inst", str(instance), "-seed", str(seed)]

    # Construct call from args dictionary
    params = []
    for key in args:
        if args[key] is not None:
            params.extend(["-" + str(key), str(args[key])])

    solver_call = subprocess.run(solver_cmd + params, capture_output=True)
    output_str = trim_to_solver_output(solver_call.stdout.decode())
    print(output_str)

except Exception as ex:
    print(f"Solver call failed with exception:\n{ex}")
    exception_file_name = "./Tmp/" + str(uuid.uuid4()) + ".txt"
    with open(exception_file_name, "w") as file:
        file.write("Solver wrapper failed with exception:\n")
        file.write(str(ex))
