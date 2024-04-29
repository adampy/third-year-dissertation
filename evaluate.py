# See https://custom-pod-autoscaler.readthedocs.io/en/latest/user-guide/getting-started/
# for installation, setup, and autoscaling commands

import json
import sys
import lookback
import requests
from os import environ
import math

WINDOW_LENGTH = 15
THRESHOLD = 0.7
HORIZON = 1

# EXAMPLE SPEC INPUT
# {
#     "current_replicas": 2,
#     "spec": {
#     "type": "Resource",
#     "resource": {
#         "name": "cpu",
#         "target": {
#         "type": "Utilization"
#         }
#     }
#     },
#     "resource": {
#     "pod_metrics_info": {
#         "teastore-webui-84788ccd89-cw727": {
#             "Timestamp": "2024-02-20T23:30:07Z",
#             "Window": 15014000000,
#             "Value": 79
#         },
#         "teastore-webui-84788ccd89-n8974": {
#             "Timestamp": "2024-02-20T23:30:07Z",
#             "Window": 15012000000,
#             "Value": 61
#         }
#     },
#     "requests": {
#         "teastore-webui-84788ccd89-cw727": 200,
#         "teastore-webui-84788ccd89-n8974": 200
#     },
#     "ready_pod_count": 2,
#     "ignored_pods": {},
#     "missing_pods": {},
#     "total_pods": 2,
#     "timestamp": "2024-02-20T23:30:07Z"
#     }
# }

def main():
    # Parse provided spec into a dict
    spec = json.loads(sys.stdin.read())
    
    with open("evaluate_input.json", "w") as f:
        f.write(json.dumps(spec))
    
    evaluate(spec)
    
def get_model_name(pod_name: str) -> str | None:
    models = ["auth", "image", "persistence", "recommender", "webui"]
    for model in models:
        if model in pod_name:
            return model
    raise ValueError(f"Model not found in pod name {pod_name}")

def new_evaluate(metric_spec) -> int:
    # Extract total cpu usage
    total_cpu = [int(pod['Value']) for pod in metric_spec["resource"]["pod_metrics_info"].values()]
    total_requested_cpu = [int(request) for request in metric_spec["resource"]["requests"].values()]

    # Perform inference
    inference_url = environ.get("INFERENCE_URL")
    if not inference_url:
        raise ValueError("INFERENCE_URL not set")

    # Get service name
    pod_name = list(metric_spec["resource"]["pod_metrics_info"].keys())[0] # Just take the first pod, we know they are from the same deployment
    service_name = get_model_name(pod_name)
    
    # Use lookback window to get inference from inference server
    newest_element = sum(total_cpu) / 1000 # Convert from millicores to cores
    lookback.append_window(service_name, newest_element, WINDOW_LENGTH)
    window = lookback.get_pod(service_name)["lookback"]["data"]
    r = requests.post(
        inference_url,
        json={
            "model": service_name,
            "window": window,
            "horizon": HORIZON
        }
    )
    if r.status_code != 200:
        raise ValueError(f"Failed to get prediction: {r.status_code} {r.text}")

    # Get prediction from horizon
    horizon = r.json()["horizon"]
    prediction = horizon[-1] # Use the last value in horizon as prediction

    # Now we have the prediction, we can use it to adjust the target replicas
    # This is the scaling policy - we use the same formula as K8 but adjusted for prediction
    curr = metric_spec["current_replicas"]
    usage = prediction / (sum(total_requested_cpu) / 1000) # Convert total into millicores
    new_replicas = math.ceil(curr * (usage / THRESHOLD))
    
    with open("evaluate_output.json", "a+") as f:
        f.write(f"Total requested: {(sum(total_requested_cpu) / 1000)}, prediction: {prediction}, current replicas: {curr}, usage: {usage}, new replicas: {new_replicas}\n")
    
    return new_replicas

def evaluate(spec):
    try:
        # Get values from spec
        metric_spec = json.loads(spec["metrics"][0]["value"])
        
        # Based on average CPU utilization, adjust target replicas
        new_replicas = new_evaluate(metric_spec)
            
        # Output evaluation as JSON to CPA resource
        sys.stdout.write(json.dumps({"targetReplicas": new_replicas}))
            
    except ValueError as err:
        # If not an integer, output error
        sys.stderr.write(f"Invalid metric value: {err}")
        exit(1)

if __name__ == "__main__":
    main()
