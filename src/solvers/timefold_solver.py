import os
import subprocess
from ..utils import *

path_problem_instance = "./src/input/data/problem_instance_europe_jan_3h.json"

# Run Timefold solver in Java

"""
M2_HOME="$HOME/maven/apache-maven-3.9.9"
export M2_HOME=$HOME/maven/apache-maven-3.9.9
export PATH=$M2_HOME/bin:$PATH

export JAVA_HOME=$HOME/java/openlogic-openjdk-17.0.14+7-linux-x64
export PATH=$JAVA_HOME/bin:$PATH
"""

mvn_build_command = [
    "mvn",
    "clean",
    "package"
]
subprocess.run(mvn_build_command, cwd="./src/solvers/timefold_solver")

java_command = [
    "java",
    "-Xmx4g",
    "-jar",
    "./src/solvers/timefold_solver/target/timefold_solver-1.0-SNAPSHOT-jar-with-dependencies.jar",
    path_problem_instance
]
subprocess.run(java_command)

# Calculate performance and plot solution
problemInstance = read_problem_instance(path_problem_instance)
satellitePasses = problemInstance["satellite_passes"]
serviceTargets = problemInstance["service_targets"]
contacts_file_path = "./Tmp/timefold_solution_tmp.json"
contacts = read_contacts_from_timefold(contacts_file_path)
os.remove("./Tmp/timefold_solution_tmp.json")

print("Performance of the solution is: " + str(round(calculateObjectiveFunction(contacts), 2)))
plotOptimizationResult(serviceTargets, satellitePasses, contacts, "Timefold")
