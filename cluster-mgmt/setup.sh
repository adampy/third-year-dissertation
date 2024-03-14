# Install Metrics API
kubectl apply -f ./metrics-server.yaml

# Install CPA
kubectl apply -f https://github.com/jthomperoo/custom-pod-autoscaler-operator/releases/download/v1.4.0/cluster.yaml

# Install the application
kubectl apply -f ./modified-teastore-ribbon.yaml

# Build PPA image and push to DockerHub
docker build -t proactive-pod-autoscaler .
docker tag proactive-pod-autoscaler:latest adamc1234/proactive-pod-autoscaler:latest # https://jsta.github.io/r-docker-tutorial/04-Dockerhub.html
docker push adamc1234/proactive-pod-autoscaler

# Now apply PPA to all the deployments
kubectl apply -f cpas/auth.yaml
kubectl apply -f cpas/db.yaml
kubectl apply -f cpas/image.yaml
kubectl apply -f cpas/persistence.yaml
kubectl apply -f cpas/recommender.yaml
kubectl apply -f cpas/registry.yaml
kubectl apply -f cpas/webui.yaml
