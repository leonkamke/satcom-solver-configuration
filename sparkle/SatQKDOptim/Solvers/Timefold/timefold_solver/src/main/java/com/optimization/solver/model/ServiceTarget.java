package com.optimization.solver.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ServiceTarget {
    private int id;
    private int applicationId;
    private double priority;
    private int nodeId;
    private String requestedOperation;
}
