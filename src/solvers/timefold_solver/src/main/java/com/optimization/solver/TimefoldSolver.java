package com.optimization.solver;

import com.optimization.solver.model.Solution;

import ai.timefold.solver.core.api.solver.Solver;
import ai.timefold.solver.core.api.solver.SolverFactory;


public class TimefoldSolver {
    public static void main( String[] args )
    {
        // Read problem instance and prepare planning solution
        String pathProblemInstance = args[0];
        Solution planningSolution = Utils.readProblemInstance(pathProblemInstance);

        // Configure timefold solver
        SolverFactory<Solution> solverFactory = SolverFactory.createFromXmlResource("solverConfig.xml");
        Solver<Solution> timefoldSolver = solverFactory.buildSolver();

        // Run optimization
        planningSolution = timefoldSolver.solve(planningSolution);

        // Filter not assigned contacts
        Utils.filterContacts(planningSolution);

        // Dump solution as json
        Utils.dumpSolution(planningSolution);
    }

    
}
