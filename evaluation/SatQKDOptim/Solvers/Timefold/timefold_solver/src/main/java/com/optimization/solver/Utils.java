package com.optimization.solver;

import java.io.File;
import java.io.IOException;
import java.security.Provider.Service;
import java.time.Duration;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.ArrayList;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.optimization.solver.model.Contact;
import com.optimization.solver.model.SatellitePass;
import com.optimization.solver.model.ServiceTarget;
import com.optimization.solver.model.Solution;
import com.optimization.solver.model.SolutionConstraintProvider;

import ai.timefold.solver.core.config.solver.SolverConfig;
import ai.timefold.solver.core.config.phase.PhaseConfig;
import ai.timefold.solver.core.config.heuristic.selector.move.generic.chained.SubChainChangeMoveSelectorConfig;
import ai.timefold.solver.core.api.score.buildin.hardsoft.HardSoftScore;
import ai.timefold.solver.core.config.constructionheuristic.ConstructionHeuristicPhaseConfig;
import ai.timefold.solver.core.config.constructionheuristic.ConstructionHeuristicType;
import ai.timefold.solver.core.config.localsearch.LocalSearchPhaseConfig;
import ai.timefold.solver.core.config.localsearch.LocalSearchType;
import ai.timefold.solver.core.config.localsearch.decider.acceptor.AcceptorType;
import ai.timefold.solver.core.config.localsearch.decider.acceptor.LocalSearchAcceptorConfig;
import ai.timefold.solver.core.config.solver.termination.TerminationConfig;

import ai.timefold.solver.core.config.solver.SolverConfig;

public class Utils {

    @SuppressWarnings("CallToPrintStackTrace")
    public static Solution readProblemInstance(String path) throws Exception {
        Solution solution = new Solution();

        File jsonFile = new File(path);

        // Jackson ObjectMapper
        ObjectMapper mapper = new ObjectMapper();

        // Register JavaTimeModule to handle LocalDateTime
        mapper.registerModule(new JavaTimeModule());
        mapper.disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);

        // Read the JSON into a tree structure
        JsonNode root = mapper.readTree(jsonFile);

        // Create lists to store satellite passes and service targets
        LinkedList<SatellitePass> satellitePasses = new LinkedList<>();
        LinkedList<ServiceTarget> serviceTargets = new LinkedList<>();

        // Iterate through the problem instances
        for (JsonNode instance : root) {
            // Read satellite passes
            JsonNode passes = instance.get("satellite_passes");
            if (passes != null) {
                for (JsonNode pass : passes) {
                    SatellitePass satellitePass = mapper.treeToValue(pass, SatellitePass.class);
                    satellitePasses.add(satellitePass);
                }
            }

            // Read service targets
            JsonNode targets = instance.get("service_targets");
            if (targets != null) {
                for (JsonNode target : targets) {
                    ServiceTarget serviceTarget = mapper.treeToValue(target, ServiceTarget.class);
                    serviceTargets.add(serviceTarget);
                }
            }
        }

        for (ServiceTarget st : serviceTargets) {
            LinkedList<SatellitePass> possibleSatellitePasses = new LinkedList<>();
            for (SatellitePass sp : satellitePasses) {
                if (!isInvalidServiceTarget(sp, st)) {
                    possibleSatellitePasses.add(sp);
                }
            }
            st.setPossibleSatellitePasses(possibleSatellitePasses);
        }

        solution.setServiceTargets(serviceTargets);
        solution.setSatellitePasses(satellitePasses);

        return solution;
    }

    // Checks if a contact can serve serivice target st during satellite pass s
    public static boolean isInvalidServiceTarget(SatellitePass s, ServiceTarget st) {
        // Check if contacted node is in service target
        if (s.getNodeId() != st.getNodeId())
            return true;
        return s.getAchievableKeyVolume() == 0.0 && st.getRequestedOperation().equals("QKD");
    }

    // Remove all contacts that are not assigned
    public static void filterServiceTargets(Solution planningSolution) {
        planningSolution.setServiceTargets(
                planningSolution.getServiceTargets().stream().filter(st -> st.getAssignedPass() != null).toList());
    }

    // Remove all contacts that are not assigned
    public static void calculateContacts(Solution planningSolution) {
        LinkedList<Contact> contacts = new LinkedList<>();
        int id = 0;
        for (ServiceTarget st : planningSolution.getServiceTargets()) {
            contacts.add(new Contact(id, st, st.getAssignedPass()));
            id++;
        }
        planningSolution.setContacts(contacts);
    }

    // Write solution into a json file (will be processed by python super process)
    @SuppressWarnings("CallToPrintStackTrace")
    public static void dumpSolution(Solution planningSolution, String filename) throws Exception {
        String dumpPath = "./Tmp/" + filename;
        dumpPath += ".json";
        ObjectMapper objectMapper = new ObjectMapper();
        // Register JavaTimeModule to handle LocalDateTime
        objectMapper.registerModule(new JavaTimeModule());
        objectMapper.disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);

        // Serialize to JSON
        objectMapper.writeValue(new File(dumpPath), planningSolution.getContacts());

    }

    // Read configuration params and create SolverConfig object
    public static SolverConfig getSolverConfig(HashMap<String, String> config) {
        SolverConfig solverConfig = new SolverConfig();
        ArrayList<PhaseConfig> searchPhases = new ArrayList();

        // solverConfig.withRandomSeed(TimefoldSolver.seed);

        // Set the solution class and constraint provider
        solverConfig.setSolutionClass(Solution.class);
        solverConfig.setEntityClassList(List.of(ServiceTarget.class));
        solverConfig.withConstraintProviderClass(SolutionConstraintProvider.class);

        // Set termination config
        TerminationConfig terminationConfig = new TerminationConfig();
        terminationConfig.setSpentLimit(Duration.ofSeconds(TimefoldSolver.maxSolveTime)); // Maximum solving time in seconds
        solverConfig.setTerminationConfig(terminationConfig);

        // Compute runtime for both phases in seconds
        Long ls1SolveTime = TimefoldSolver.maxSolveTime;
        Long ls2Solvetime = TimefoldSolver.maxSolveTime;
        String ls1Type = config.get("ls1Type");
        String ls2Type = config.get("ls2Type");
        if (!ls1Type.equals("NONE") && !ls2Type.equals("NONE")) {
            double fraction = Double.parseDouble(config.get("fractionTime"));
            ls1SolveTime = Math.round(TimefoldSolver.maxSolveTime * fraction);
            ls2Solvetime = TimefoldSolver.maxSolveTime - ls1SolveTime;
        }

        // Construction heuristic phase
        if (!config.get("constructionHeuristicType").equals("NONE")) {
            ConstructionHeuristicPhaseConfig chPhaseConfig = new ConstructionHeuristicPhaseConfig();
            ConstructionHeuristicType chType = null;
            if (config.get("constructionHeuristicType").equals("FIRST_FIT")) {
                chType = ConstructionHeuristicType.FIRST_FIT;
            } else { // First Fit Decreasing
                chType = ConstructionHeuristicType.FIRST_FIT_DECREASING;
            }
            chPhaseConfig.setConstructionHeuristicType(chType);
            searchPhases.add(chPhaseConfig);
        }

        // Local search phase 1
        if (!ls1Type.equals("NONE")) {
            LocalSearchPhaseConfig ls1PhaseConfig = new LocalSearchPhaseConfig();

            // Set termination config
            TerminationConfig ls1TerminationConfig = new TerminationConfig();
            ls1TerminationConfig.setSecondsSpentLimit(ls1SolveTime);
            ls1PhaseConfig.setTerminationConfig(ls1TerminationConfig);

            if (ls1Type.equals("HILL_CLIMBING")) {
                ls1PhaseConfig.setLocalSearchType(LocalSearchType.HILL_CLIMBING);
            } else if (ls1Type.equals("TABU_SEARCH")) {
                ls1PhaseConfig.setLocalSearchType(LocalSearchType.TABU_SEARCH);
            } else if (ls1Type.equals("SIMULATED_ANNEALING")) {
                LocalSearchAcceptorConfig acceptorConfig = new LocalSearchAcceptorConfig();
                acceptorConfig.setSimulatedAnnealingStartingTemperature("1hard/0soft");
                ls1PhaseConfig.setAcceptorConfig(acceptorConfig);
            } else { // Late Acceptance
                ls1PhaseConfig.setLocalSearchType(LocalSearchType.LATE_ACCEPTANCE);
            }

            searchPhases.add(ls1PhaseConfig);
        }

        // Local search phase 2
        if (!ls2Type.equals("NONE")) {
            LocalSearchPhaseConfig ls2PhaseConfig = new LocalSearchPhaseConfig();

            // Set termination config
            TerminationConfig ls2TerminationConfig = new TerminationConfig();
            ls2TerminationConfig.setSecondsSpentLimit(ls2Solvetime);
            ls2PhaseConfig.setTerminationConfig(ls2TerminationConfig);

            if (ls2Type.equals("HILL_CLIMBING")) {
                ls2PhaseConfig.setLocalSearchType(LocalSearchType.HILL_CLIMBING);
            } else if (ls2Type.equals("TABU_SEARCH")) {
                ls2PhaseConfig.setLocalSearchType(LocalSearchType.TABU_SEARCH);
            } else if (ls2Type.equals("SIMULATED_ANNEALING")) {
                LocalSearchAcceptorConfig acceptorConfig = new LocalSearchAcceptorConfig();
                acceptorConfig.setSimulatedAnnealingStartingTemperature("1hard/0soft");
                ls2PhaseConfig.setAcceptorConfig(acceptorConfig);
            } else { // Late Acceptance
                ls2PhaseConfig.setLocalSearchType(LocalSearchType.LATE_ACCEPTANCE);
            }

            searchPhases.add(ls2PhaseConfig);
        }

        // Set the phase configs and return
        solverConfig.setPhaseConfigList(searchPhases);
        return solverConfig;
    }

    public static HashMap<String, String> getConfigHashMap(String[] args) {
        HashMap<String, String> config = new HashMap<>();

        // Read configuration parameters
        for (int i = 0; i < args.length; i++) {
            switch (args[i]) {
                case "-inst": // Skip
                    if (i + 1 < args.length) {
                        i++;
                    }
                    break;
                case "-uuid": // Skip
                    if (i + 1 < args.length) {
                        i++;
                    }
                    break;
                case "-moveThreadCount":
                    if (i + 1 < args.length) {
                        config.put("moveThreadCount", args[i + 1]);
                        i++;
                    }
                    break;
                case "-constructionHeuristicType":
                    if (i + 1 < args.length) {
                        config.put("constructionHeuristicType", args[i + 1]);
                        i++;
                    }
                    break;
                case "-ls1Type":
                    if (i + 1 < args.length) {
                        config.put("ls1Type", args[i + 1]);
                        i++;
                    }
                    break;
                case "-ls2Type":
                    if (i + 1 < args.length) {
                        config.put("ls2Type", args[i + 1]);
                        i++;
                    }
                    break;
                case "-fractionTime":
                    if (i + 1 < args.length) {
                        config.put("fractionTime", args[i + 1]);
                        i++;
                    }
                    break;
            }
        }

        return config;
    }
}
