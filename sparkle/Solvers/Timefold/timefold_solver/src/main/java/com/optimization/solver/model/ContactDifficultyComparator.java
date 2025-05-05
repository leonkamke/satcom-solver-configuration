package com.optimization.solver.model;

import java.util.Comparator;

public class ContactDifficultyComparator implements Comparator<ServiceTarget> {

    @Override
    public int compare(ServiceTarget arg0, ServiceTarget arg1) {
        if (arg0.getPossibleSatellitePasses() == null || arg0.getPossibleSatellitePasses().size() == 0) {
            return 0;
        }
        if (arg1.getPossibleSatellitePasses() == null || arg1.getPossibleSatellitePasses().size() == 0) {
            return 0;
        }
        int orbit0 = arg0.getPossibleSatellitePasses().get(0).getOrbitId();
        int orbit1 = arg1.getPossibleSatellitePasses().get(0).getOrbitId();
        
        return Integer.compare(orbit0, orbit1);
    }
    
}
