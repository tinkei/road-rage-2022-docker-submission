import commonroad_dc
from commonroad.scenario.scenario import Scenario
from commonroad.common.solution import Solution, CommonRoadSolutionReader
from typing import Optional

# import planner for interactive scenarios
from simulation.simulations import simulate_with_planner


def motion_planner(scenario: Scenario) -> Optional[Solution]:
    """
    Motion planner that takes a scenario and outputs a solution.

    Drivability Checker toolbox (`commonroad_dc`) can be used
    here to make sure the solution is feasible and does not
    collide with other scenario
    elements.
    """

    # Implement your own planner here

    # As a template, load already existing dummy solution and return
    solution_path = "/commonroad/dummy_solutions/dummy_solution_KS2:SM1:CHN_Sha-4_1_T-1:2018b.xml"
    return CommonRoadSolutionReader.open(solution_path)


def motion_planner_interactive(scenario_path: str) -> Optional[Solution]:
    """
    Motion planner that takes the path of the folder with an interactive  scenario folder and outputs a solution.

    Drivability Checker toolbox (`commonroad_dc`) can be used
    here to make sure the solution is feasible and does not
    collide with other scenario
    elements.
    """

    # Implement your own planner here
    # simulate_with_planner(scenario_path,...)

    # As a template, load already existing dummy solution and return
    solution_path = "/commonroad/dummy_solutions/dummy_solution_KS1:TR1:DEU_Frankfurt-73_2_I-1:2020a.xml"
    return CommonRoadSolutionReader.open(solution_path)