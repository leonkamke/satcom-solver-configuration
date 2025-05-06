import os
import time
import subprocess
from datetime import datetime

# Runtime evaluations for ground terminals located in Europe ########################

# Quality evaluations for 15 seconds limit -------------------------------------------

europe_quality_eval_gurobi_15s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Gurobi",
    "sed -i '1s/.*/15/' ./Solvers/Gurobi/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 60/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/Dataset_Europe_All_Train --instance-set-test Instances/Dataset_Europe_All_Test --objectives quality:max",
]

europe_quality_eval_scip_15s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/SCIP",
    "sed -i '1s/.*/15/' ./Solvers/SCIP/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 60/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/Dataset_Europe_All_Train --instance-set-test Instances/Dataset_Europe_All_Test --objectives quality:max",
]

europe_quality_eval_timefold_15s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Timefold",
    "sed -i '1s/.*/15/' ./Solvers/Timefold/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 60/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/Dataset_Europe_All_Train --instance-set-test Instances/Dataset_Europe_All_Test --objectives quality:max",
]

# Quality evaluations for 30 seconds limit -------------------------------------------

europe_quality_eval_gurobi_30s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Gurobi",
    "sed -i '1s/.*/30/' ./Solvers/Gurobi/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 70/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/Dataset_Europe_All_Train --instance-set-test Instances/Dataset_Europe_All_Test --objectives quality:max",
]

europe_quality_eval_scip_30s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/SCIP",
    "sed -i '1s/.*/30/' ./Solvers/SCIP/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 70/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/Dataset_Europe_All_Train --instance-set-test Instances/Dataset_Europe_All_Test --objectives quality:max",
]

europe_quality_eval_timefold_30s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Timefold",
    "sed -i '1s/.*/30/' ./Solvers/Timefold/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 70/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/Dataset_Europe_All_Train --instance-set-test Instances/Dataset_Europe_All_Test --objectives quality:max",
]

# Quality evaluations for 45 seconds limit -------------------------------------------

europe_quality_eval_gurobi_45s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Gurobi",
    "sed -i '1s/.*/45/' ./Solvers/Gurobi/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 90/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/Dataset_Europe_All_Train --instance-set-test Instances/Dataset_Europe_All_Test --objectives quality:max",
]

europe_quality_eval_scip_45s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/SCIP",
    "sed -i '1s/.*/45/' ./Solvers/SCIP/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 90/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/Dataset_Europe_All_Train --instance-set-test Instances/Dataset_Europe_All_Test --objectives quality:max",
]

europe_quality_eval_timefold_45s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Timefold",
    "sed -i '1s/.*/45/' ./Solvers/Timefold/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 90/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/Dataset_Europe_All_Train --instance-set-test Instances/Dataset_Europe_All_Test --objectives quality:max",
]

# Quality evaluations for 60 seconds limit -------------------------------------------

europe_quality_eval_gurobi_60s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Gurobi",
    "sed -i '1s/.*/60/' ./Solvers/Gurobi/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 90/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/Dataset_Europe_All_Train --instance-set-test Instances/Dataset_Europe_All_Test --objectives quality:max",
]

europe_quality_eval_scip_60s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/SCIP",
    "sed -i '1s/.*/60/' ./Solvers/SCIP/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 90/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/Dataset_Europe_All_Train --instance-set-test Instances/Dataset_Europe_All_Test --objectives quality:max",
]

europe_quality_eval_timefold_60s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Timefold",
    "sed -i '1s/.*/60/' ./Solvers/Timefold/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 90/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/Dataset_Europe_All_Train --instance-set-test Instances/Dataset_Europe_All_Test --objectives quality:max",
]

# Quality evaluations for 300 seconds limit -------------------------------------------

europe_quality_eval_gurobi_300s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Gurobi",
    "sed -i '1s/.*/300/' ./Solvers/Gurobi/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 360/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 3600/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 180:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/Dataset_Europe_All_Train --instance-set-test Instances/Dataset_Europe_All_Test --objectives quality:max",
]

europe_quality_eval_scip_300s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/SCIP",
    "sed -i '1s/.*/300/' ./Solvers/SCIP/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 360/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 3600/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 180:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/Dataset_Europe_All_Train --instance-set-test Instances/Dataset_Europe_All_Test --objectives quality:max",
]

europe_quality_eval_timefold_300s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Timefold",
    "sed -i '1s/.*/300/' ./Solvers/Timefold/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 360/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 3600/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 180:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/Dataset_Europe_All_Train --instance-set-test Instances/Dataset_Europe_All_Test --objectives quality:max",
]

# Runtime evaluations for ground terminals located on all continents ########################

world_quality_eval_gurobi_15s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Gurobi",
    "sed -i '1s/.*/15/' ./Solvers/Gurobi/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 60/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/Dataset_World_All_Train --instance-set-test Instances/Dataset_World_All_Test --objectives quality:max",
]

world_quality_eval_scip_15s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/SCIP",
    "sed -i '1s/.*/15/' ./Solvers/SCIP/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 60/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/Dataset_World_All_Train --instance-set-test Instances/Dataset_World_All_Test --objectives quality:max",
]

world_quality_eval_timefold_15s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Timefold",
    "sed -i '1s/.*/15/' ./Solvers/Timefold/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 60/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/Dataset_World_All_Train --instance-set-test Instances/Dataset_World_All_Test --objectives quality:max",
]

# Quality evaluations for 30 seconds limit -------------------------------------------

world_quality_eval_gurobi_30s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Gurobi",
    "sed -i '1s/.*/30/' ./Solvers/Gurobi/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 70/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/Dataset_World_All_Train --instance-set-test Instances/Dataset_World_All_Test --objectives quality:max",
]

world_quality_eval_scip_30s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/SCIP",
    "sed -i '1s/.*/30/' ./Solvers/SCIP/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 70/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/Dataset_World_All_Train --instance-set-test Instances/Dataset_World_All_Test --objectives quality:max",
]

world_quality_eval_timefold_30s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Timefold",
    "sed -i '1s/.*/30/' ./Solvers/Timefold/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 70/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/Dataset_World_All_Train --instance-set-test Instances/Dataset_World_All_Test --objectives quality:max",
]

# Quality evaluations for 45 seconds limit -------------------------------------------

world_quality_eval_gurobi_45s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Gurobi",
    "sed -i '1s/.*/45/' ./Solvers/Gurobi/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 90/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/Dataset_World_All_Train --instance-set-test Instances/Dataset_World_All_Test --objectives quality:max",
]

world_quality_eval_scip_45s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/SCIP",
    "sed -i '1s/.*/45/' ./Solvers/SCIP/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 90/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/Dataset_World_All_Train --instance-set-test Instances/Dataset_World_All_Test --objectives quality:max",
]

world_quality_eval_timefold_45s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Timefold",
    "sed -i '1s/.*/45/' ./Solvers/Timefold/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 90/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/Dataset_World_All_Train --instance-set-test Instances/Dataset_World_All_Test --objectives quality:max",
]

# Quality evaluations for 60 seconds limit -------------------------------------------

world_quality_eval_gurobi_60s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Gurobi",
    "sed -i '1s/.*/60/' ./Solvers/Gurobi/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 90/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/Dataset_World_All_Train --instance-set-test Instances/Dataset_World_All_Test --objectives quality:max",
]

world_quality_eval_scip_60s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/SCIP",
    "sed -i '1s/.*/60/' ./Solvers/SCIP/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 90/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/Dataset_World_All_Train --instance-set-test Instances/Dataset_World_All_Test --objectives quality:max",
]

world_quality_eval_timefold_60s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Timefold",
    "sed -i '1s/.*/60/' ./Solvers/Timefold/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 90/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 2700/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 90:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/Dataset_World_All_Train --instance-set-test Instances/Dataset_World_All_Test --objectives quality:max",
]

# Quality evaluations for 300 seconds limit -------------------------------------------

world_quality_eval_gurobi_300s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Gurobi",
    "sed -i '1s/.*/300/' ./Solvers/Gurobi/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 360/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 3600/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 180:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/Dataset_World_All_Train --instance-set-test Instances/Dataset_World_All_Test --objectives quality:max",
]

world_quality_eval_scip_300s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/SCIP",
    "sed -i '1s/.*/300/' ./Solvers/SCIP/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 360/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 3600/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 180:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/Dataset_World_All_Train --instance-set-test Instances/Dataset_World_All_Test --objectives quality:max",
]

world_quality_eval_timefold_300s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_World_All_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Timefold",
    "sed -i '1s/.*/300/' ./Solvers/Timefold/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '4s/.*/target_cutoff_time = 360/' ./Settings/sparkle_settings.ini",
    "sed -i '12s/.*/wallclock_time = 3600/' ./Settings/sparkle_settings.ini",
    "sed -i '30s/.*/time = 180:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/Dataset_World_All_Train --instance-set-test Instances/Dataset_World_All_Test --objectives quality:max",
]


# List of evaluations
evaluations = [
    # Evaluations for europe ground terminals
    {
        "name": "europe_quality_eval_gurobi_15s",
        "commands": europe_quality_eval_gurobi_15s,
    },
    {"name": "europe_quality_eval_scip_15s", "commands": europe_quality_eval_scip_15s},
    {
        "name": "europe_quality_eval_timefold_15s",
        "commands": europe_quality_eval_timefold_15s,
    },
    {
        "name": "europe_quality_eval_gurobi_30s",
        "commands": europe_quality_eval_gurobi_30s,
    },
    {"name": "europe_quality_eval_scip_30s", "commands": europe_quality_eval_scip_30s},
    {
        "name": "europe_quality_eval_timefold_30s",
        "commands": europe_quality_eval_timefold_30s,
    },
    {
        "name": "europe_quality_eval_gurobi_45s",
        "commands": europe_quality_eval_gurobi_45s,
    },
    {"name": "europe_quality_eval_scip_45s", "commands": europe_quality_eval_scip_45s},
    {
        "name": "europe_quality_eval_timefold_45s",
        "commands": europe_quality_eval_timefold_45s,
    },
    {
        "name": "europe_quality_eval_gurobi_60s",
        "commands": europe_quality_eval_gurobi_60s,
    },
    {"name": "europe_quality_eval_scip_60s", "commands": europe_quality_eval_scip_60s},
    {
        "name": "europe_quality_eval_timefold_60s",
        "commands": europe_quality_eval_timefold_60s,
    },
    {
        "name": "europe_quality_eval_gurobi_300s",
        "commands": europe_quality_eval_gurobi_300s,
    },
    {
        "name": "europe_quality_eval_scip_300s",
        "commands": europe_quality_eval_scip_300s,
    },
    {
        "name": "europe_quality_eval_timefold_300s",
        "commands": europe_quality_eval_timefold_300s,
    },
    # Evaluations for world round terminals
    {
        "name": "world_quality_eval_gurobi_15s",
        "commands": world_quality_eval_gurobi_15s,
    },
    {"name": "world_quality_eval_scip_15s", "commands": world_quality_eval_scip_15s},
    {
        "name": "world_quality_eval_timefold_15s",
        "commands": world_quality_eval_timefold_15s,
    },
    {
        "name": "world_quality_eval_gurobi_30s",
        "commands": world_quality_eval_gurobi_30s,
    },
    {"name": "world_quality_eval_scip_30s", "commands": world_quality_eval_scip_30s},
    {
        "name": "world_quality_eval_timefold_30s",
        "commands": world_quality_eval_timefold_30s,
    },
    {
        "name": "world_quality_eval_gurobi_45s",
        "commands": world_quality_eval_gurobi_45s,
    },
    {"name": "world_quality_eval_scip_45s", "commands": world_quality_eval_scip_45s},
    {
        "name": "world_quality_eval_timefold_45s",
        "commands": world_quality_eval_timefold_45s,
    },
    {
        "name": "world_quality_eval_gurobi_60s",
        "commands": world_quality_eval_gurobi_60s,
    },
    {"name": "world_quality_eval_scip_60s", "commands": world_quality_eval_scip_60s},
    {
        "name": "world_quality_eval_timefold_60s",
        "commands": world_quality_eval_timefold_60s,
    },
    {
        "name": "world_quality_eval_gurobi_300s",
        "commands": world_quality_eval_gurobi_300s,
    },
    {"name": "world_quality_eval_scip_300s", "commands": world_quality_eval_scip_300s},
    {
        "name": "world_quality_eval_timefold_300s",
        "commands": world_quality_eval_timefold_300s,
    },
]

BASE_DIR = os.getcwd()


def wait_until_no_jobs():
    print("\nWaiting for all jobs to finish...")
    while True:
        # Execute squeue --me command
        result = subprocess.run(["squeue", "--me"], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")

        # If only header is present, there are no jobs (except for evaluation job itself)
        if len(lines) <= 2:
            print("All jobs completed.\n")
            return
        else:
            print(f"{len(lines)-2} job(s) still running...")
            time.sleep(120)  # Wait a minute before checking again


def run_evaluation(eval):
    # Go into results folder
    os.chdir("results")
    
    # Create new folder for evaluation (with timestamp)
    folder_name = f"{eval['name']}"
    
    # Skip if folder exists
    if os.path.exists(folder_name):
        return
    
    # Create folder
    os.makedirs(folder_name, exist_ok=False)

    # Switch to the new folder
    os.chdir(folder_name)

    print(f"############# Running {eval['name']} in {os.getcwd()} #############")

    for cmd in eval["commands"]:
        print(f"Executing: {cmd}")
        subprocess.run(cmd, shell=True)

    # Switch back to evaluation root directory
    os.chdir(BASE_DIR)
    


# Run the evaluations
for eval in evaluations:
    run_evaluation(eval)
    wait_until_no_jobs()
    
