"""
Creation of problem instances based on the article:
'QUARC: Quantum Research Cubesat—A Constellation for Quantum Communication'
Link: https://www.mdpi.com/2410-387X/4/1/7
"""


# Approximated key rate depending on elevation angle of satellite
def quarcKeyRateApproximation(elevation):
    return -0.0145 * (elevation**3) + 2.04 * (elevation**2) - 20.65 * elevation + 88.42

