# See https://custom-pod-autoscaler.readthedocs.io/en/latest/user-guide/getting-started/
# for installation, setup, and autoscaling commands

import json
import sys

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
    evaluate(spec)

def evaluate(spec):
    try:
        # Get values from spec
        metric_spec = json.loads(spec["metrics"][0]["value"])
        
        total_cpu = [int(pod['Value']) for pod in metric_spec["resource"]["pod_metrics_info"].values()]
        total_requested_cpu = [int(request) for request in metric_spec["resource"]["requests"].values()]
        
        # Calculate average CPU utilization
        avg_cpu = sum(total_cpu) / sum(total_requested_cpu)
        
        # Based on average CPU utilization, adjust target replicas
        evaluation = {}
        evaluation["targetReplicas"] = metric_spec["current_replicas"]
        if avg_cpu > 0.9 and evaluation["targetReplicas"] < 10:
            evaluation["targetReplicas"] += 3
        elif avg_cpu > 0.8 and evaluation["targetReplicas"] < 10:
            evaluation["targetReplicas"] += 1
        elif avg_cpu < 0.1 and evaluation["targetReplicas"] > 2:
            evaluation["targetReplicas"] -= 3
        elif avg_cpu < 0.2 and evaluation["targetReplicas"] > 1:
            evaluation["targetReplicas"] -= 1
            
        # Output evaluation as JSON to CPA resource
        sys.stdout.write(json.dumps(evaluation))

        # evaluation = {}
        # evaluation["targetReplicas"] = 2
        # sys.stdout.write(json.dumps(evaluation))
            
    except ValueError as err:
        # If not an integer, output error
        sys.stderr.write(f"Invalid metric value: {err}")
        exit(1)

if __name__ == "__main__":
    main()