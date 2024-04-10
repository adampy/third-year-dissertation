# Build PPA image and push to DockerHub
docker build -t proactive-pod-autoscaler .
docker tag proactive-pod-autoscaler:latest adamc1234/proactive-pod-autoscaler:latest # https://jsta.github.io/r-docker-tutorial/04-Dockerhub.html
docker push adamc1234/proactive-pod-autoscaler