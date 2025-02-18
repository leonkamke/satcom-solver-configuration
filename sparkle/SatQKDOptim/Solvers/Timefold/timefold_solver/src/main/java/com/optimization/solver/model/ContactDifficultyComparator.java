package com.optimization.solver.model;

import java.util.Comparator;

public class ContactDifficultyComparator implements Comparator<Contact> {

    @Override
    public int compare(Contact arg0, Contact arg1) {
        return Integer.compare(arg0.getSatellitePass().getOrbitId(), arg1.getSatellitePass().getOrbitId());
    }
    
}
