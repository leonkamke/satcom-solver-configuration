package com.optimization.solver.model;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonIgnore;

import ai.timefold.solver.core.api.domain.entity.PlanningEntity;
import ai.timefold.solver.core.api.domain.lookup.PlanningId;
import ai.timefold.solver.core.api.domain.valuerange.ValueRangeProvider;
import ai.timefold.solver.core.api.domain.variable.PlanningVariable;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
@PlanningEntity(difficultyComparatorClass = ContactDifficultyComparator.class)
public class ServiceTarget {
    @EqualsAndHashCode.Include
    @PlanningId
    private int id;
    
    private int applicationId;
    private double priority;
    private int nodeId;
    private String requestedOperation;
    @JsonIgnore
    private List<SatellitePass> possibleSatellitePasses;

    @JsonIgnore
    @PlanningVariable(allowsUnassigned = true)
    private SatellitePass assignedPass;

    @JsonIgnore
    @ValueRangeProvider
    public List<SatellitePass> getPossiblesaSatellitePasses() {
        return this.possibleSatellitePasses;
    }

}
