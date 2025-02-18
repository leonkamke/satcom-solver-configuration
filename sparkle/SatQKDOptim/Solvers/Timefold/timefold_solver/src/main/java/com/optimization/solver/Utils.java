package com.optimization.solver;

import java.io.File;
import java.io.IOException;
import java.util.LinkedList;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.optimization.solver.model.Contact;
import com.optimization.solver.model.SatellitePass;
import com.optimization.solver.model.ServiceTarget;
import com.optimization.solver.model.Solution;

public class Utils {
    
    @SuppressWarnings("CallToPrintStackTrace")
    public static Solution readProblemInstance(String path) {
        Solution solution = new Solution();
        try {
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

            solution.setServiceTargets(serviceTargets);
            solution.setSatellitePasses(satellitePasses);

            LinkedList<Contact> potentialContacts = new LinkedList<>();
            int id = 0;
            for (SatellitePass sp : satellitePasses) {
                for (ServiceTarget st: serviceTargets) {
                    if (sp.getNodeId() == st.getNodeId() && !isInvalidServiceTarget(sp, st)) {
                        potentialContacts.add(new Contact(id, st, sp));
                        id++;
                    }
                }
            }
            solution.setContacts(potentialContacts);

        } catch (IOException | IllegalArgumentException e) {
            e.printStackTrace();
        }
        
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
    public static void filterContacts(Solution planningSolution) {
        planningSolution.setContacts(planningSolution.getContacts().stream().filter(contact -> contact.getSelected()).toList());
    }

    // Write solution into a json file (will be processed by python super process)
    @SuppressWarnings("CallToPrintStackTrace")
    public static void dumpSolution(Solution planningSolution) {
        String dumpPath = "./tmp/";
        ObjectMapper objectMapper = new ObjectMapper();
        // Register JavaTimeModule to handle LocalDateTime
        objectMapper.registerModule(new JavaTimeModule());
        objectMapper.disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);
        try {
            // Serialize to JSON
            objectMapper.writeValue(new File(dumpPath + "timefold_solution_tmp.json"), planningSolution);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
