package com.optimization.solver.model;

import ai.timefold.solver.core.api.domain.entity.PlanningEntity;
import ai.timefold.solver.core.api.domain.lookup.PlanningId;
import ai.timefold.solver.core.api.domain.variable.PlanningVariable;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@PlanningEntity
public class Contact {
    
    @PlanningId
    private int id;

    private ServiceTarget serviceTarget;
    private SatellitePass satellitePass;

    @PlanningVariable(valueRangeProviderRefs = "booleanRange")
    private Boolean selected = false;

    public Contact(int id, ServiceTarget serviceTarget, SatellitePass satellitePass) {
        this.id = id;
        this.serviceTarget = serviceTarget;
        this.satellitePass = satellitePass;
    }
}
