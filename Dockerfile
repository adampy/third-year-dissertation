# Pull in Python build of CPA
FROM custompodautoscaler/python:latest

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY . /tmp/

# Add config, evaluator and metric gathering Py scripts
ADD config.yaml evaluate.py metric.py lookback.py /