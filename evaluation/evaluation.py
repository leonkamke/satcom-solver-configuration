import os
import time
import subprocess
from datetime import datetime

runtime_eval_gurobi = [
    "sparkle initialise --no-save",
    "sparkle add_instances ../SatQKDOptim/Instances/TestInstances",
    "sparkle add_instances ../SatQKDOptim/Instances/TrainInstances",
    "sparkle add_solver ../SatQKDOptim/Solvers/Gurobi",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/TrainInstances --instance-set-test Instances/TestInstances"
]

runtime_eval_scip = [
    "sparkle initialise --no-save",
    "sparkle add_instances ../SatQKDOptim/Instances/TestInstances",
    "sparkle add_instances ../SatQKDOptim/Instances/TrainInstances",
    "sparkle add_solver ../SatQKDOptim/Solvers/SCIP",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/TrainInstances --instance-set-test Instances/TestInstances"
]

runtime_eval_timefold = [
    "sparkle initialise --no-save",
    "sparkle add_instances ../SatQKDOptim/Instances/TestInstances",
    "sparkle add_instances ../SatQKDOptim/Instances/TrainInstances",
    "sparkle add_solver ../SatQKDOptim/Solvers/Timefold",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/TrainInstances --instance-set-test Instances/TestInstances"
]

# List of evaluations
evaluations = [
    {"name": "eval_runtime_gurobi", "commands": runtime_eval_gurobi},
    # {"name": "eval_runtime_scip", "commands": runtime_eval_scip},
]

BASE_DIR = os.getcwd()

def wait_until_no_jobs():
    print("\nWaiting for all jobs to finish...")
    while True:
        result = subprocess.run(["squeue", "--me"], capture_output=True, text=True)
        print(result)
        lines = result.stdout.strip().split("\n")
        print(lines)

        # If only header is present, there are no jobs
        if len(lines) <= 2:
            print("All jobs completed.\n")
            return
        else:
            print(f"{len(lines)-1} job(s) still running...")
            time.sleep(60)  # Wait a minute before checking again


def run_experiment(eval):
    folder_name = f"{eval['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(folder_name, exist_ok=True)
    os.chdir(folder_name)

    print(f"Running {eval['name']} in {os.getcwd()}")

    for cmd in eval["commands"]:
        print(f"Executing: {cmd}")
        subprocess.run(cmd, shell=True)

    os.chdir(BASE_DIR)


# Run the evaluations
for evaluation in evaluations:
    run_experiment(evaluation)
    wait_until_no_jobs()
