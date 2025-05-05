package com.optimization.solver.model;

import java.time.LocalDateTime;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SatellitePass {
    private int id;
    private int nodeId;
    private LocalDateTime startTime;
    private LocalDateTime endTime;
    private double achievableKeyVolume;
    private int orbitId;
}
