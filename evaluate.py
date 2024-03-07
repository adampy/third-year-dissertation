# See https://custom-pod-autoscaler.readthedocs.io/en/latest/user-guide/getting-started/
# for installation, setup, and autoscaling commands

import json
import sys
import numpy as np

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # Supress TF info and warnings (obtained from https://stackoverflow.com/questions/35911252/disable-tensorflow-debugging-information)
from keras.models import load_model
import azure_blob
import lookback
from typing import Optional

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
    "teastore-webui": "webui_lstm_model-w10.keras",
}
def get_model_name(pod_name: str) -> Optional[str]:
    for key in model_mapping:
        if key in pod_name:
            return model_mapping[key]
    return None

def new_evaluate(metric_spec) -> int:
    # Extract total cpu usage
    total_cpu = [int(pod['Value']) for pod in metric_spec["resource"]["pod_metrics_info"].values()]
    total_requested_cpu = [int(request) for request in metric_spec["resource"]["requests"].values()]

    # Get ML model - all given metrics will be of the same pod, so we can just use the first one
    pod_name = list(metric_spec["resource"]["pod_metrics_info"].keys())[0]
    model_name = get_model_name(pod_name)
    azure_blob.load_blob_file(model_name) # Download model and store locally
    model = load_model(model_name) # Load from local
    
    # Perform inference
    newest_element = sum(total_cpu) / 1000
    #lookback.append_window(pod_name, newest_element, 10)
    #window = lookback.get_pod(pod_name)["lookback"]["data"]
    window = [0.1, 0.1, 0.2, 0.3, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1]
    window = np.array(window)
    window = window.reshape(-1, 1, 10)

    prediction = model.predict(window, verbose=0)[0][0] # verbose=0 to suppress TF info from stdout - since we require that only the JSON is placed into this

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