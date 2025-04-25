package com.optimization.solver;

import java.io.FileNotFoundException;

import com.optimization.solver.model.Solution;

import ai.timefold.solver.core.api.solver.Solver;
import ai.timefold.solver.core.api.solver.SolverFactory;

public class TimefoldSolver {
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

            String instancePath = null;
            String uuid = null;

            for (int i = 0; i < 4; i++) {
                switch (args[i]) {
                    case "-inst":
                        if (i + 1 < args.length) {
                            instancePath = args[i + 1];
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

            // Configure timefold solver
            SolverFactory<Solution> solverFactory = SolverFactory.createFromXmlResource("solverConfig.xml");
            Solver<Solution> timefoldSolver = solverFactory.buildSolver();

            // Run optimization
            System.out.println("Start solving");
            Solution solution = timefoldSolver.solve(planningSolution);
            System.out.println("Ended solving");

            // Filter not assigned contacts
            Utils.filterContacts(solution);

            // Dump solution as json
            Utils.dumpSolution(solution, uuid);

            System.out.println("Finished Timefold computation");
        } catch (Exception ex) {
            ex.printStackTrace();
        }

    }

}
