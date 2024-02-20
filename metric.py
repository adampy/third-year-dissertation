import os
import json
import sys

import logging

def main():
    # Parse spec into a dict
    spec = json.loads(sys.stdin.read())
    metric(spec)

def metric(spec):
    logging.basicConfig(level=logging.INFO)
    
    deployment = spec["kubernetesMetrics"][0]["resource"]
    pod_names = deployment["pod_metrics_info"].keys()
    
    for pod_name in pod_names:
        pod = deployment["pod_metrics_info"][pod_name]
        requested_cpu = deployment["requests"][pod_name]
        logging.info(f"CPU: {pod['Value']}m / {requested_cpu}m")

    sys.stdout.write(str(1))
    #sys.stderr.write("No 'numPods' label on resource being managed")
    #exit(1)

if __name__ == "__main__":
    main()