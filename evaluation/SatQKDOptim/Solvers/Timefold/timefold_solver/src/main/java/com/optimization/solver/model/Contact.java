package com.optimization.solver.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Contact {
    private int id;
    private ServiceTarget serviceTarget;
    private SatellitePass satellitePass;
}
