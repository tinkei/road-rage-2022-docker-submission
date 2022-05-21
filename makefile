# The list of targets that are going to run when used together
# with `make` command.

# Build the commonroad-submission:base image
build-base:
	@docker build -t gitlab.lrz.de:5005/tum-cps/commonroad-docker-submission/base:1.0.1 base

# Build the current submission based on base image
# Can be run as:
# 	make TAG="mytag" build
# 	or
# 	make build TAG="mytag"
build:
	@docker build -t commonroad-submission:$(TAG) .

# Run the current implementation without building
# Loads the
# 	- scenarios
# 	- solutions
# 	- planner
# folders as volume in order to reflect implementation
# changes directly, and save the solutions for the given
# scenarios.
# Must be executed as:
#	make run PWD=`pwd` TAG="mytag"
run:
	docker run \
		--rm \
		-e PYTHONUNBUFFERED=1 \
		-v $(PWD)/scenarios:/commonroad/scenarios \
		-v $(PWD)/solutions:/commonroad/solutions \
		commonroad-submission:$(TAG)

