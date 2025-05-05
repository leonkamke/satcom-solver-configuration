package com.optimization.solver.model;

import java.util.Arrays;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonIgnore;

import ai.timefold.solver.core.api.domain.solution.PlanningEntityCollectionProperty;
import ai.timefold.solver.core.api.domain.solution.PlanningScore;
import ai.timefold.solver.core.api.domain.solution.PlanningSolution;
import ai.timefold.solver.core.api.domain.solution.ProblemFactCollectionProperty;
import ai.timefold.solver.core.api.domain.valuerange.ValueRangeProvider;
import ai.timefold.solver.core.api.score.buildin.hardsoftbigdecimal.HardSoftBigDecimalScore;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@PlanningSolution
public class Solution {

    @JsonIgnore
    @PlanningEntityCollectionProperty
    private List<ServiceTarget> serviceTargets;

    @JsonIgnore
    @ProblemFactCollectionProperty
    private List<SatellitePass> satellitePasses;

    private List<Contact> contacts;

    @JsonIgnore
    @PlanningScore
    private HardSoftBigDecimalScore score;

    @ValueRangeProvider(id = "booleanRange")
    public List<Boolean> getBooleanValues() {
        return Arrays.asList(true, false);
    }
}

