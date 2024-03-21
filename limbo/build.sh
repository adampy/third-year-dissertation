docker build -t proactive-pod-autoscaler:limbo .
docker tag proactive-pod-autoscaler:limbo adamc1234/proactive-pod-autoscaler:limbo # https://jsta.github.io/r-docker-tutorial/04-Dockerhub.html
docker push adamc1234/proactive-pod-autoscaler:limbo