# commonroad-docker-submission

This repository provides a template for creating docker images with motion planners that can be evaluated on https://commonroad.in.tum.de/. The following guide provides the required commands to build and run the docker image.

For general information regarding docker and its installation, please have a look at the [getting started guide for docker](https://docs.docker.com/get-started/) and some helpful tips for [writing dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/).

# Overview: How it works

The dockerized motion planner is executed on the server and generates the solution files that are evaluated afterward.

1. Previously **unknown scenarios** are mounted to the docker container when executed on the server. The scenarios are accessible in the container under the folder `commonroad/scenarios`.
2. When running the container, the **motion planner** has to solve the scenarios under folder `commonroad/scenarios`. A dummy script that iterates through the scenarios can be found in this repository under `/planner/__main__.py`. It uses a scenario iterator that returns the path of the scenario folder of each interactive scenario.
3. The trajectory driven by the motion planner is then written as a CommonRoad **solution XML file** to the folder `commonroad/solutions`. This folder is also mounted as a volume and the solutions are fetched from there on the CommonRoad server.

# Create a Dockerfile

This repository already contains a template Dockerfile that is based on a base image that can be pulled from `gitlab.lrz.de:5005/tum-cps/commonroad-docker-submission/base` and whose Dockerfile can be found under the path `/base/Dockerfile`. The base image comes with SUMO and the drivability-checker pre-installed. The drivability checker can be removed if not required, SUMO, however, will be required to execute interactive scenarios. 

In either case, the planner has to be executed using an `ENTRYPOINT` so that it gets executed once the container is started, e.g., like in the template Dockerfile:

```Dockerfile
ENTRYPOINT python3.7 /commonroad/planner
```
Please refrain from using `CMD` because this command might be overwritten by external commands when running the container.

### Dummy planner
The dummy planner `planner/__main__.py` already contains a scenario iterator that iterates through all scenario files under `/commonroad/scenarios/` and write solution files to `/commonroad/solutions/`. There are two seperate iterators for non-interactive and interactive scenarios. Which of the iterators needs to be used depends on the competition. Please write only solution files to `/commonroad/solutions/`, since all files in this folder will be uploaded to the evaluation system once the container exits.

# Build and test the docker image locally
Before submitting the image, we suggest testing the container locally using some training scenario files.

The container is built using the command

```bash
cd commonroad-docker-submission
docker build usernameDockerhub/dummy-image:latest
```

In this example, we build an image with a dummy "planner" from this repository, that just copies a solution file to the solution folder. The docker image will be pushed later to dockerhub, so the username `usernameDockerhub` needs to be replaced with your user name, and the image name `dummy-image` and tag `latest` can be chosen as desired.

Before running the image, you can put some training scenario files in the local folder `(PWD)/scenarios` which will be mounted to the image via the argument `-v`. The command for running the image will the mounted folders is:

```bash
docker run \
    --rm \
    -v $(pwd)/scenarios:/commonroad/scenarios \
    -v $(pwd)/solutions:/commonroad/solutions \
    usernameDockerhub/dummy-image:latest
```
After running it, the container is removed automatically due to `--rm` and the solution will be accessible in the local folder `$(PWD)/solutions`.

### Run without building

During development, the container can also be run without building it each time. For that purpose, also mount the folder `(PWD)/planner` or any other folder where the planner is implemented:

```bash
docker run \
    --rm \
    -v $(pwd)/scenarios:/commonroad/scenarios \
    -v $(pwd)/solutions:/commonroad/solutions \
    -v $(pwd)/planner:/commonroad/planner \
    usernameDockerhub/dummy-image:latest
```


# Submit docker image
Before submitting the name of the image on the competition page on CommonRoad, the image needs to be pushed to [docker hub](https://hub.docker.com/):

```bash
docker login
docker push usernameDockerhub/dummy-image:tag
```
 
**Since images on docker hub are public by default, choose a generic name that cannot be found easily by competitors.**

The image can now be submitted to a CommonRoad challenge that accepts docker submissions.
The image needs to be submitted in the format `usernameDockerhub/dummy-image:tag` where usernameDockerhub is the username on [docker hub](https://hub.docker.com/) and `dummy-image:tag` is the name of the image.  We strongly suggest to use tags to keep an overview of your submissions and to verify whether the image can be pulled using the submitted URL. Submissions from private docker repositories are currently not supported.



# Information to consider

- The number of available cores on the server is limited. Furthermore, the max. computation time per docker submission is limited and only solutions evaluated until the timeout are considered. Check the competition page for the latest numbers. 
- All ports of the container are blocked and internet access is not possible.
