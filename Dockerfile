FROM gitlab.lrz.de:5005/tum-cps/commonroad-docker-submission/base:1.0.1

RUN git clone https://gitlab.lrz.de/tum-cps/commonroad-interactive-scenarios.git && \
    pip install -r ./commonroad-interactive-scenarios/requirements.txt

ENV PYTHONPATH="/commonroad-interactive-scenarios/:${PYTHONPATH}"

COPY ./commonroad-search/SMP /commonroad-search/SMP
COPY ./commonroad-search/requirements.txt /commonroad-search/requirements.txt
RUN ls -la /commonroad-search
RUN ls -la /commonroad-search/SMP
RUN pip install -r ./commonroad-search/requirements.txt
RUN pip install psutil commonroad-route-planner

ENV PYTHONPATH="/commonroad-search/:${PYTHONPATH}"

COPY ./planner /commonroad/planner
RUN ls -la /commonroad/planner

COPY ./simulation /commonroad-interactive-scenarios/simulation
RUN ls -la /commonroad-interactive-scenarios/simulation

COPY ./my_motion_primitives /my_motion_primitives
RUN ls -la /my_motion_primitives

COPY ./my_automatons /my_automatons
RUN ls -la /my_automatons

# ENTRYPOINT python3.9 /commonroad/planner
ENTRYPOINT ["python3.9", "/commonroad/planner"]
