package com.optimization.solver.model;

import java.math.BigDecimal;
import java.time.Duration;
import java.time.LocalDate;

import com.optimization.solver.Utils;

import ai.timefold.solver.core.api.score.buildin.hardsoftbigdecimal.HardSoftBigDecimalScore;
import ai.timefold.solver.core.api.score.stream.Constraint;
import ai.timefold.solver.core.api.score.stream.ConstraintCollectors;
import ai.timefold.solver.core.api.score.stream.ConstraintFactory;
import ai.timefold.solver.core.api.score.stream.ConstraintProvider;
import ai.timefold.solver.core.api.score.stream.Joiners;

public class SolutionConstraintProvider implements ConstraintProvider {

    // Minimum time in seconds between two contacts
    private final int t_min = 60;

    @Override
    public Constraint[] defineConstraints(ConstraintFactory constraintFactory) {
        return new Constraint[] {
                // Hard constraint
                satellitePassUsedAtMostOnce(constraintFactory),
                overlappingContacts(constraintFactory),
                targetUsedAtMostOnce(constraintFactory),

                // Soft constraint
                maximizeObjective(constraintFactory)
        };
    }


    private Constraint targetUsedAtMostOnce(ConstraintFactory constraintFactory) {
    return constraintFactory.from(ServiceTarget.class)
            .filter(st -> st.getAssignedPass() != null)
            .groupBy(ServiceTarget::getId, ConstraintCollectors.count())
            .filter((id, count) -> count > 1)
            .penalize("Service target assigned more than once", HardSoftBigDecimalScore.ONE_HARD);
    }

    private Constraint satellitePassUsedAtMostOnce(ConstraintFactory constraintFactory) {
        return constraintFactory.from(ServiceTarget.class)
                .filter(st -> st.getAssignedPass() != null)
                .groupBy(ServiceTarget::getAssignedPass, ConstraintCollectors.count())
                .filter((sp, count) -> count > 1)
                .penalize("Satellite pass used more than once", HardSoftBigDecimalScore.ONE_HARD);
    }

    private Constraint overlappingContacts(ConstraintFactory constraintFactory) {
        return constraintFactory.forEachUniquePair(ServiceTarget.class)
                .filter((st1, st2) -> {
                    SatellitePass p1 = st1.getAssignedPass();
                    SatellitePass p2 = st2.getAssignedPass();
                    if (p1 == null || p2 == null)
                        return false;

                    return isOverlapping(p1, p2, t_min);
                })
                .penalize("Overlapping contacts", HardSoftBigDecimalScore.ONE_HARD);
    }

    private Constraint enforceQkdBeforePostProcessing(ConstraintFactory constraintFactory) {
        return constraintFactory.forEachUniquePair(ServiceTarget.class,
                Joiners.equal(ServiceTarget::getApplicationId))
                .filter((st1, st2) -> {
                    SatellitePass p1 = st1.getAssignedPass();
                    SatellitePass p2 = st2.getAssignedPass();
                    if (p1 == null || p2 == null)
                        return false;

                    // st1 is QKD, st2 is Post-Processing
                    if (st1.getRequestedOperation().equals("QKD") && !st2.getRequestedOperation().equals("QKD")) {
                        return p1.getStartTime().isAfter(p2.getStartTime());
                    }
                    return false;
                })
                .penalize("QKD must happen before Post-Processing", HardSoftBigDecimalScore.ONE_HARD);
    }

    private Constraint maximizeObjective(ConstraintFactory constraintFactory) {
        return constraintFactory.from(ServiceTarget.class)
                .filter(st -> st.getAssignedPass() != null)
                .rewardBigDecimal("Maximize weighted priority", HardSoftBigDecimalScore.ONE_SOFT,
                        st -> {
                            double volume = st.getRequestedOperation().equals("QKD")
                                    ? st.getAssignedPass().getAchievableKeyVolume()
                                    : 0.0;
                            return new BigDecimal(st.getPriority() * (1 + volume));
                        });
    }

    // Checks if two contacts are considered as overlapping
    private boolean isOverlapping(SatellitePass sp1, SatellitePass sp2, int minimumGap) {
        Duration minGap = Duration.ofSeconds(minimumGap);
        long gap;
        if (sp1.getEndTime().isBefore(sp2.getStartTime())) {
            gap = Duration.between(sp1.getEndTime(), sp2.getStartTime()).getSeconds();
        } else if (sp2.getEndTime().isBefore(sp1.getStartTime())) {
            gap = Duration.between(sp2.getEndTime(), sp1.getStartTime()).getSeconds();
        } else {
            return true;
        }
        return gap < minimumGap;
    }

}
