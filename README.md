# commonroad-docker-submission

This repository provides a template for creating docker images with motion planners that can be evaluated on https://commonroad.in.tum.de/. The following guide provides the required commands to build and run the docker image.

For general information regarding docker and its installation, please have a look at the [getting started guide for docker](https://docs.docker.com/get-started/) and some helpful tips for [writing dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/).

# Overview: How it works

The dockerized motion planner is executed on the server and generates the solution files that are evaluated afterward.

1. Previously **unknown scenarios** are mounted to the docker container when executing on the server. The scenarios are accessible to the container under the folder `commonroad/scenarios`.
2. When running the container, the **motion planner** has to solve the scenarios under folder `commonroad/scenarios`. A dummy script that iterates through the scenarios can be found in this repository under `/planner/__main__.py`. It uses a scenario iterator that returns the path of the scenario folder of each interactive scenario.
3. If you wish to perform an open-loop planning, you can simply implement your planner in the `motion_planner_interactive` function within `planner/planner.py`; if you wish to perform a close-loop planning, you should implement your own motion planner in the `simulate_scenario` function within `simulation/simulations.py`. The `simulation/` folder should be mounted as a volume to override motion planner script in the container in closed-loop planning.
4. The trajectory driven by the motion planner is then written as a CommonRoad **solution XML file** to the folder `commonroad/solutions`. This folder is also mounted as a volume and the solutions are fetched from there by the CommonRoad server.

# Create a Dockerfile

This repository already contains a template Dockerfile that is based on a base image that can be pulled from `gitlab.lrz.de:5005/tum-cps/commonroad-docker-submission/base` and whose Dockerfile can be found under the path `/base/Dockerfile`. The base image comes with SUMO and the drivability-checker pre-installed. The drivability checker can be removed if not required, SUMO, however, will be required to execute interactive scenarios. 

In either case, the planner has to be executed using an `ENTRYPOINT` so that it gets executed once the container is started, e.g., like in the template Dockerfile:

```Dockerfile
ENTRYPOINT python3.7 /commonroad/planner
```
Please refrain from using `CMD` because this command might be overwritten by external commands when running the container.

### Template
A template for motion planning and generating solutions is provided in `planner/__main__.py`, and it already contains a scenario iterator that iterates through all scenario files under `/commonroad/scenarios/` and write solution files to `/commonroad/solutions/`. There are two separate iterators for non-interactive and interactive scenarios. Which of the iterators needs to be used depends on the competition. Please write only solution files to `/commonroad/solutions/`, since all files in this folder will be uploaded to the evaluation system once the container exits.

# Build and test the docker image locally
Before submitting the image to the CommonRoad server, we suggest testing the container locally using some training scenario files.

The container can be built using the command

```bash
cd commonroad-docker-submission
docker build -t <tag_of_image> .
```

This will copy the `planner/` and `simulation/` folders into the image (you can refer to `Dockerfile`). You should replace `<tag_of_image>` with a valid tag for docker image. We suggest using the format `usernameDockerhub/plannerName:versionID`, where `usernameDockerhub` is your username on [Docker Hub](https://hub.docker.com/) (since the docker image should later be pushed to Docker Hub), and `versionID` specifies the version of your planner. An example could be

```bash
docker build -t usernameDockerhub/dummy:0.1 .
```

In this example, we build an image with a dummy planner from this repository versioned 0.1.

Before running the image, you can put some training scenario files in the local folder `$(pwd)/scenarios` which will be mounted to the image via the argument `-v`. The command for running the image with the mounted scenario and solution folders is:

```bash
docker run \
    --rm \
    -v $(pwd)/scenarios:/commonroad/scenarios \
    -v $(pwd)/solutions:/commonroad/solutions
    usernameDockerhub/dummy:0.1
```
After running, the container is removed automatically due to `--rm` and the solution will be accessible in the local folder `$(pwd)/solutions`.

During development, we can also run the container without building every time after making changes locally. Simply mount planner related files as follows:

```bash
docker run \
    --rm \
    -v $(pwd)/scenarios:/commonroad/scenarios \
    -v $(pwd)/solutions:/commonroad/solutions \
    -v $(pwd)/planner:/commonroad/planner \ # for both open and close loop planning
    -v $(pwd)/simulation:/commonroad-interactive-scenarios/simulation \ # only for close-loop planning
    usernameDockerhub/dummy:0.1
```

This will mount your local folders for scenarios, solutions, and motion planner (which is integrated in `simulations.py` in case of close-loop planning) to the container. Note that you should rebuild an image after finalizing your development before submitting to the Docker Hub in the next section.


# Submit docker image
Before submitting your docker image on the CommonRoad competition page, you should push your image to Docker Hub. And before that, make sure that the image contains your latest planner (this can be achieved by rebuilding the image). To push the image to [Docker Hub](https://hub.docker.com/), use the following commands:

```bash
docker login
docker push <tag_of_image>
```

**Since images on docker hub are public by default, you should choose a generic name so that it cannot be found easily by other competitors.**

The image can now be submitted to a CommonRoad challenge that accepts docker submissions.
The image needs to be submitted in the format `usernameDockerhub/tag` where usernameDockerhub is the username on [docker hub](https://hub.docker.com/) and `tag` is the name of the image.  We strongly suggest to use tags to keep an overview of your submissions and to verify whether the image can be pulled using the submitted URL. Submissions from private docker repositories are currently not supported.

# Information to consider

- The number of available cores on the server is limited. Furthermore, the max. computation time per docker submission is limited and only solutions evaluated until the timeout are considered. Check the competition page for the latest numbers. 
- All ports of the container are blocked and access to the Internet is not possible.
