docker build -t proactive-pod-autoscaler:inference-server .
docker tag proactive-pod-autoscaler:inference-server adamc1234/proactive-pod-autoscaler:inference-server # https://jsta.github.io/r-docker-tutorial/04-Dockerhub.html
docker push adamc1234/proactive-pod-autoscaler:inference-server