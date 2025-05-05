package com.optimization.solver;

import java.io.FileNotFoundException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;

import com.optimization.solver.model.Solution;

import ai.timefold.solver.core.api.solver.Solver;
import ai.timefold.solver.core.api.solver.SolverFactory;
import ai.timefold.solver.core.config.solver.EnvironmentMode;
import ai.timefold.solver.core.config.solver.SolverConfig;
import ai.timefold.solver.core.config.phase.PhaseConfig;
import ai.timefold.solver.core.config.heuristic.selector.move.generic.chained.SubChainChangeMoveSelectorConfig;
import ai.timefold.solver.core.config.constructionheuristic.ConstructionHeuristicPhaseConfig;
import ai.timefold.solver.core.config.constructionheuristic.ConstructionHeuristicType;
import ai.timefold.solver.core.config.localsearch.LocalSearchPhaseConfig;
import ai.timefold.solver.core.config.localsearch.LocalSearchType;
import ai.timefold.solver.core.config.solver.termination.TerminationConfig;

public class TimefoldSolver {

    // Maximum solving time in seconds
    public static Long maxSolveTime = null;

    // Random seed for solver
    public static Long seed = null;

    public static void main(String[] args) {
        try {
            /*
             * System.setOut(new java.io.PrintStream(new java.io.OutputStream() {
             * public void write(int b) {
             * // Do nothing
             * }
             * }));
             */

            /*
             * System.setErr(new java.io.PrintStream(new java.io.OutputStream() {
             * public void write(int b) {
             * // Do nothing
             * }
             * }));
             */

            // Read max solve time from txt file
            String content = Files.readString(Paths.get("./Solvers/Timefold/max_solve_time.txt")).trim();
            maxSolveTime = Long.parseLong(content);

            // Read instance path, seed, and uuid (for tmp solution file)
            String instancePath = null;
            String uuid = null;
            for (int i = 0; i < 6; i++) {
                switch (args[i]) {
                    case "-inst":
                        if (i + 1 < args.length) {
                            instancePath = args[i + 1];
                            i++;
                        }
                        break;
                    case "-seed":
                        if (i + 1 < args.length) {
                            seed = Long.parseLong(args[i+1]);
                            i++;
                        }
                        break;
                    case "-uuid":
                        if (i + 1 < args.length) {
                            uuid = args[i + 1];
                            i++;
                        }
                        break;
                }
            }

            // Read problem instance and prepare planning solution
            Solution planningSolution = Utils.readProblemInstance(instancePath);

            // Instantiate object for configuration
            HashMap<String, String> config = Utils.getConfigHashMap(args);
            SolverConfig solverConfig = Utils.getSolverConfig(config);

            // Configure timefold solver
            SolverFactory<Solution> solverFactory = SolverFactory.create(solverConfig);
            // SolverFactory<Solution> solverFactory =
            // SolverFactory.createFromXmlResource("solverConfig.xml");
            Solver<Solution> timefoldSolver = solverFactory.buildSolver();

            // Run optimization
            System.out.println("Start solving");
            Solution solution = timefoldSolver.solve(planningSolution);
            System.out.println("Ended solving");

            // Filter not assigned contacts
            Utils.filterServiceTargets(solution);

            // Create contacts
            Utils.calculateContacts(solution);

            // Dump solution as json
            Utils.dumpSolution(solution, uuid);

            System.out.println("Finished Timefold computation");
        } catch (Exception ex) {
            ex.printStackTrace();
        }

    }

}
