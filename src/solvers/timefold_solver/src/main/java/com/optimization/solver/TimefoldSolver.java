package com.optimization.solver;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.optimization.solver.model.SatellitePass;
import com.optimization.solver.model.ServiceTarget;

public class TimefoldSolver {
    public static void main( String[] args )
    {
        try {
            String pathProblemInstance = "/home/leon/code/satellite-operations-planning/src/input/data/problem_instance_europe_1day.json";
            File jsonFile = new File(pathProblemInstance);

            // Jackson ObjectMapper
            ObjectMapper mapper = new ObjectMapper();

            // Read the JSON into a tree structure
            JsonNode root = mapper.readTree(jsonFile);

            // Create lists to store satellite passes and service targets
            List<SatellitePass> satellitePasses = new ArrayList<>();
            List<ServiceTarget> serviceTargets = new ArrayList<>();

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

            // Print the results
            System.out.println("Satellite Passes:");
            satellitePasses.forEach(System.out::println);

            System.out.println("\nService Targets:");
            serviceTargets.forEach(System.out::println);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
