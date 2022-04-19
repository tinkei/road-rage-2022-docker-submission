FROM gitlab.lrz.de:5005/tum-cps/commonroad-docker-submission/base:1.0.1

COPY ./planner /commonroad/planner

RUN git clone https://gitlab.lrz.de/tum-cps/commonroad-interactive-scenarios.git && \
    pip install -r ./commonroad-interactive-scenarios/requirements.txt

ENV PYTHONPATH="/commonroad-interactive-scenarios/:${PYTHONPATH}"

ENTRYPOINT python3.9 /commonroad/planner
