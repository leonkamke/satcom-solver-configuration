import os
import subprocess
from ..utils import *
import uuid

instance_path = "/home/vx475510/satcom-solver-configuration/src/input/data/Dataset_year_europe_24h_100app/test_europe_24h_100app_aug_15.json"

# Run Timefold solver in Java

# Read user home from file
user_home = None
with open("./src/solvers/cluster_home.txt", "r") as f:
    user_home = f.read().strip()

# Compile and build Java Timefold project (WORKS WITH SPARKLE!)
# TODO: Remove for big experiments (takes some time)
"""mvn_build_command = [
    os.path.join(user_home, "maven/apache-maven-3.9.9/bin/mvn"),
    "clean",
    "package"
]
subprocess.run(mvn_build_command, cwd="./Solvers/Timefold/timefold_solver")"""

# Run Timefold jar file
java_path = os.path.join(user_home, "java/openlogic-openjdk-17.0.14+7-linux-x64/bin/java")
random_uuid = str(uuid.uuid4())
java_command = [
    java_path,
    "-Xmx20g",
    "-jar",
    "./src/solvers/timefold_solver/target/timefold_solver-1.0-SNAPSHOT-jar-with-dependencies.jar",
    "-inst",
    instance_path,
    "-uuid",
    random_uuid,
    "-constructionHeuristicType", "NONE", "-ls1Type", "NONE", "-ls2Type", "NONE"
]
subprocess.run(java_command)

# Calculate performance and plot solution
problemInstance = read_problem_instance(instance_path)
satellitePasses = problemInstance["satellite_passes"]
serviceTargets = problemInstance["service_targets"]
contacts_file_path = "./Tmp/" + random_uuid + ".json"
contacts = read_contacts_from_timefold(contacts_file_path)
os.remove(contacts_file_path)
print("Number of contacts in solution: " + str(len(contacts)))
print("Solution is valid: " + str(verify_contacts_solution(contacts)))


print(
    "Performance of the solution is: "
    + str(round(calculateObjectiveFunction(contacts), 2))
)
plotOptimizationResult(serviceTargets, satellitePasses, contacts, "Timefold")
