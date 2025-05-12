import os
import time
import subprocess

####################### max_solve_time = 30s #############################################
##########################################################################################
## SCIP
europe_quality_eval_scip_100s_30s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/SCIP",
    "sed -i '1s/.*/30/' ./Solvers/SCIP/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 100/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 60 --objectives quality:max",
]

europe_quality_eval_scip_1000s_30s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/SCIP",
    "sed -i '1s/.*/30/' ./Solvers/SCIP/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 1000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 60 --objectives quality:max",
]

europe_quality_eval_scip_10000s_30s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/SCIP",
    "sed -i '1s/.*/30/' ./Solvers/SCIP/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 10000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 60 --objectives quality:max",
]

### Timefold

europe_quality_eval_timefold_100s_30s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Timefold",
    "sed -i '1s/.*/30/' ./Solvers/Timefold/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 100/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 60 --objectives quality:max",
]

europe_quality_eval_timefold_1000s_30s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Timefold",
    "sed -i '1s/.*/30/' ./Solvers/Timefold/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 1000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 60 --objectives quality:max",
]

europe_quality_eval_timefold_10000s_30s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Timefold",
    "sed -i '1s/.*/30/' ./Solvers/Timefold/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 10000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 60 --objectives quality:max",
]

### Gurobi 
europe_quality_eval_gurobi_100s_30s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Gurobi",
    "sed -i '1s/.*/30/' ./Solvers/Gurobi/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 100/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 60 --objectives quality:max",
]

europe_quality_eval_gurobi_1000s_30s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Gurobi",
    "sed -i '1s/.*/30/' ./Solvers/Gurobi/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 1000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 60 --objectives quality:max",
]

europe_quality_eval_gurobi_10000s_30s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Gurobi",
    "sed -i '1s/.*/30/' ./Solvers/Gurobi/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 10000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 60 --objectives quality:max",
]

####################### max_solve_time = 60s #############################################
##########################################################################################
## SCIP
europe_quality_eval_scip_100s_60s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/SCIP",
    "sed -i '1s/.*/60/' ./Solvers/SCIP/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 100/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 90 --objectives quality:max",
]

europe_quality_eval_scip_1000s_60s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/SCIP",
    "sed -i '1s/.*/60/' ./Solvers/SCIP/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 1000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 90 --objectives quality:max",
]

europe_quality_eval_scip_10000s_60s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/SCIP",
    "sed -i '1s/.*/60/' ./Solvers/SCIP/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 10000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 90 --objectives quality:max",
]

### Timefold

europe_quality_eval_timefold_100s_60s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Timefold",
    "sed -i '1s/.*/60/' ./Solvers/Timefold/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 100/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 90 --objectives quality:max",
]

europe_quality_eval_timefold_1000s_60s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Timefold",
    "sed -i '1s/.*/60/' ./Solvers/Timefold/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 1000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 90 --objectives quality:max",
]

europe_quality_eval_timefold_10000s_60s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Timefold",
    "sed -i '1s/.*/60/' ./Solvers/Timefold/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 10000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 90 --objectives quality:max",
]

### Gurobi 
europe_quality_eval_gurobi_100s_60s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Gurobi",
    "sed -i '1s/.*/60/' ./Solvers/Gurobi/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 100/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 90 --objectives quality:max",
]

europe_quality_eval_gurobi_1000s_60s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Gurobi",
    "sed -i '1s/.*/60/' ./Solvers/Gurobi/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 1000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 90 --objectives quality:max",
]

europe_quality_eval_gurobi_10000s_60s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Gurobi",
    "sed -i '1s/.*/60/' ./Solvers/Gurobi/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 10000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 90 --objectives quality:max",
]



####################### max_solve_time = 300s #############################################
##########################################################################################
## SCIP
europe_quality_eval_scip_100s_300s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/SCIP",
    "sed -i '1s/.*/300/' ./Solvers/SCIP/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 100/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 330 --objectives quality:max",
]

europe_quality_eval_scip_1000s_300s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/SCIP",
    "sed -i '1s/.*/300/' ./Solvers/SCIP/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 1000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 330 --objectives quality:max",
]

europe_quality_eval_scip_10000s_300s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/SCIP",
    "sed -i '1s/.*/300/' ./Solvers/SCIP/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 10000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 330 --objectives quality:max",
]

### Timefold

europe_quality_eval_timefold_100s_300s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Timefold",
    "sed -i '1s/.*/300/' ./Solvers/Timefold/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 100/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 330 --objectives quality:max",
]

europe_quality_eval_timefold_1000s_300s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Timefold",
    "sed -i '1s/.*/300/' ./Solvers/Timefold/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 1000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 330 --objectives quality:max",
]

europe_quality_eval_timefold_10000s_300s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Timefold",
    "sed -i '1s/.*/300/' ./Solvers/Timefold/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 10000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 330 --objectives quality:max",
]

### Gurobi 
europe_quality_eval_gurobi_100s_300s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Gurobi",
    "sed -i '1s/.*/300/' ./Solvers/Gurobi/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 100/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 330 --objectives quality:max",
]

europe_quality_eval_gurobi_1000s_300s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Gurobi",
    "sed -i '1s/.*/300/' ./Solvers/Gurobi/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 1000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 330 --objectives quality:max",
]

europe_quality_eval_gurobi_10000s_300s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Gurobi",
    "sed -i '1s/.*/300/' ./Solvers/Gurobi/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 10000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 330 --objectives quality:max",
]

####################### max_solve_time = 600s #############################################
##########################################################################################
## SCIP
europe_quality_eval_scip_100s_600s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/SCIP",
    "sed -i '1s/.*/600/' ./Solvers/SCIP/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 100/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 630 --objectives quality:max",
]

europe_quality_eval_scip_1000s_600s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/SCIP",
    "sed -i '1s/.*/600/' ./Solvers/SCIP/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 1000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 630 --objectives quality:max",
]

europe_quality_eval_scip_10000s_600s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/SCIP",
    "sed -i '1s/.*/600/' ./Solvers/SCIP/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 10000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/SCIP --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 630 --objectives quality:max",
]

### Timefold

europe_quality_eval_timefold_100s_600s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Timefold",
    "sed -i '1s/.*/600/' ./Solvers/Timefold/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 100/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 630 --objectives quality:max",
]

europe_quality_eval_timefold_1000s_600s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Timefold",
    "sed -i '1s/.*/600/' ./Solvers/Timefold/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 1000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 630 --objectives quality:max",
]

europe_quality_eval_timefold_10000s_600s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Timefold",
    "sed -i '1s/.*/600/' ./Solvers/Timefold/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 10000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Timefold --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 630 --objectives quality:max",
]

### Gurobi 
europe_quality_eval_gurobi_100s_600s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Gurobi",
    "sed -i '1s/.*/600/' ./Solvers/Gurobi/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 100/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 630 --objectives quality:max",
]

europe_quality_eval_gurobi_1000s_600s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Gurobi",
    "sed -i '1s/.*/600/' ./Solvers/Gurobi/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 1000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 630 --objectives quality:max",
]

europe_quality_eval_gurobi_10000s_600s = [
    "sparkle initialise",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Train",
    "sparkle add_instances ../../SatQKDOptim/Instances/Dataset_Europe_General_Test",
    "sparkle add_solver ../../SatQKDOptim/Solvers/Gurobi",
    "sed -i '1s/.*/600/' ./Solvers/Gurobi/max_solve_time.txt",
    "rm -rf ./Settings && cp -r ../../Settings .",
    "sed -i '2s/.*/objectives = quality:max/' ./Settings/sparkle_settings.ini",
    "sed -i '13s/.*/wallclock_time = 10000/' ./Settings/sparkle_settings.ini",
    "sed -i '31s/.*/time = 04:00:00/' ./Settings/sparkle_settings.ini",
    "sparkle configure_solver --solver Solvers/Gurobi --instance-set-train Instances/Dataset_Europe_General_Train --instance-set-test Instances/Dataset_Europe_General_Test --target-cutoff-time 630 --objectives quality:max",
]



# List of evaluations
evaluations_30s = [
   {
      "name": "europe_quality_eval_scip_100s_300s",
      "commands": europe_quality_eval_scip_100s_300s,
   }, 
   {
      "name": "europe_quality_eval_scip_1000s_300s",
      "commands": europe_quality_eval_scip_1000s_300s,
   }, 
   {
      "name": "europe_quality_eval_scip_10000s_300s",
      "commands": europe_quality_eval_scip_10000s_300s,
   }, 
    {
       "name": "europe_quality_eval_timefold_100s_300s",
       "commands": europe_quality_eval_timefold_100s_300s,
    }, 
   {
      "name": "europe_quality_eval_timefold_1000s_300s",
      "commands": europe_quality_eval_timefold_1000s_300s,
   }, 
   {
      "name": "europe_quality_eval_timefold_10000s_300s",
      "commands": europe_quality_eval_timefold_10000s_300s,
   }, 
   {
      "name": "europe_quality_eval_gurobi_100s_300s",
      "commands": europe_quality_eval_gurobi_100s_300s,
   }, 
   {
      "name": "europe_quality_eval_gurobi_1000s_300s",
      "commands": europe_quality_eval_gurobi_1000s_300s,
   }, 
   {
      "name": "europe_quality_eval_gurobi_10000s_300s",
      "commands": europe_quality_eval_gurobi_10000s_300s,
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
            time.sleep(300)  # Wait five minutes before checking again


def run_evaluation(eval):
    # Go into results folder
    os.chdir("convergence_eval_general")

    # Create new folder for evaluation (with timestamp)
    folder_name = f"{eval['name']}"

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
for eval in evaluations_30s:
    # Skip if folder exists
    if os.path.exists(f"./results/{eval['name']}"):
        continue
    run_evaluation(eval)
    # wait_until_no_jobs()
