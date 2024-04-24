FROM tensorflow/tensorflow:latest-gpu

WORKDIR /app

# Install required packages
COPY requirements.txt /tmp/requirements.txt
RUN pip install --ignore-installed -r /tmp/requirements.txt
COPY . /tmp/

COPY . .

CMD [ "gunicorn", "app:app", "--bind=0.0.0.0:8080" ]