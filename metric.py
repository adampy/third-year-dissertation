import json
import sys


def main():
    # Parse spec into a dict
    spec = json.loads(sys.stdin.read())
    metric(spec)

def metric(spec):
    #metric = CollatedMetrics(cpu=int(pod['Value']), requested_cpu=int(requested_cpu))
    #sys.stdout.write(str(pod['Value']))

    sys.stdout.write(json.dumps(spec["kubernetesMetrics"][0]))

if __name__ == "__main__":
    main()