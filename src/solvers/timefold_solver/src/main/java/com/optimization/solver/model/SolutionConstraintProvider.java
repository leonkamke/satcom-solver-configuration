package com.optimization.solver.model;

import java.math.BigDecimal;
import java.time.Duration;

import com.optimization.solver.Utils;

import ai.timefold.solver.core.api.score.buildin.hardsoftbigdecimal.HardSoftBigDecimalScore;
import ai.timefold.solver.core.api.score.stream.Constraint;
import ai.timefold.solver.core.api.score.stream.ConstraintCollectors;
import ai.timefold.solver.core.api.score.stream.ConstraintFactory;
import ai.timefold.solver.core.api.score.stream.ConstraintProvider;

public class SolutionConstraintProvider implements ConstraintProvider {

    // Minimum time in seconds between two contacts
    private final int t_min = 60;

    @Override
    public Constraint[] defineConstraints(ConstraintFactory constraintFactory) {
        return new Constraint[] {
            // Hard constraint
            nonOverlappingContacts(constraintFactory),
            singleAssignmentPerPass(constraintFactory),
            singleAssignmentPerServiceTarget(constraintFactory),
            validServiceTarget(constraintFactory),
            qkdAndThenPostprocessing(constraintFactory),
            qkdAndPostprocessing(constraintFactory),

            // Soft constraint
            maximizePriorityAndBitRate(constraintFactory)
        };
    }

    private Constraint nonOverlappingContacts(ConstraintFactory constraintFactory) {
        return constraintFactory
            .forEachUniquePair(Contact.class)
            .filter((c1, c2) -> c1.getSelected() && c2.getSelected()
                            && isOverlapping(c1, c2, this.t_min))
            .penalize(HardSoftBigDecimalScore.ONE_HARD)
            .asConstraint("Overlapping contacts conflict");
    }

    private Constraint singleAssignmentPerPass(ConstraintFactory constraintFactory) {
        return constraintFactory
            .forEach(Contact.class)
            .filter(contact -> contact.getSelected())
            .groupBy(contact -> contact.getSatellitePass().getId(), ConstraintCollectors.count())
            .penalize(HardSoftBigDecimalScore.ONE_HARD, (satellitePassId, count) -> {
                if (count > 1) {
                    return 1;
                } else {
                    return 0;
                }
            })
            .asConstraint("Single assignment per pass");
    }

    private Constraint singleAssignmentPerServiceTarget(ConstraintFactory constraintFactory) {
        return constraintFactory
            .forEach(Contact.class)
            .filter(contact -> contact.getSelected())
            .groupBy(contact -> contact.getServiceTarget().getId(), ConstraintCollectors.count())
            .penalize(HardSoftBigDecimalScore.ONE_HARD, (serviceTargetid, count) -> {
                if (count > 1) {
                    return 1;
                } else {
                    return 0;
                }
            })
            .asConstraint("Single assignment per service target");
    }

    private Constraint validServiceTarget(ConstraintFactory constraintFactory) {
        return constraintFactory
            .forEach(Contact.class)
            .filter(contact -> contact.getSelected())
            .filter(contact -> Utils.isInvalidServiceTarget(contact.getSatellitePass(), contact.getServiceTarget()))
            .penalize(HardSoftBigDecimalScore.ONE_HARD)
            .asConstraint("Invalid service target");
    }

    private Constraint qkdAndThenPostprocessing(ConstraintFactory constraintFactory) {
        return constraintFactory
            .forEachUniquePair(Contact.class)
            .filter((c1, c2) -> c1.getSelected() && c2.getSelected() && c1.getServiceTarget().getApplicationId() == c2.getServiceTarget().getApplicationId() && c1.getServiceTarget().getRequestedOperation().equals("QKD") && c2.getServiceTarget().getRequestedOperation().equals("OPTICAL_ONLY"))
            .penalize(HardSoftBigDecimalScore.ONE_HARD, (c1, c2) -> {
                if (c1.getSatellitePass().getStartTime().isBefore(c2.getSatellitePass().getStartTime())) {
                    return 0;
                } else {
                    return 1;
                }
            })
            .asConstraint("For a given application id, first do QKD and afterwards QKD post-processing");
    }

    private Constraint qkdAndPostprocessing(ConstraintFactory constraintFactory) {
        return constraintFactory
            .forEachUniquePair(Contact.class)
            .filter((c1, c2) -> c1.getServiceTarget().getApplicationId() == c2.getServiceTarget().getApplicationId() && c1.getServiceTarget().getRequestedOperation().equals("QKD") && c2.getServiceTarget().getRequestedOperation().equals("OPTICAL_ONLY"))
            .penalize(HardSoftBigDecimalScore.ONE_HARD, (c1, c2) -> {
                if (c1.getSatellitePass().getStartTime().isBefore(c2.getSatellitePass().getStartTime()) && c1.getSelected() && !c2.getSelected()){
                    return 1;
                } else {
                    return 0;
                }
            })
            .asConstraint("For a given application id, QKD post-processing and QKD must happen in the same schedule");
    }

    private Constraint maximizePriorityAndBitRate(ConstraintFactory constraintFactory) {
        return constraintFactory
            .forEach(Contact.class)
            .filter(contact -> contact.getSelected())
            .rewardBigDecimal(HardSoftBigDecimalScore.ONE_SOFT,
                contact -> {
                    double priority = contact.getServiceTarget().getPriority();
                    double achievableKeyVolume = contact.getSatellitePass().getAchievableKeyVolume();
                    double requestedOperation = contact.getServiceTarget().getRequestedOperation().equals("QKD") ? 1 : 0;
                    return new BigDecimal(priority * (1.0 + achievableKeyVolume * requestedOperation));
                })
            .asConstraint("Maximize objective function");
    }

    // Checks if two contacts are considered as overlapping
    private boolean isOverlapping(Contact c1, Contact c2, int minimumGap) {
        Duration gap = Duration.ofMinutes(minimumGap);
        // Check if c1 overlaps or is within minimumGap minutes of c2
        return c1.getSatellitePass().getStartTime()
                .isBefore(c2.getSatellitePass().getEndTime().plus(gap))
                && c1.getSatellitePass().getEndTime()
                        .isAfter(c2.getSatellitePass().getStartTime().minus(gap));
    }

}
