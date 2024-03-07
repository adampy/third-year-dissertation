import json
import sys


def main():
    # Parse spec into a dict
    spec = json.loads(sys.stdin.read())
    
    with open("metric_input.json", "w") as f:
        f.write(json.dumps(spec))
    
    metric(spec)

def metric(spec):
    sys.stdout.write(json.dumps(spec["kubernetesMetrics"][0]))

if __name__ == "__main__":
    main()