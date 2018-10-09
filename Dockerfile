FROM python:3.7.0-alpine

LABEL maintainer "mats16 <mats.kazuki@gmail.com>"

RUN pip install boto3==1.9.17 requests==2.19.1

COPY ecs/ /opt/ecs/

CMD python -u /opt/ecs/check_termination.py
