import os
import subprocess
from ..utils import *

path_problem_instance = "./src/input/data/problem_instance_europe_1day.json"

# Run Timefold solver in Java

mvn_build_command = [
    "mvn",
    "clean",
    "package"
]
subprocess.run(mvn_build_command, cwd="/home/leon/code/satellite-operations-planning/src/solvers/timefold_solver")

java_command = [
    "java",
    "-Xmx4g",
    "-jar",
    "/home/leon/code/satellite-operations-planning/src/solvers/timefold_solver/target/timefold_solver-1.0-SNAPSHOT-jar-with-dependencies.jar",
    path_problem_instance
]
subprocess.run(java_command)

# Calculate performance and plot solution
problemInstance = read_problem_instance(path_problem_instance)
satellitePasses = problemInstance["satellite_passes"]
serviceTargets = problemInstance["service_targets"]
contacts_file_path = "/home/leon/code/satellite-operations-planning/src/output/optimization/timefold/timefold_solution.json"
contacts = read_contacts_from_timefold(contacts_file_path)
os.remove("/home/leon/code/satellite-operations-planning/src/output/optimization/timefold/timefold_solution.json")

print("Performance of the solution is: " + str(round(calculateObjectiveFunction(contacts), 2)))
plotOptimizationResult(serviceTargets, satellitePasses, contacts, "Timefold")
