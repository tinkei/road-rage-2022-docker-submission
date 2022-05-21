import os.path
import signal

from commonroad.common.solution import Solution, CommonRoadSolutionWriter

# Load planner module
from planner import motion_planner, motion_planner_interactive
from iterator import scenario_iterator_interactive, scenario_iterator_non_interactive

import os
import sys



# Does not work on Windows: https://stackoverflow.com/questions/492519/timeout-on-a-function-call
def timeout_handler(signum, frame):
    print(f'Execution timed out.')
    raise TimeoutError(f'Path planning exceeded alloted time.')

def save_solution(solution: Solution, path: str) -> None:
    """
    Save the given solution to the given path.
    """
    return CommonRoadSolutionWriter(solution).write_to_file(
        output_path=path,
        overwrite=True,
        pretty=True
    )



# Run Main Process
if __name__ == "__main__":

    print("Started main process.")
    print(f'PID: {os.getpid()}')
    # print(list(scenario_iterator_non_interactive(scenario_dir)))
    # print(list(scenario_iterator_interactive(scenario_dir)))

    scenario_dir = "/commonroad/scenarios"
    solution_dir = "/commonroad/solutions"

    timeout = 180



    # solve all non-interactive scenarios
    for scenario, planning_problem_set in scenario_iterator_non_interactive(scenario_dir):

        memory_error = False
        name_scenario = str(scenario.scenario_id)
        print(f"Processing scenario {str(scenario.scenario_id)} ...")

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)
        try:
            solution = motion_planner(scenario, solution_dir)
            signal.alarm(0) # Cancel timout countdown.
        except TimeoutError as e:
            print(f'{name_scenario}: Timed out.')
        except MemoryError as e:
            print(f'{name_scenario}: Frontier too large or exceeded memory use limit.')
            memory_error = True
        except Exception as e:
            import traceback
            print(f'{name_scenario}: Exception {e} caught.')
            print(f'{name_scenario}: {repr(e)}.')
            print(traceback.format_exc())
        finally:
            signal.alarm(0) # Cancel timout countdown.
            if memory_error:
                # Restart kernel to release memory. Don't know how to do that on Docker...
                pass



    # solve all interactive scenarios
    for scenario_path in scenario_iterator_interactive(scenario_dir):

        memory_error = False
        name_scenario = os.path.basename(scenario_path)
        print(f"Processing scenario {os.path.basename(scenario_path)} ...")

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)
        try:
            solution = motion_planner_interactive(scenario_path, solution_dir)
            signal.alarm(0) # Cancel timout countdown.
        except TimeoutError as e:
            print(f'{name_scenario}: Timed out.')
        except MemoryError as e:
            print(f'{name_scenario}: Frontier too large or exceeded memory use limit.')
            memory_error = True
        except Exception as e:
            import traceback
            print(f'{name_scenario}: Exception {e} caught.')
            print(f'{name_scenario}: {repr(e)}.')
            print(traceback.format_exc())
        finally:
            signal.alarm(0) # Cancel timout countdown.
            if memory_error:
                # Restart kernel to release memory. Don't know how to do that on Docker...
                pass
