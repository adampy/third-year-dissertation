# Supply inference URL
export INFERENCE_URL=http://inference-server-service:8080/predict

# Find ReplicaSets
export AUTH_REPLICASET_NAME=$(kubectl get replicaset -l run=teastore-auth -o jsonpath={..metadata.name})
export DB_REPLICASET_NAME=$(kubectl get replicaset -l run=teastore-db -o jsonpath={..metadata.name})
export IMAGE_REPLICASET_NAME=$(kubectl get replicaset -l run=teastore-image -o jsonpath={..metadata.name})
export PERSISTENCE_REPLICASET_NAME=$(kubectl get replicaset -l run=teastore-persistence -o jsonpath={..metadata.name})
export RECOMMENDER_REPLICASET_NAME=$(kubectl get replicaset -l run=teastore-recommender -o jsonpath={..metadata.name})
export REGISTRY_REPLICASET_NAME=$(kubectl get replicaset -l run=teastore-registry -o jsonpath={..metadata.name})
export WEBUI_REPLICASET_NAME=$(kubectl get replicaset -l run=teastore-webui -o jsonpath={..metadata.name})

# Now run all CPAs after passing in the ReplicaSet names
cat auth.yaml | envsubst | kubectl apply -f -
cat db.yaml | envsubst | kubectl apply -f -
cat image.yaml | envsubst | kubectl apply -f -
cat persistence.yaml | envsubst | kubectl apply -f -
cat recommender.yaml | envsubst | kubectl apply -f -
cat registry.yaml | envsubst | kubectl apply -f -
cat webui.yaml | envsubst | kubectl apply -f -