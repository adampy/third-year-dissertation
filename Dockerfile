# Adapted from https://github.com/jthomperoo/custom-pod-autoscaler/blob/v1.0.1/example/custom-docker-image/Dockerfile
FROM tensorflow/tensorflow:latest-gpu

WORKDIR /app

# Install wget
RUN apt-get update && apt-get install wget -y

# Install CPA
RUN wget                                                                                                      \
    -qO-                                                                                                      \
    https://github.com/jthomperoo/custom-pod-autoscaler/releases/download/v2.10.0/custom-pod-autoscaler.tar.gz \
    | tar xvz                                                                                                 \
    && mv dist/* /app/

# Remove unused dist directory
RUN rm -r dist/

# Install required packages
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY . /tmp/

# Set up config
ENV configPath /app/config.yaml
COPY config.yaml ./

# Add config, evaluator and metric gathering Py scripts
ADD config.yaml evaluate.py metric.py azure_blob.py lookback.py /

CMD [ "/app/custom-pod-autoscaler" ]