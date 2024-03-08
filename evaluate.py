# See https://custom-pod-autoscaler.readthedocs.io/en/latest/user-guide/getting-started/
# for installation, setup, and autoscaling commands

import json
import sys
import lookback
import requests
from os import environ

#from .models import CollatedMetrics

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
    
def naive_evaluate(metric_spec) -> int:
    # Extract total cpu usage
    total_cpu = [int(pod['Value']) for pod in metric_spec["resource"]["pod_metrics_info"].values()]
    total_requested_cpu = [int(request) for request in metric_spec["resource"]["requests"].values()]
    
    # Calculate average CPU utilization
    avg_cpu = sum(total_cpu) / sum(total_requested_cpu)
    
    curr = metric_spec["current_replicas"]
    if avg_cpu > 0.9 and curr < 10:
        return curr + 2
    elif avg_cpu > 0.8 and curr < 10:
        return curr + 1
    elif avg_cpu < 0.1 and curr > 2:
        return curr - 2
    elif avg_cpu < 0.2 and curr > 1:
        return curr - 1
    else:
        return curr
    
model_mapping = {
    "teastore-webui": "webui",
}
def get_model_name(pod_name: str) -> str | None:
    for key in model_mapping:
        if key in pod_name:
            return model_mapping[key]
    return None

def new_evaluate(metric_spec) -> int:    
    # Extract total cpu usage
    total_cpu = [int(pod['Value']) for pod in metric_spec["resource"]["pod_metrics_info"].values()]
    total_requested_cpu = [int(request) for request in metric_spec["resource"]["requests"].values()]

    # Perform inference
    inference_url = environ.get("INFERENCE_URL")
    if not inference_url:
        raise ValueError("INFERENCE_URL not set")
    with open("temp.txt", "w") as f:
        f.write("meow")
    pod_name = list(metric_spec["resource"]["pod_metrics_info"].keys())[0] # Just take the first pod, we know they are from the same deployment
    newest_element = sum(total_cpu) / 1000
    lookback.append_window(pod_name, newest_element, 10)
    window = lookback.get_pod(pod_name)["lookback"]["data"]
    with open("temp.txt", "w") as f:
        f.write("awdaw")
    r = requests.post(
        inference_url,
        json={
            "model": get_model_name(pod_name),
            "window": window
        }
    )
    
    
    with open("temp.txt", "w") as f:
        f.write(r.text)
    
    prediction = r.json()["prediction"]
    
    with open("temp.txt", "w") as f:
        f.write(f"Prediction: {prediction}\n")

    # Now we have the prediction, we can use it to adjust the target replicas
    # This is the scaling policy
    curr = metric_spec["current_replicas"]
    if prediction > 0.7 * sum(total_requested_cpu) and curr < 5:
        return curr + 1
    elif prediction < 0.3 * sum(total_requested_cpu) and curr > 1:
        return curr - 1
    else:
        return curr

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