package com.optimization.solver.model;

import java.util.Comparator;

public class ContactDifficultyComparator implements Comparator<ServiceTarget> {

    @Override
    public int compare(ServiceTarget arg0, ServiceTarget arg1) {
        return Integer.compare(arg0.getNodeId(), arg1.getNodeId());
    }
    
}
