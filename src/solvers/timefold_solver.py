import subprocess

def call_timefold_solver():
    java_command = [
        "java",
        "-cp",
        "/home/leon/code/satellite-operations-planning/src/solvers/timefold_solver/target/timefold_solver-1.0-SNAPSHOT.jar",
        "com.optimization.solver.TimefoldSolver"
    ]
    print("aaaaa")
    subprocess.run(java_command)
    print("bbbbb")

call_timefold_solver()