FROM gitlab.lrz.de:5005/tum-cps/commonroad-docker-submission/base:1.0.1

RUN git clone https://gitlab.lrz.de/tum-cps/commonroad-interactive-scenarios.git && \
    pip install -r ./commonroad-interactive-scenarios/requirements.txt

ENV PYTHONPATH="/commonroad-interactive-scenarios/:${PYTHONPATH}"

COPY ./planner /commonroad/planner
COPY ./simulation /commonroad-interactive-scenarios/simulation

ENTRYPOINT python3.9 /commonroad/planner
