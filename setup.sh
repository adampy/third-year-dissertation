# Install Metrics API
kubectl apply -f ./metrics-server/components.yaml

# Install CPA
kubectl apply -f https://github.com/jthomperoo/custom-pod-autoscaler-operator/releases/download/v1.4.0/cluster.yaml

# Install the application
kubectl apply -f ./azure/modified-teastore-ribbon.yaml

# Build PPA image
docker build -t proactive-pod-autoscaler .

# Now apply PPA to all the deployments
kubectl apply -f cpas/cpa-teastore-auth.yaml
kubectl apply -f cpas/cpa-teastore-db.yaml
kubectl apply -f cpas/cpa-teastore-image.yaml
kubectl apply -f cpas/cpa-teastore-persistence.yaml
kubectl apply -f cpas/cpa-teastore-recommender.yaml
kubectl apply -f cpas/cpa-teastore-registry.yaml
kubectl apply -f cpas/cpa-teastore-webui.yaml